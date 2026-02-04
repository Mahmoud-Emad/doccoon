<template>
    <div class="py-20 px-8 max-md:py-12 max-md:px-5 bg-[var(--section-alt-bg)]">
        <div class="max-w-[1200px] mx-auto">
            <!-- Header -->
            <div class="text-center mb-12">
                <p
                    class="text-sm font-semibold tracking-widest uppercase text-primary mb-3"
                >
                    AI Writing Assistant
                </p>
                <h2
                    class="text-[32px] max-md:text-[24px] font-bold mb-4 text-[var(--text-color)] leading-tight"
                >
                    Enhance your writing with AI
                </h2>
                <p
                    class="text-base max-md:text-[15px] leading-relaxed text-[var(--text-color)] opacity-60 max-w-[540px] mx-auto"
                >
                    Refine for clarity and grammar, or rewrite with a fresh
                    perspective. Try it free below.
                </p>
            </div>

            <!-- Mode Pills -->
            <div class="flex items-center justify-center gap-3 mb-6">
                <button
                    v-for="mode in modes"
                    :key="mode.value"
                    class="px-4 py-2 text-sm font-medium rounded-full border transition-all duration-200 cursor-pointer"
                    :class="
                        activeMode === mode.value
                            ? 'bg-primary text-white border-primary'
                            : 'bg-transparent text-[var(--text-color)] opacity-70 border-[var(--border-color)] hover:opacity-100 hover:border-[var(--text-color)]/30'
                    "
                    @click="activeMode = mode.value"
                >
                    {{ mode.label }}
                </button>
            </div>

            <!-- Demo Container - Book Style -->
            <div
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
                    >
                        AI {{ activeMode === "refine" ? "Refine" : "Rewrite" }}
                    </span>
                    <div class="w-[52px]"></div>
                </div>

                <!-- Book Spread -->
                <div
                    class="grid grid-cols-2 max-md:grid-cols-1 min-h-[280px] max-md:min-h-[240px]"
                >
                    <!-- Left Page - Input -->
                    <div
                        class="p-6 max-md:p-4 border-r border-[var(--border-color)] max-md:border-r-0 max-md:border-b bg-[var(--page-bg)] relative flex flex-col"
                    >
                        <div
                            class="text-[10px] font-medium text-[var(--text-color)] opacity-40 uppercase tracking-widest mb-3"
                        >
                            Original
                        </div>
                        <textarea
                            v-model="inputText"
                            class="flex-1 w-full p-0 bg-transparent border-none outline-none resize-none text-[13px] leading-relaxed text-[var(--text-color)] placeholder:text-[var(--text-color)] placeholder:opacity-25 font-mono"
                            :placeholder="placeholderText"
                        ></textarea>
                        <div
                            class="absolute bottom-4 left-6 text-xs text-[var(--text-color)] opacity-20"
                        >
                            1
                        </div>
                    </div>

                    <!-- Right Page - Output -->
                    <div
                        class="p-6 max-md:p-4 bg-[var(--page-bg)] relative flex flex-col"
                    >
                        <div
                            class="text-[10px] font-medium text-[var(--text-color)] opacity-40 uppercase tracking-widest mb-3"
                        >
                            {{
                                activeMode === "refine"
                                    ? "Refined"
                                    : "Rewritten"
                            }}
                        </div>

                        <!-- Loading State -->
                        <div
                            v-if="isLoading"
                            class="flex-1 flex items-center justify-center"
                        >
                            <div class="flex items-center gap-2">
                                <div class="loading-dot"></div>
                                <div
                                    class="loading-dot"
                                    style="animation-delay: 0.15s"
                                ></div>
                                <div
                                    class="loading-dot"
                                    style="animation-delay: 0.3s"
                                ></div>
                            </div>
                        </div>

                        <!-- Output Text with Typewriter -->
                        <div
                            v-else-if="displayedText || isTyping"
                            class="flex-1 overflow-y-auto text-[13px] leading-relaxed text-[var(--text-color)] font-mono whitespace-pre-wrap"
                        >
                            <span>{{ displayedText }}</span>
                            <span
                                v-if="isTyping"
                                class="inline-block w-[2px] h-[1.1em] bg-primary ml-[1px] align-middle animate-blink"
                            ></span>
                        </div>

                        <!-- Empty State -->
                        <div
                            v-else
                            class="flex-1 flex items-center justify-center"
                        >
                            <p
                                class="text-sm text-[var(--text-color)] opacity-25 text-center max-w-[180px]"
                            >
                                {{
                                    activeMode === "refine"
                                        ? "Refined text will appear here"
                                        : "Rewritten text will appear here"
                                }}
                            </p>
                        </div>

                        <div
                            class="absolute bottom-4 right-6 text-xs text-[var(--text-color)] opacity-20"
                        >
                            2
                        </div>
                    </div>
                </div>

                <!-- Footer Bar -->
                <div
                    class="flex items-center justify-between px-5 py-3 border-t border-[var(--border-color)] bg-[var(--section-alt-bg)]/50"
                >
                    <!-- Credits -->
                    <div class="flex items-center gap-5">
                        <div class="flex items-center gap-2">
                            <span
                                class="w-1.5 h-1.5 rounded-full transition-colors duration-200"
                                :class="
                                    hasUsedRefine
                                        ? 'bg-[var(--text-color)] opacity-20'
                                        : 'bg-emerald-500'
                                "
                            ></span>
                            <span
                                class="text-xs text-[var(--text-color)] transition-opacity duration-200"
                                :class="
                                    hasUsedRefine ? 'opacity-40' : 'opacity-60'
                                "
                            >
                                Refine
                            </span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span
                                class="w-1.5 h-1.5 rounded-full transition-colors duration-200"
                                :class="
                                    hasUsedRewrite
                                        ? 'bg-[var(--text-color)] opacity-20'
                                        : 'bg-emerald-500'
                                "
                            ></span>
                            <span
                                class="text-xs text-[var(--text-color)] transition-opacity duration-200"
                                :class="
                                    hasUsedRewrite ? 'opacity-40' : 'opacity-60'
                                "
                            >
                                Rewrite
                            </span>
                        </div>
                    </div>

                    <!-- Run Button -->
                    <button
                        class="inline-flex items-center gap-2 px-5 py-2 text-[13px] font-medium text-white bg-primary border-none rounded-md cursor-pointer transition-all duration-200 hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed"
                        :disabled="isLoading || isTyping || !canRun"
                        @click="runAI"
                    >
                        <span v-if="isLoading">Processing</span>
                        <span v-else-if="isTyping">Typing...</span>
                        <span v-else>
                            Run
                            {{ activeMode === "refine" ? "Refine" : "Rewrite" }}
                        </span>
                        <svg
                            v-if="!isLoading && !isTyping"
                            width="14"
                            height="14"
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
                </div>
            </div>

            <!-- Info Text -->
            <p
                class="text-center text-xs text-[var(--text-color)] opacity-40 mt-5 max-w-[400px] mx-auto"
            >
                <span v-if="hasUsedRefine && hasUsedRewrite">
                    Credits reset every {{ RESET_MINUTES }} minutes.
                    <router-link
                        to="/register"
                        class="text-primary opacity-100 no-underline hover:underline"
                    >
                        Sign up
                    </router-link>
                    for unlimited access.
                </span>
                <span v-else-if="hasUsedRefine && activeMode === 'refine'">
                    Refine used. Try
                    <button
                        class="text-primary opacity-100 bg-transparent border-none cursor-pointer hover:underline p-0 font-inherit"
                        @click="activeMode = 'rewrite'"
                    >
                        Rewrite
                    </button>
                    or wait {{ RESET_MINUTES }} min.
                </span>
                <span v-else-if="hasUsedRewrite && activeMode === 'rewrite'">
                    Rewrite used. Try
                    <button
                        class="text-primary opacity-100 bg-transparent border-none cursor-pointer hover:underline p-0 font-inherit"
                        @click="activeMode = 'refine'"
                    >
                        Refine
                    </button>
                    or wait {{ RESET_MINUTES }} min.
                </span>
                <span v-else>
                    Free demo — 1 of each, resets every {{ RESET_MINUTES }} min.
                </span>
            </p>

            <!-- Error Message -->
            <div
                v-if="errorMessage"
                class="mt-4 max-w-[900px] mx-auto p-4 bg-red-500/5 border border-red-500/15 rounded-lg text-sm text-red-500 text-center"
            >
                {{ errorMessage }}
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { api, type ApiResponse } from "@/api/client";

