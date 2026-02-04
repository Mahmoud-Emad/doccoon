<template>
    <div class="py-20 px-8 max-md:py-12 max-md:px-5 bg-[var(--bg-color)]">
        <div class="max-w-[1200px] mx-auto">
            <!-- Header -->
            <div class="text-center mb-12">
                <p
                    class="text-sm font-semibold tracking-widest uppercase text-primary mb-3"
                >
                    Markdown Book Editor
                </p>
                <h1
                    class="text-[40px] max-md:text-[28px] font-bold mb-4 text-[var(--text-color)] leading-tight"
                >
                    Write beautifully, publish anywhere
                </h1>
                <p
                    class="text-base max-md:text-[15px] leading-relaxed text-[var(--text-color)] opacity-60 max-w-[600px] mx-auto mb-8"
                >
                    A modern editor with a two-page book spread. Write in
                    markdown, create diagrams, add math equations, and enhance
                    with AI.
                </p>
                <div class="flex items-center justify-center gap-3 flex-wrap">
                    <button
                        class="inline-flex items-center gap-2 px-6 py-3 text-[15px] font-medium text-white bg-primary border-none rounded-md cursor-pointer transition-opacity duration-200 hover:opacity-90 active:opacity-80"
                        @click="$emit('start-writing')"
                    >
                        Start Writing
                        <svg
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        >
                            <path d="M5 12h14M12 5l7 7-7 7" />
                        </svg>
                    </button>
                    <router-link
                        to="/docs"
                        class="inline-flex items-center gap-2 px-6 py-3 text-[15px] font-medium text-[var(--text-color)] bg-transparent border border-[var(--border-color)] rounded-md no-underline transition-colors duration-200 hover:bg-[var(--section-alt-bg)]"
                    >
                        Documentation
                    </router-link>
                </div>
            </div>

            <!-- Book Preview -->
            <div
                ref="bookPreview"
                class="relative max-w-[900px] mx-auto rounded-lg overflow-hidden border border-[var(--border-color)] bg-[var(--page-bg)] shadow-lg"
            >
                <!-- Editor Header Bar -->
                <div
                    class="flex items-center justify-between px-4 py-2 border-b border-[var(--border-color)] bg-[var(--section-alt-bg)]"
                >
                    <div class="flex items-center gap-2">
                        <div
                            class="w-3 h-3 rounded-full bg-[#ff5f57] opacity-80"
                        ></div>
                        <div
                            class="w-3 h-3 rounded-full bg-[#ffbd2e] opacity-80"
                        ></div>
                        <div
                            class="w-3 h-3 rounded-full bg-[#28c840] opacity-80"
                        ></div>
                    </div>
                    <span
                        class="text-xs text-[var(--text-color)] opacity-40 font-medium"
                        >Getting Started.md</span
                    >
                    <div class="w-[52px]"></div>
                </div>

                <!-- Book Spread -->
                <div
                    class="grid grid-cols-2 max-md:grid-cols-1 min-h-[400px] max-md:min-h-[300px]"
                >
                    <!-- Left Page - Markdown Source -->
                    <div
                        class="p-6 max-md:p-4 border-r border-[var(--border-color)] max-md:border-r-0 max-md:border-b bg-[var(--page-bg)] relative"
                    >
                        <div
                            class="font-mono text-[13px] leading-relaxed text-[var(--text-color)] whitespace-pre-wrap"
                        >
                            <span>{{ displayedMarkdown }}</span>
                            <span
                                v-if="isTyping"
                                class="inline-block w-[2px] h-[1.2em] bg-primary ml-[1px] align-middle animate-blink"
                            ></span>
                        </div>
                        <div
                            class="absolute bottom-4 left-6 text-xs text-[var(--text-color)] opacity-30"
                        >
                            1
                        </div>
                    </div>

                    <!-- Right Page - Rendered Preview -->
                    <div class="p-6 max-md:p-4 bg-[var(--page-bg)] relative">
                        <div
                            class="page-view text-sm leading-relaxed"
                            v-html="renderedMarkdown"
                        ></div>
                        <div
                            class="absolute bottom-4 right-6 text-xs text-[var(--text-color)] opacity-30"
                        >
                            2
                        </div>
                    </div>
                </div>
            </div>

            <!-- Feature Pills -->
            <div
                class="flex items-center justify-center gap-4 mt-8 flex-wrap max-md:gap-3"
            >
                <div
                    v-for="feature in features"
                    :key="feature"
                    class="px-3 py-1.5 bg-[var(--section-alt-bg)] border border-[var(--border-color)] rounded-full text-sm text-[var(--text-color)] opacity-70"
                >
                    {{ feature }}
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { marked } from "marked";

