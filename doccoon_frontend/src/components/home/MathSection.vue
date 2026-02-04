<template>
    <div
        class="py-20 px-8 max-md:py-[60px] max-md:px-5 bg-[var(--section-alt-bg)]"
    >
        <div class="max-w-[1200px] mx-auto">
            <h2
                class="text-center text-[32px] max-md:text-[28px] font-semibold mb-4 text-[var(--text-color)]"
            >
                Mathematical Expressions
            </h2>
            <p
                class="text-center text-base max-md:text-[15px] leading-relaxed mb-12 text-[var(--text-color)] opacity-60 max-w-[640px] mx-auto"
            >
                Write beautiful mathematical notation using LaTeX syntax.
                Support for inline math, display equations, matrices, and
                advanced mathematical symbols.
            </p>

            <div
                class="grid grid-cols-[repeat(auto-fit,minmax(320px,1fr))] max-md:grid-cols-1 gap-6"
            >
                <div
                    v-for="(example, index) in examples"
                    :key="index"
                    class="math-example bg-[var(--page-bg)] border border-[var(--border-color)] rounded-lg p-5 transition-all duration-200 hover:border-primary/30 hover:shadow-md"
                    :data-index="index"
                >
                    <div class="flex items-center justify-between mb-3">
                        <h3
                            class="text-[15px] font-semibold m-0 text-[var(--text-color)]"
                        >
                            {{ example.title }}
                        </h3>
                        <div class="flex gap-2">
                            <button
                                class="relative flex items-center justify-center bg-transparent border border-[var(--border-color)] rounded px-2 py-1.5 cursor-pointer text-[var(--text-color)] opacity-60 transition-all duration-200 hover:opacity-100 hover:border-primary hover:text-primary hover:bg-primary/5 active:scale-95"
                                @click="copyCode(index)"
                                title="Copy code"
                            >
                                <BaseIcon name="copy" :size="16" />
                                <span
                                    v-if="copiedIndex === index"
                                    class="copy-tooltip"
                                    >Copied!</span
                                >
                            </button>
                            <button
                                class="flex items-center justify-center bg-transparent border border-[var(--border-color)] rounded px-2 py-1.5 cursor-pointer text-[var(--text-color)] opacity-60 transition-all duration-200 hover:opacity-100 hover:border-primary hover:text-primary hover:bg-primary/5 active:scale-95"
                                @click="tryCode(index)"
                                title="Try it"
                            >
                                <svg
                                    width="16"
                                    height="16"
                                    viewBox="0 0 16 16"
                                    fill="none"
                                    xmlns="http://www.w3.org/2000/svg"
                                >
                                    <path
                                        d="M5 3L11 8L5 13V3Z"
                                        fill="currentColor"
                                    />
                                </svg>
                            </button>
                        </div>
                    </div>
                    <div
                        class="math-preview bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md p-4 overflow-x-auto min-h-[150px]"
                    >
                        <pre
                            class="math-code m-0 font-mono text-xs leading-relaxed text-[var(--text-color)] opacity-80 whitespace-pre overflow-x-auto"
                            >{{ example.preview }}</pre
                        >
                    </div>
                </div>
            </div>

            <div class="mt-8 text-center">
                <a
                    href="https://katex.org/docs/supported.html"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="inline-flex items-center gap-1.5 text-primary no-underline text-[15px] font-medium px-4 py-2 rounded-md transition-all duration-200 hover:bg-primary/[0.08] hover:gap-2"
                >
                    See supported LaTeX functions
                    <BaseIcon name="chevron-right" :size="16" />
                </a>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { marked } from "marked";
import katex from "katex";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import { logger } from "@/utils/logger";

const props = defineProps<{
    isDarkTheme: boolean;
}>();

const copiedIndex = ref<number | null>(null);

