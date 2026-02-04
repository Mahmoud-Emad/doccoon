import { watch, type Ref, type ComputedRef } from "vue";
import { marked } from "marked";
import mermaid from "mermaid";
import hljs from "highlight.js";
import katex from "katex";
import "katex/dist/katex.min.css";
import { logger } from "@/utils/logger";
import { escapeHtml } from "@/utils/html";
import { COPY_BUTTON_FEEDBACK_MS } from "@/config/constants";

export function useMarkdown(isDarkTheme: Ref<boolean> | ComputedRef<boolean>) {
  function initializeMermaid() {
    const theme = isDarkTheme.value ? "dark" : "default";
    mermaid.initialize({
      startOnLoad: false,
      theme: theme,
      securityLevel: "strict",
    });
  }

  function updateMermaidTheme() {
    initializeMermaid();
  }

  // Initialize immediately
  initializeMermaid();

  async function renderMarkdown(markdown: string, targetElement: HTMLElement) {
    // Store math expressions before markdown processing
    const mathBlocks: {
      placeholder: string;
      content: string;
      display: boolean;
    }[] = [];
    let mathIndex = 0;

    // Protect block math ($$...$$) - must come before inline math
    let processedMarkdown = markdown.replace(
      /\$\$([\s\S]+?)\$\$/g,
      (_match, content) => {
        const placeholder = `MATH_BLOCK_${mathIndex++}`;
        mathBlocks.push({
          placeholder,
          content: content.trim(),
          display: true,
        });
        return placeholder;
      },
    );

    // Protect inline math ($...$)
    processedMarkdown = processedMarkdown.replace(
      /\$([^\$\n]+?)\$/g,
      (_match, content) => {
        const placeholder = `MATH_INLINE_${mathIndex++}`;
        mathBlocks.push({
          placeholder,
          content: content.trim(),
          display: false,
        });
        return placeholder;
      },
    );

    // Configure marked
    marked.setOptions({
      gfm: true,
      breaks: true,
    });

    // Render markdown
    let html = marked.parse(processedMarkdown) as string;

    // Process task lists
    html = html.replace(
      /<li>\s*\[ \]\s*/g,
      '<li class="task-list-item"><input type="checkbox" disabled> ',
    );
    html = html.replace(
      /<li>\s*\[x\]\s*/gi,
      '<li class="task-list-item"><input type="checkbox" checked disabled> ',
    );
    html = html.replace(
      /<ul>\s*(<li class="task-list-item">)/g,
      '<ul class="contains-task-list">$1',
    );

    // Find mermaid blocks
    const mermaidRegex = /```mermaid\n([\s\S]*?)```/g;
    const mermaidBlocks: string[] = [];
    let match;

    while ((match = mermaidRegex.exec(markdown)) !== null) {
      if (match[1]) {
        mermaidBlocks.push(match[1]);
      }
    }

    // Replace mermaid code blocks with placeholder divs
    let index = 0;
    html = html.replace(
      /<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/g,
      () => {
        return `<div class="mermaid-diagram" id="mermaid-${Date.now()}-${index++}"></div>`;
      },
    );

    // Restore math expressions as placeholders that will be rendered by KaTeX
    mathBlocks.forEach(({ placeholder, content, display }) => {
      const mathPlaceholder = display
        ? `<div class="math-placeholder" data-math="${escapeHtml(content)}" data-display="true"></div>`
        : `<span class="math-placeholder" data-math="${escapeHtml(content)}" data-display="false"></span>`;
      html = html.replace(placeholder, mathPlaceholder);
    });

    targetElement.innerHTML = html;

    // Render mermaid diagrams
    const mermaidDivs = targetElement.querySelectorAll(".mermaid-diagram");
    for (let i = 0; i < mermaidDivs.length && i < mermaidBlocks.length; i++) {
      const mermaidCode = mermaidBlocks[i];
      if (!mermaidCode) continue;

      try {
        const { svg } = await mermaid.render(
          `mermaid-svg-${Date.now()}-${i}`,
          mermaidCode,
        );
        (mermaidDivs[i] as HTMLElement).innerHTML = svg;
      } catch (error) {
        (mermaidDivs[i] as HTMLElement).innerHTML =
          `<pre style="color: red;">Mermaid Error: ${(error as Error).message}</pre>`;
      }
    }

    // Apply syntax highlighting
    targetElement.querySelectorAll("pre code").forEach((block) => {
      hljs.highlightElement(block as HTMLElement);
      addCopyButton(block as HTMLElement);
    });

    // Render KaTeX math expressions from placeholders
    renderMathPlaceholders(targetElement);
  }

  function renderMathPlaceholders(element: HTMLElement) {
    try {
      const placeholders = element.querySelectorAll(".math-placeholder");

      placeholders.forEach((placeholder) => {
        const mathContent = placeholder.getAttribute("data-math");
        const isDisplay = placeholder.getAttribute("data-display") === "true";

        if (!mathContent) return;

        try {
          const container = document.createElement(isDisplay ? "div" : "span");

          katex.render(mathContent, container, {
            displayMode: isDisplay,
            throwOnError: false,
            strict: false,
            trust: false,
          });

          placeholder.replaceWith(container);
        } catch (error) {
          logger.error("KaTeX rendering error:", error);
          placeholder.textContent = isDisplay
            ? `$$${mathContent}$$`
            : `$${mathContent}$`;
        }
      });
    } catch (error) {
      logger.error("Math placeholder processing error:", error);
    }
  }

  function addCopyButton(codeBlock: HTMLElement) {
    const pre = codeBlock.parentElement;
    if (!pre || pre.querySelector(".code-copy-btn")) return;

    const copyBtn = document.createElement("button");
    copyBtn.className = "code-copy-btn";
    copyBtn.innerHTML = getCopyIcon();
    copyBtn.title = "Copy code";

    copyBtn.addEventListener("click", async () => {
      const code = codeBlock.textContent || "";
      await navigator.clipboard.writeText(code);

      copyBtn.innerHTML = getCheckIcon();

      setTimeout(() => {
        copyBtn.innerHTML = getCopyIcon();
      }, COPY_BUTTON_FEEDBACK_MS);
    });

    pre.style.position = "relative";
    pre.appendChild(copyBtn);
  }

  function getCopyIcon(): string {
    return `<svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
      <path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path>
      <path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path>
    </svg>`;
  }

  function getCheckIcon(): string {
    return `<svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
      <path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path>
    </svg>`;
  }

  watch(isDarkTheme, () => {
    updateMermaidTheme();
  });

  return {
    renderMarkdown,
    updateMermaidTheme,
  };
}
