<template>
    <div class="min-h-screen bg-[var(--bg-color)] text-[var(--text-color)]">
        <!-- Navigation Bar -->
        <nav
            class="sticky top-0 z-100 bg-[var(--bg-color)] border-b border-[var(--border-color)]"
        >
            <div
                class="max-w-[1200px] mx-auto px-8 md:px-8 max-md:px-4 h-[60px] flex items-center justify-between"
            >
                <div class="flex items-center gap-2 max-md:gap-4">
                    <img
                        :src="isDarkTheme ? logoDark : logoLight"
                        alt="Doccoon"
                        class="h-10 max-md:h-10 mx-auto"
                    />
                    <router-link
                        to="/"
                        class="flex items-center gap-2 text-[var(--text-color)] no-underline text-base font-semibold transition-opacity duration-200 hover:opacity-70"
                    >
                        Doccoon
                    </router-link>

                    <div class="flex gap-1 max-md:hidden">
                        <button
                            class="px-3 py-1.5 text-[var(--text-color)] bg-transparent border-none text-sm font-medium rounded-md transition-colors duration-200 opacity-70 hover:bg-[var(--page-bg)] hover:opacity-100 cursor-pointer"
                            @click="startWriting"
                        >
                            Editor
                        </button>
                        <router-link
                            to="/docs"
                            class="px-3 py-1.5 text-[var(--text-color)] no-underline text-sm font-medium rounded-md transition-colors duration-200 opacity-70 hover:bg-[var(--page-bg)] hover:opacity-100 [&.router-link-active]:bg-[var(--page-bg)] [&.router-link-active]:opacity-100"
                            >Docs</router-link
                        >
                        <a
                            href="#features"
                            class="px-3 py-1.5 text-[var(--text-color)] no-underline text-sm font-medium rounded-md transition-colors duration-200 opacity-70 hover:bg-[var(--page-bg)] hover:opacity-100"
                            @click.prevent="scrollToSection('features')"
                            >Features</a
                        >
                        <a
                            href="#ai"
                            class="px-3 py-1.5 text-[var(--text-color)] no-underline text-sm font-medium rounded-md transition-colors duration-200 opacity-70 hover:bg-[var(--page-bg)] hover:opacity-100"
                            @click.prevent="scrollToSection('ai')"
                            >AI</a
                        >
                    </div>
                </div>

                <div class="flex items-center gap-3 max-md:gap-2">
                    <button
                        class="flex items-center justify-center w-8 h-8 bg-transparent border border-[var(--border-color)] rounded-md text-[var(--text-color)] cursor-pointer transition-colors duration-200 hover:bg-[var(--section-alt-bg)]"
                        title="Toggle theme"
                        @click="toggleTheme"
                    >
                        <BaseIcon
                            :name="isDarkTheme ? 'sun' : 'moon'"
                            :size="16"
                        />
                    </button>
                    <template v-if="loggedIn">
                        <NotificationDropdown />
                        <UserProfileDropdown />
                    </template>
                    <template v-else>
                        <router-link
                            to="/login"
                            class="px-3 py-1.5 text-[var(--text-color)] no-underline text-sm font-medium rounded-md transition-colors duration-200 opacity-70 hover:bg-[var(--page-bg)] hover:opacity-100"
                        >
                            Sign in
                        </router-link>
                        <router-link
                            to="/register"
                            class="px-3.5 py-1.5 bg-primary text-white no-underline text-sm font-medium rounded-md transition-opacity duration-200 hover:opacity-90"
                        >
                            Sign up
                        </router-link>
                    </template>
                </div>
            </div>
        </nav>

        <HeroSection
            :is-dark-theme="isDarkTheme"
            @start-writing="startWriting"
        />
        <AboutSection />
        <div id="features">
            <FeaturesSection />
        </div>
        <div id="ai">
            <AIDemoSection />
        </div>
        <MermaidSection :is-dark-theme="isDarkTheme" />
        <CodeSection />
        <MathSection :is-dark-theme="isDarkTheme" />
        <DiffSection />
        <CTASection @start-writing="startWriting" />
        <AppFooter />

        <!-- Book Selection Dialog -->
        <BookSelectionDialog
            v-model:visible="bookDialogVisible"
            @select="handleBookSelect"
            @create="handleCreateBook"
            @close="bookDialogVisible = false"
        />

        <!-- Anonymous User Dialog -->
        <AnonymousUserDialog
            :visible="anonymousDialogVisible"
            @close="anonymousDialogVisible = false"
            @continue="handleAnonymousContinue"
        />
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useTheme } from "@/composables/useTheme";
import { useViewMode } from "@/composables/useViewMode";
import AppFooter from "@/components/AppFooter.vue";
import UserProfileDropdown from "@/components/UserProfileDropdown.vue";
import NotificationDropdown from "@/components/NotificationDropdown.vue";
import HeroSection from "@/components/home/HeroSection.vue";
import MermaidSection from "@/components/home/MermaidSection.vue";
import CodeSection from "@/components/home/CodeSection.vue";
import MathSection from "@/components/home/MathSection.vue";
import DiffSection from "@/components/home/DiffSection.vue";
import FeaturesSection from "@/components/home/FeaturesSection.vue";
import AIDemoSection from "@/components/home/AIDemoSection.vue";
import AboutSection from "@/components/home/AboutSection.vue";
import CTASection from "@/components/home/CTASection.vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import BookSelectionDialog from "@/components/BookSelectionDialog.vue";
import AnonymousUserDialog from "@/components/AnonymousUserDialog.vue";
import { isAuthenticated } from "@/api/auth";
import type { BookSummary } from "@/types";