const examples = [
    {
        title: "Basic Equations",
        preview: `Einstein's equation: $E = mc^2$

Pythagorean theorem:

$$
a^2 + b^2 = c^2
$$

The golden ratio: $\\phi = \\frac{1 + \\sqrt{5}}{2}$`,
        tryCode: `# Basic Math Examples

Einstein's equation: $E = mc^2$

Pythagorean theorem:

$$
a^2 + b^2 = c^2
$$

The golden ratio: $\\phi = \\frac{1 + \\sqrt{5}}{2}$`,
    },
    {
        title: "Calculus",
        preview: `Derivative definition:

$$
f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}
$$

Fundamental theorem of calculus:

$$
\\int_a^b f(x) dx = F(b) - F(a)
$$

Sum notation: $\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$`,
        tryCode: `# Calculus Examples

Derivative definition:

$$
f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}
$$

Fundamental theorem of calculus:

$$
\\int_a^b f(x) dx = F(b) - F(a)
$$

Sum notation: $\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$`,
    },
    {
        title: "Advanced Math",
        preview: `Normal distribution:

$$
f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x-\\mu}{\\sigma}\\right)^2}
$$

Matrix:

$$
A = \\begin{pmatrix}
a & b \\\\
c & d
\\end{pmatrix}
$$

Binomial theorem: $\\binom{n}{k} = \\frac{n!}{k!(n-k)!}$`,
        tryCode: `# Advanced Math Examples

Normal distribution:

$$
f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x-\\mu}{\\sigma}\\right)^2}
$$

Matrix:

$$
A = \\begin{pmatrix}
a & b \\\\
c & d
\\end{pmatrix}
$$

Binomial theorem: $\\binom{n}{k} = \\frac{n!}{k!(n-k)!}$`,
    },
];

function escapeHtml(text: string): string {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function renderMathPlaceholders(element: HTMLElement) {
    try {
        const placeholders = element.querySelectorAll(".math-placeholder");

        placeholders.forEach((placeholder) => {
            const mathContent = placeholder.getAttribute("data-math");
            const isDisplay =
                placeholder.getAttribute("data-display") === "true";

            if (!mathContent) return;

            try {
                const container = document.createElement(
                    isDisplay ? "div" : "span",
                );
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

function renderMarkdownWithMath(markdown: string, targetElement: HTMLElement) {
    const mathBlocks: {
        placeholder: string;
        content: string;
        display: boolean;
    }[] = [];
    let mathIndex = 0;

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

    marked.setOptions({ gfm: true, breaks: true });

    let html = marked.parse(processedMarkdown) as string;

    mathBlocks.forEach(({ placeholder, content, display }) => {
        const mathPlaceholder = display
            ? `<div class="math-placeholder" data-math="${escapeHtml(content)}" data-display="true"></div>`
            : `<span class="math-placeholder" data-math="${escapeHtml(content)}" data-display="false"></span>`;
        html = html.replace(placeholder, mathPlaceholder);
    });

    targetElement.innerHTML = html;
    renderMathPlaceholders(targetElement);
}

async function renderExpressions() {
    await new Promise((resolve) => setTimeout(resolve, 100));

    const mathExamples = document.querySelectorAll(".math-example");

    mathExamples.forEach((example, index) => {
        const preview = example.querySelector(".math-preview");
        if (!preview) return;

        const code = examples[index]?.preview;
        if (!code) return;

        let container = preview.querySelector(".math-rendered") as HTMLElement;

        if (!container) {
            const codeElement = preview.querySelector(".math-code");
            if (!codeElement) return;

            container = document.createElement("div");
            container.className = "math-rendered";
            container.setAttribute("data-index", index.toString());
            codeElement.parentElement?.replaceChild(container, codeElement);
        }

        renderMarkdownWithMath(code, container);
    });
}

async function copyCode(index: number) {
    const code = examples[index]?.tryCode;
    if (!code) return;

    try {
        await navigator.clipboard.writeText(code);
        copiedIndex.value = index;
        setTimeout(() => {
            copiedIndex.value = null;
        }, 2000);
    } catch (err) {
        logger.error("Failed to copy code:", err);
    }
}

function tryCode(index: number) {
    // Map index to example key
    const exampleKeys = ["math-basic", "math-calculus", "math-advanced"];
    const exampleKey = exampleKeys[index];
    if (!exampleKey) return;

    const url = `${window.location.origin}/edit?example=${exampleKey}`;
    window.open(url, "_blank");
}

onMounted(() => {
    renderExpressions();
});

watch(
    () => props.isDarkTheme,
    () => {
        renderExpressions();
    },
);
</script>
