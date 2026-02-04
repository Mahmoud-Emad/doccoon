<template>
    <div class="py-20 px-8 max-md:py-[60px] max-md:px-5 bg-[var(--bg-color)]">
        <div class="max-w-[1200px] mx-auto">
            <h2
                class="text-center text-[32px] max-md:text-[28px] font-semibold mb-4 text-[var(--text-color)]"
            >
                Side-by-Side Diff Checker
            </h2>
            <p
                class="text-center text-base max-md:text-[15px] leading-relaxed mb-12 text-[var(--text-color)] opacity-60 max-w-[640px] mx-auto"
            >
                Compare left and right pages in book view mode with visual diff
                highlighting. Perfect for tracking changes, comparing versions,
                or reviewing edits.
            </p>

            <div
                class="bg-[var(--bg-color)] border border-[var(--border-color)] rounded-lg p-6 mt-8"
            >
                <div class="flex items-center justify-between mb-6">
                    <div class="text-center flex-1">
                        <h3
                            class="text-lg font-semibold m-0 mb-2 text-[var(--text-color)]"
                        >
                            Compare Two Versions
                        </h3>
                        <p
                            class="text-sm m-0 text-[var(--text-color)] opacity-60"
                        >
                            See additions, deletions, and unchanged content at a
                            glance
                        </p>
                    </div>
                    <button
                        class="flex items-center justify-center bg-transparent border border-[var(--border-color)] rounded px-2 py-1.5 cursor-pointer text-[var(--text-color)] opacity-60 transition-all duration-200 hover:opacity-100 hover:border-primary hover:text-primary hover:bg-primary/5 active:scale-95"
                        @click="tryDiff"
                        title="Try it"
                    >
                        <svg
                            width="16"
                            height="16"
                            viewBox="0 0 16 16"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path d="M5 3L11 8L5 13V3Z" fill="currentColor" />
                        </svg>
                    </button>
                </div>

                <div class="grid grid-cols-2 max-md:grid-cols-1 gap-4 mb-6">
                    <div
                        class="border border-[var(--border-color)] rounded-md overflow-hidden"
                    >
                        <div
                            class="bg-[var(--page-bg)] px-3 py-2 text-[13px] font-semibold text-[var(--text-color)] border-b border-[var(--border-color)]"
                        >
                            Left Page (Original)
                        </div>
                        <div class="font-mono text-[13px] leading-snug">
                            <div
                                class="diff-line diff-line-unchanged px-2 py-0.5 whitespace-pre-wrap break-words border-l-[3px] border-l-transparent"
                            >
                                <span
                                    class="inline-block w-5 font-bold mr-2 select-none"
                                    >&nbsp;</span
                                >- **Markdown Support**
                            </div>
                            <div
                                class="diff-line diff-line-removed px-2 py-0.5 whitespace-pre-wrap break-words bg-[#ffeef0] border-l-[3px] border-l-[#dc3545] text-[#24292f]"
                            >
                                <span
                                    class="inline-block w-5 font-bold mr-2 select-none text-[#dc3545]"
                                    >-</span
                                >- **Mermaid Diagrams**
                            </div>
                            <div
                                class="diff-line diff-line-unchanged px-2 py-0.5 whitespace-pre-wrap break-words border-l-[3px] border-l-transparent"
                            >
                                <span
                                    class="inline-block w-5 font-bold mr-2 select-none"
                                    >&nbsp;</span
                                >- **Math Expressions**
                            </div>
                            <div
                                class="diff-line diff-line-unchanged px-2 py-0.5 whitespace-pre-wrap break-words border-l-[3px] border-l-transparent"
                            >
                                <span
                                    class="inline-block w-5 font-bold mr-2 select-none"
                                    >&nbsp;</span
                                >- **Syntax Highlighting**
                            </div>
                            <div
                                class="diff-line diff-line-unchanged px-2 py-0.5 whitespace-pre-wrap break-words border-l-[3px] border-l-transparent"
                            >
                                <span
                                    class="inline-block w-5 font-bold mr-2 select-none"
                                    >&nbsp;</span
                                >- **Dark & Light Themes**
                            </div>
                            <div
                                class="diff-line diff-line-placeholder px-2 py-0.5 whitespace-pre-wrap break-words bg-[#f5f5f5] border-l-[3px] border-l-[#d0d0d0] opacity-50 min-h-[1.5em]"
                            >
                                <span
                                    class="inline-block w-5 font-bold mr-2 select-none text-[#999]"
                                    >&nbsp;</span
                                >&nbsp;
                            </div>
                        </div>
                    </div>

                    <div
                        class="border border-[var(--border-color)] rounded-md overflow-hidden"
                    >
                        <div
                            class="bg-[var(--page-bg)] px-3 py-2 text-[13px] font-semibold text-[var(--text-color)] border-b border-[var(--border-color)]"
                        >
                            Right Page (Modified)
                        </div>
                        <div class="font-mono text-[13px] leading-snug">
                            <div
                                class="diff-line diff-line-unchanged px-2 py-0.5 whitespace-pre-wrap break-words border-l-[3px] border-l-transparent"
                            >
                                <span
                                    class="inline-block w-5 font-bold mr-2 select-none"
                                    >&nbsp;</span
                                >- **Markdown Support**
                            </div>
                            <div
                                class="diff-line diff-line-placeholder px-2 py-0.5 whitespace-pre-wrap break-words bg-[#f5f5f5] border-l-[3px] border-l-[#d0d0d0] opacity-50 min-h-[1.5em]"
                            >
                                <span
                                    class="inline-block w-5 font-bold mr-2 select-none text-[#999]"
                                    >&nbsp;</span
                                >&nbsp;
                            </div>
                            <div
                                class="diff-line diff-line-unchanged px-2 py-0.5 whitespace-pre-wrap break-words border-l-[3px] border-l-transparent"
                            >
                                <span
                                    class="inline-block w-5 font-bold mr-2 select-none"
                                    >&nbsp;</span
                                >- **Math Expressions**
                            </div>
                            <div
                                class="diff-line diff-line-unchanged px-2 py-0.5 whitespace-pre-wrap break-words border-l-[3px] border-l-transparent"
                            >
                                <span
                                    class="inline-block w-5 font-bold mr-2 select-none"
                                    >&nbsp;</span
                                >- **Syntax Highlighting**
                            </div>
                            <div
                                class="diff-line diff-line-unchanged px-2 py-0.5 whitespace-pre-wrap break-words border-l-[3px] border-l-transparent"
                            >
                                <span
                                    class="inline-block w-5 font-bold mr-2 select-none"
                                    >&nbsp;</span
                                >- **Dark & Light Themes**
                            </div>
                            <div
                                class="diff-line diff-line-added px-2 py-0.5 whitespace-pre-wrap break-words bg-[#e6ffed] border-l-[3px] border-l-[#28a745] text-[#24292f]"
                            >
                                <span
                                    class="inline-block w-5 font-bold mr-2 select-none text-[#28a745]"
                                    >+</span
                                >- **Diff Checker**
                            </div>
                        </div>
                    </div>
                </div>

                <div
                    class="flex max-md:flex-col gap-6 max-md:gap-3 max-md:items-start justify-center pt-4 border-t border-[var(--border-color)]"
                >
                    <div
                        class="flex items-center gap-2 text-[13px] text-[var(--text-color)]"
                    >
                        <span
                            class="w-4 h-4 rounded-sm border border-[#28a745] bg-[#e6ffed]"
                        ></span>
                        <span>Added lines (green)</span>
                    </div>
                    <div
                        class="flex items-center gap-2 text-[13px] text-[var(--text-color)]"
                    >
                        <span
                            class="w-4 h-4 rounded-sm border border-[#dc3545] bg-[#ffeef0]"
                        ></span>
                        <span>Removed lines (red)</span>
                    </div>
                    <div
                        class="flex items-center gap-2 text-[13px] text-[var(--text-color)]"
                    >
                        <span
                            class="w-4 h-4 rounded-sm border border-[#d0d0d0] bg-[#f5f5f5]"
                        ></span>
                        <span>Placeholder (gray)</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
function tryDiff() {
    const url = `${window.location.origin}/edit?example=diff`;
    window.open(url, "_blank");
}
</script>