defineProps<{
    isDarkTheme?: boolean;
}>();

defineEmits<{
    "start-writing": [];
}>();

const features = [
    "Markdown",
    "Mermaid",
    "LaTeX",
    "AI",
    "Cloud Sync",
    "Sharing",
];

const fullMarkdown = `# Welcome to Doccoon

A modern **markdown editor** with a unique two-page book spread.

## Features

- Full Markdown support
- Mermaid diagrams
- LaTeX math equations
- AI-powered writing

> "The best way to predict the future is to create it."`;

const displayedMarkdown = ref("");
const isTyping = ref(true);
const bookPreview = ref<HTMLElement | null>(null);
const isVisible = ref(false);
const hasStartedTyping = ref(false);

// Configure marked
marked.setOptions({
    gfm: true,
    breaks: true,
});

const renderedMarkdown = computed(() => {
    if (!displayedMarkdown.value) return "";
    return marked.parse(displayedMarkdown.value) as string;
});

let typingTimeout: ReturnType<typeof setTimeout> | null = null;
let observer: IntersectionObserver | null = null;

function getTypingDelay(char: string, nextChar: string): number {
    // Pause longer after punctuation
    if ([".', '!", "?"].includes(char)) return 400;
    if ([",", ";", ":"].includes(char)) return 200;
    // Pause at newlines
    if (char === "\n") return nextChar === "\n" ? 300 : 150;
    // Faster for repeated characters or within words
    return Math.random() * 30 + 25;
}

function startTyping() {
    if (hasStartedTyping.value) return;
    hasStartedTyping.value = true;

    let index = 0;
    isTyping.value = true;

    function typeNextChar() {
        if (index < fullMarkdown.length) {
            const currentChar = fullMarkdown[index] ?? "";
            const nextChar = fullMarkdown[index + 1] ?? "";
            displayedMarkdown.value = fullMarkdown.slice(0, index + 1);
            index++;

            const delay = getTypingDelay(currentChar, nextChar);
            typingTimeout = setTimeout(typeNextChar, delay);
        } else {
            isTyping.value = false;
        }
    }

    // Small initial delay before starting
    typingTimeout = setTimeout(typeNextChar, 500);
}

function stopTyping() {
    if (typingTimeout) {
        clearTimeout(typingTimeout);
        typingTimeout = null;
    }
}

watch(isVisible, (visible) => {
    if (visible && !hasStartedTyping.value) {
        startTyping();
    }
});

onMounted(() => {
    // Use Intersection Observer to start typing only when visible
    observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                isVisible.value = entry.isIntersecting;
            });
        },
        { threshold: 0.3 },
    );

    if (bookPreview.value) {
        observer.observe(bookPreview.value);
    }
});

onUnmounted(() => {
    stopTyping();
    if (observer) {
        observer.disconnect();
    }
});
</script>

<style scoped>
@keyframes blink {
    0%,
    50% {
        opacity: 1;
    }
    51%,
    100% {
        opacity: 0;
    }
}

.animate-blink {
    animation: blink 1s step-end infinite;
}
</style>
