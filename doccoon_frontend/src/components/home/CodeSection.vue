<template>
    <div class="py-20 px-8 max-md:py-[60px] max-md:px-5 bg-[var(--bg-color)]">
        <div class="max-w-[1200px] mx-auto">
            <h2
                class="text-center text-[32px] max-md:text-[28px] font-semibold mb-4 text-[var(--text-color)]"
            >
                Beautiful Code Blocks
            </h2>
            <p
                class="text-center text-base max-md:text-[15px] leading-relaxed mb-12 text-[var(--text-color)] opacity-60 max-w-[640px] mx-auto"
            >
                Syntax highlighting for 100+ programming languages with
                automatic language detection. Write clean, readable code
                examples with beautiful color schemes.
            </p>

            <div
                class="grid grid-cols-[repeat(auto-fit,minmax(320px,1fr))] max-md:grid-cols-1 gap-6"
            >
                <div
                    v-for="(example, index) in examples"
                    :key="index"
                    class="code-example bg-[var(--page-bg)] border border-[var(--border-color)] rounded-lg p-5 transition-all duration-200 hover:border-primary/30 hover:shadow-md"
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
                        class="code-preview bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md overflow-hidden"
                    >
                        <pre
                            class="m-0 p-4 overflow-x-auto text-[13px] leading-normal"
                        ><code :class="`language-${example.language} font-mono block`" v-html="highlightedCode[index]"></code></pre>
                    </div>
                </div>
            </div>

            <div class="mt-8 text-center">
                <a
                    href="https://highlightjs.org/static/demo/"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="inline-flex items-center gap-1.5 text-primary no-underline text-[15px] font-medium px-4 py-2 rounded-md transition-all duration-200 hover:bg-primary/[0.08] hover:gap-2"
                >
                    See all supported languages
                    <BaseIcon name="chevron-right" :size="16" />
                </a>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import hljs from "highlight.js";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import { logger } from "@/utils/logger";

const copiedIndex = ref<number | null>(null);

const examples = [
    {
        title: "TypeScript",
        language: "typescript",
        code: `interface Book {
  title: string;
  author: string;
  pages: number;
}

function createBook(title: string, author: string): Book {
  return {
    title,
    author,
    pages: 0
  };
}`,
    },
    {
        title: "Python",
        language: "python",
        code: `class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author
        self.pages = 0

    def add_chapter(self, name: str, pages: int):
        self.pages += pages
        print(f"Added chapter: {name}")

    def remove_chapter(self, name: str):
        self.pages -= pages
        print(f"Removed chapter: {name}")`,
    },
];

const highlightedCode = computed(() => {
    return examples.map((example) => {
        try {
            return hljs.highlight(example.code, { language: example.language })
                .value;
        } catch {
            return hljs.highlightAuto(example.code).value;
        }
    });
});

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
    const example = examples[index];
    if (!example) return;

    // Use simple example key for clean URLs
    const exampleKey = example.language; // "typescript" or "python"
    const url = `${window.location.origin}/edit?example=${exampleKey}`;
    window.open(url, "_blank");
}
</script>
