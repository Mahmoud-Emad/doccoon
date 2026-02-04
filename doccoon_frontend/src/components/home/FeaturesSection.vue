<template>
    <div class="py-20 px-8 bg-[var(--bg-color)]">
        <h2
            class="text-center text-[28px] max-md:text-2xl font-semibold mb-4 text-[var(--text-color)]"
        >
            Features
        </h2>
        <p
            class="text-center text-base max-md:text-[15px] leading-relaxed mb-12 text-[var(--text-color)] opacity-60 max-w-[640px] mx-auto"
        >
            Everything you need to write, visualize, and share beautiful
            documents.
        </p>

        <div
            class="max-w-[1000px] mx-auto grid grid-cols-3 max-md:grid-cols-1 gap-5"
        >
            <div
                v-for="feature in features"
                :key="feature.title"
                class="p-6 bg-[var(--section-alt-bg)] border border-[var(--border-color)] rounded-lg transition-all duration-200 hover:border-primary/30 hover:shadow-md"
            >
                <div
                    class="mb-4 flex items-center justify-start"
                    v-html="feature.icon"
                ></div>
                <h3
                    class="text-base font-semibold m-0 mb-2 text-[var(--text-color)]"
                >
                    {{ feature.title }}
                </h3>
                <p
                    class="text-sm leading-normal m-0 text-[var(--text-color)] opacity-60"
                >
                    {{ feature.description }}
                </p>
            </div>

            <div
                class="p-6 bg-[var(--section-alt-bg)] border border-[var(--border-color)] rounded-lg transition-all duration-200 hover:border-primary/30 hover:shadow-md"
            >
                <div class="mb-4 flex items-center justify-start">
                    <svg
                        width="40"
                        height="40"
                        viewBox="0 0 40 40"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <circle
                            cx="20"
                            cy="20"
                            r="14"
                            stroke="#007ACC"
                            stroke-width="2"
                            fill="none"
                        />
                        <path
                            d="M15 20H25M20 15V25"
                            stroke="#007ACC"
                            stroke-width="2"
                            stroke-linecap="round"
                        />
                    </svg>
                </div>
                <h3
                    class="text-base font-semibold m-0 mb-3 text-[var(--text-color)]"
                >
                    And More
                </h3>
                <ul class="list-none p-0 m-0 flex flex-col gap-1.5">
                    <li
                        v-for="item in moreFeatures"
                        :key="item"
                        class="text-sm text-[var(--text-color)] opacity-60 flex items-center gap-2"
                    >
                        <span class="text-primary text-xs">&#9679;</span>
                        {{ item }}
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
const features = [
    {
        title: "Markdown Support",
        description:
            "Full GitHub Flavored Markdown with live preview, task lists, tables, and more.",
        icon: '<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 10H32M8 20H32M8 30H24" stroke="#007ACC" stroke-width="3" stroke-linecap="round"/></svg>',
    },
    {
        title: "Mermaid Diagrams",
        description:
            "Create flowcharts, sequence diagrams, and other visualizations directly in your text.",
        icon: '<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="5" y="10" width="10" height="20" stroke="#007ACC" stroke-width="2" fill="none"/><rect x="25" y="10" width="10" height="20" stroke="#007ACC" stroke-width="2" fill="none"/><path d="M15 20H25M20 15V25" stroke="#007ACC" stroke-width="2"/></svg>',
    },
    {
        title: "Math Expressions",
        description:
            "Beautiful mathematical notation with KaTeX support for inline and display equations.",
        icon: '<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><text x="8" y="28" font-size="24" font-weight="bold" fill="#007ACC">&#x2211;x&#xB2;</text></svg>',
    },
    {
        title: "AI-Powered Refinement",
        description:
            "Enhance your writing with AI. Choose between OpenAI and Gemini providers, select your preferred model, and refine or rewrite content with a click.",
        icon: '<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 6L22.5 14H31L24.5 19L27 27L20 22L13 27L15.5 19L9 14H17.5L20 6Z" stroke="#007ACC" stroke-width="2" fill="none" stroke-linejoin="round"/><circle cx="20" cy="18" r="3" fill="#007ACC"/></svg>',
    },
    {
        title: "Sharing & Collaboration",
        description:
            "Share pages via secure links with versioned content snapshots. Share on WhatsApp, Facebook, or Telegram. Revoke access anytime.",
        icon: '<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="14" cy="20" r="4" stroke="#007ACC" stroke-width="2" fill="none"/><circle cx="30" cy="12" r="3" stroke="#007ACC" stroke-width="2" fill="none"/><circle cx="30" cy="28" r="3" stroke="#007ACC" stroke-width="2" fill="none"/><path d="M17.5 18L27.5 13M17.5 22L27.5 27" stroke="#007ACC" stroke-width="2" stroke-linecap="round"/></svg>',
    },
    {
        title: "Cloud Sync & Auto-Save",
        description:
            "Your books sync to the cloud automatically with configurable save intervals. Access your work from any device, anytime.",
        icon: '<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 28h14a7 7 0 10-2-13.74A9 9 0 1013 28z" stroke="#007ACC" stroke-width="2" fill="none" stroke-linejoin="round"/></svg>',
    },
    {
        title: "Accounts & Authentication",
        description:
            "Sign in with Google, GitHub, or email. Your books, editor preferences, and AI provider keys stay with your account.",
        icon: '<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="20" cy="15" r="6" stroke="#007ACC" stroke-width="2" fill="none"/><path d="M10 33c0-5.523 4.477-10 10-10s10 4.477 10 10" stroke="#007ACC" stroke-width="2" fill="none" stroke-linecap="round"/></svg>',
    },
    {
        title: "Profile & Book Management",
        description:
            "Manage all your books from a dedicated profile page. Create, edit, delete, and organize your library in one place.",
        icon: '<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="8" y="6" width="24" height="28" rx="2" stroke="#007ACC" stroke-width="2" fill="none"/><path d="M14 14h12M14 20h12M14 26h8" stroke="#007ACC" stroke-width="2" stroke-linecap="round"/></svg>',
    },
];

const moreFeatures = [
    "Syntax Highlighting for 100+ languages",
    "Two-Page Book Spread layout",
    "Dark & Light Themes",
    "Drag & Drop images and links",
    "Side-by-Side Diff Checker",
    "Line numbers with word-wrap sync",
    "Configurable editor preferences",
    "In-app notification system",
    "Content versioning for shared pages",
];
</script>