import logoLight from "@/assets/logo-light.png";
import logoDark from "@/assets/logo-dark.png";

const router = useRouter();
const { isDarkTheme, toggleTheme } = useTheme();
const { setViewMode } = useViewMode();
const loggedIn = ref(isAuthenticated());
const bookDialogVisible = ref(false);
const anonymousDialogVisible = ref(false);
const pendingViewMode = ref(false);

function scrollToSection(sectionId: string) {
    const element = document.getElementById(sectionId);
    if (element) {
        const navbarHeight = 60;
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.scrollY - navbarHeight;
        window.scrollTo({
            top: offsetPosition,
            behavior: "smooth",
        });
    }
}

function startWriting() {
    setViewMode(false); // Edit mode
    pendingViewMode.value = false;

    if (isAuthenticated()) {
        bookDialogVisible.value = true;
    } else {
        // Show anonymous user dialog
        anonymousDialogVisible.value = true;
    }
}

function handleAnonymousContinue() {
    anonymousDialogVisible.value = false;
    const path = pendingViewMode.value ? "/view" : "/edit";
    router.push(path);
}

function handleBookSelect(book: BookSummary) {
    const path = pendingViewMode.value ? "/view" : "/edit";
    router.push({ path, query: { book: String(book.id) } });
}

function handleCreateBook() {
    const path = pendingViewMode.value ? "/view" : "/edit";
    router.push(`${path}?new=true`);
}
</script>

<style>
/* Import highlight.js theme */
@import "highlight.js/styles/github.css";

/* Tooltip animation */
.copy-tooltip {
    position: absolute;
    bottom: calc(100% + 8px);
    left: 50%;
    transform: translateX(-50%);
    background: #007acc;
    color: white;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
    white-space: nowrap;
    pointer-events: none;
    animation: tooltipFadeIn 0.2s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.copy-tooltip::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 4px solid transparent;
    border-top-color: #007acc;
}

@keyframes tooltipFadeIn {
    from {
        opacity: 0;
        transform: translateX(-50%) translateY(-4px);
    }
    to {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
}

/* Mermaid rendered container */
.mermaid-rendered {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.mermaid-rendered svg {
    max-width: 100%;
    height: auto;
}

/* Math rendered container */
.math-rendered {
    color: var(--text-color);
    font-size: 14px;
    line-height: 1.8;
}

.math-rendered h1 {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 12px 0;
    color: var(--text-color);
}

.math-rendered p {
    margin: 8px 0;
    color: var(--text-color);
}

.math-rendered .katex {
    font-size: 1em;
    color: var(--text-color);
}

.math-rendered .katex-display {
    margin: 12px 0;
    overflow-x: auto;
    overflow-y: hidden;
}

body.dark-theme .math-rendered .katex {
    color: var(--text-color);
}

body.dark-theme .math-rendered .katex .mord,
body.dark-theme .math-rendered .katex .mbin,
body.dark-theme .math-rendered .katex .mrel,
body.dark-theme .math-rendered .katex .mop,
body.dark-theme .math-rendered .katex .mpunct,
body.dark-theme .math-rendered .katex .mopen,
body.dark-theme .math-rendered .katex .mclose,
body.dark-theme .math-rendered .katex .minner {
    color: var(--text-color);
}

/* Dark theme overrides for code preview */
body.dark-theme .code-preview {
    background: #0d1117;
}

/* Dark theme diff overrides for the home page demo */
body.dark-theme .diff-line-added {
    background-color: #1e4620 !important;
    border-left-color: #3fb950 !important;
    color: #c9d1d9 !important;
}

body.dark-theme .diff-line-removed {
    background-color: #4a1c1c !important;
    border-left-color: #f85149 !important;
    color: #c9d1d9 !important;
}

body.dark-theme .diff-line-placeholder {
    background-color: #0d1117 !important;
    border-left-color: #444 !important;
}
</style>