const RESET_MINUTES = 5;

const modes = [
    { value: "refine" as const, label: "Refine" },
    { value: "rewrite" as const, label: "Rewrite" },
];

const activeMode = ref<"refine" | "rewrite">("refine");
const inputText = ref("");
const outputText = ref("");
const displayedText = ref("");
const isLoading = ref(false);
const isTyping = ref(false);
const errorMessage = ref("");

const hasUsedRefine = ref(false);
const hasUsedRewrite = ref(false);

let typingTimeout: ReturnType<typeof setTimeout> | null = null;

const placeholderText = computed(() =>
    activeMode.value === "refine"
        ? "Enter text to refine grammar and improve clarity..."
        : "Enter text to completely rewrite with a fresh perspective...",
);

// Fetch credit status from backend on mount
async function fetchCreditStatus() {
    try {
        const response = await api.get<{
            refine_used: boolean;
            rewrite_used: boolean;
            reset_minutes: number;
        }>("/ai/demo/");

        if (response.results) {
            hasUsedRefine.value = response.results.refine_used;
            hasUsedRewrite.value = response.results.rewrite_used;
        }
    } catch {
        // Ignore errors, will use default values
    }
}

onMounted(() => {
    fetchCreditStatus();
});

onUnmounted(() => {
    stopTyping();
});

