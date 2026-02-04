<template>
    <div
        class="py-20 px-8 max-md:py-[60px] max-md:px-5 bg-[var(--section-alt-bg)]"
    >
        <div class="max-w-[1200px] mx-auto">
            <h2
                class="text-center text-[32px] max-md:text-[28px] font-semibold mb-4 text-[var(--text-color)]"
            >
                Powerful Diagram Support
            </h2>
            <p
                class="text-center text-base max-md:text-[15px] leading-relaxed mb-12 text-[var(--text-color)] opacity-60 max-w-[640px] mx-auto"
            >
                Create beautiful diagrams directly in your markdown using
                Mermaid syntax. Perfect for flowcharts, class diagrams, entity
                relationships, and more.
            </p>

            <div
                class="grid grid-cols-[repeat(auto-fit,minmax(320px,1fr))] max-md:grid-cols-1 gap-6"
            >
                <div
                    v-for="(example, index) in examples"
                    :key="index"
                    class="mermaid-example bg-[var(--bg-color)] border border-[var(--border-color)] rounded-lg p-5 transition-all duration-200 hover:border-primary/30 hover:shadow-md"
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
                        class="mermaid-preview bg-[var(--page-bg)] border border-[var(--border-color)] rounded-md p-4 overflow-x-auto min-h-[150px] flex items-center justify-center"
                    >
                        <pre
                            class="mermaid-code m-0 font-mono text-xs leading-relaxed text-[var(--text-color)] opacity-80 whitespace-pre overflow-x-auto"
                            >{{ example.code }}</pre
                        >
                    </div>
                </div>
            </div>

            <div class="mt-8 text-center">
                <a
                    href="https://mermaid.js.org/intro/"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="inline-flex items-center gap-1.5 text-primary no-underline text-[15px] font-medium px-4 py-2 rounded-md transition-all duration-200 hover:bg-primary/[0.08] hover:gap-2"
                >
                    See more diagram types
                    <BaseIcon name="chevron-right" :size="16" />
                </a>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import mermaid from "mermaid";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import { logger } from "@/utils/logger";

const props = defineProps<{
    isDarkTheme: boolean;
}>();

const copiedIndex = ref<number | null>(null);

const examples = [
    {
        title: "Flowchart",
        code: `graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E`,
    },
    {
        title: "Class Diagram",
        code: `classDiagram
    class Book {
        +String title
        +String author
        +publish()
    }
    class Chapter {
        +String name
        +int pages
    }
    Book "1" --> "*" Chapter`,
    },
    {
        title: "Entity Relationship",
        code: `erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ITEM : contains
    USER {
        string name
        string email
    }`,
    },
];

function initMermaid() {
    mermaid.initialize({
        startOnLoad: false,
        theme: props.isDarkTheme ? "dark" : "default",
        securityLevel: "loose",
        fontFamily: "inherit",
    });
}

async function renderDiagrams() {
    initMermaid();
    await new Promise((resolve) => setTimeout(resolve, 100));

    const mermaidExamples = document.querySelectorAll(".mermaid-example");

    mermaidExamples.forEach((example, index) => {
        const preview = example.querySelector(".mermaid-preview");
        if (!preview) return;

        const code = examples[index]?.code;
        if (!code) return;

        let container = preview.querySelector(
            ".mermaid-rendered",
        ) as HTMLElement;

        if (!container) {
            const codeElement = preview.querySelector(".mermaid-code");
            if (!codeElement) return;

            container = document.createElement("div");
            container.className = "mermaid-rendered";
            container.setAttribute("data-index", index.toString());
            codeElement.parentElement?.replaceChild(container, codeElement);
        }

        mermaid
            .render(`mermaid-svg-${Date.now()}-${index}`, code)
            .then(({ svg }) => {
                container.innerHTML = svg;
            })
            .catch((error) => {
                logger.error("Mermaid rendering error:", error);
                container.innerHTML = `<pre class="mermaid-code">${code}</pre>`;
            });
    });
}

async function copyCode(index: number) {
    const code = examples[index]?.code;
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
    const exampleKeys = ["flowchart", "class-diagram", "er-diagram"];
    const exampleKey = exampleKeys[index];
    if (!exampleKey) return;

    const url = `${window.location.origin}/edit?example=${exampleKey}`;
    window.open(url, "_blank");
}

onMounted(() => {
    renderDiagrams();
});

watch(
    () => props.isDarkTheme,
    () => {
        renderDiagrams();
    },
);
</script>