const canRun = computed(() => {
    if (!inputText.value.trim()) return false;
    if (activeMode.value === "refine" && hasUsedRefine.value) return false;
    if (activeMode.value === "rewrite" && hasUsedRewrite.value) return false;
    return true;
});

function stopTyping() {
    if (typingTimeout) {
        clearTimeout(typingTimeout);
        typingTimeout = null;
    }
    isTyping.value = false;
}

function getTypingDelay(char: string, nextChar: string): number {
    // Pause longer after punctuation
    if ([".", "!", "?"].includes(char)) return 80;
    if ([",", ";", ":"].includes(char)) return 50;
    // Pause at newlines
    if (char === "\n") return nextChar === "\n" ? 60 : 40;
    // Fast base speed with slight variation
    return Math.random() * 8 + 12;
}

function startTypewriter(text: string) {
    stopTyping();
    displayedText.value = "";
    isTyping.value = true;

    let index = 0;

    function typeNextChar() {
        if (index < text.length) {
            const currentChar = text[index] ?? "";
            const nextChar = text[index + 1] ?? "";
            displayedText.value = text.slice(0, index + 1);
            index++;

            const delay = getTypingDelay(currentChar, nextChar);
            typingTimeout = setTimeout(typeNextChar, delay);
        } else {
            isTyping.value = false;
        }
    }

    // Small initial delay before starting
    typingTimeout = setTimeout(typeNextChar, 100);
}

async function runAI() {
    if (!canRun.value) return;

    errorMessage.value = "";
    isLoading.value = true;
    outputText.value = "";
    displayedText.value = "";
    stopTyping();

    try {
        const response = await api.post<{
            original: string;
            refined: string;
            mode: string;
        }>("/ai/demo/", {
            content: inputText.value,
            mode: activeMode.value,
        });

        if (response.results) {
            outputText.value = response.results.refined;

            // Mark as used
            if (activeMode.value === "refine") {
                hasUsedRefine.value = true;
            } else {
                hasUsedRewrite.value = true;
            }

            // Start typewriter effect
            isLoading.value = false;
            startTypewriter(response.results.refined);
        }
    } catch (err) {
        const apiErr = err as ApiResponse<{
            exceeded?: boolean;
            mode?: string;
        }>;

        // Check if it's an exceeded error from backend
        if (apiErr?.results?.exceeded) {
            if (activeMode.value === "refine") {
                hasUsedRefine.value = true;
            } else {
                hasUsedRewrite.value = true;
            }
        }

        errorMessage.value =
            apiErr?.message || "Something went wrong. Please try again.";
        isLoading.value = false;
    }
}
</script>

<style scoped>
.loading-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: var(--text-color);
    opacity: 0.4;
    animation: pulse 0.8s ease-in-out infinite;
}

@keyframes pulse {
    0%,
    100% {
        opacity: 0.2;
        transform: scale(0.8);
    }
    50% {
        opacity: 0.5;
        transform: scale(1);
    }
}

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
    animation: blink 0.8s step-end infinite;
}
</style>
