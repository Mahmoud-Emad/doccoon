<template>
    <footer
        class="bg-[var(--bg-color)] border-t border-[var(--border-color)] pt-16 pb-8 px-8"
    >
        <div class="max-w-[1200px] mx-auto">
            <div
                class="grid grid-cols-[2fr_1fr_1fr_1fr] max-md:grid-cols-2 max-sm:grid-cols-1 gap-12 max-md:gap-8 mb-12"
            >
                <!-- About Section -->
                <div
                    class="flex flex-col gap-4 max-md:col-span-2 max-sm:col-span-1"
                >
                    <div class="flex items-center gap-2">
                        <img
                            :src="isDarkTheme ? logoDark : logoLight"
                            alt="Doccoon"
                            class="h-8"
                        />
                        <h3
                            class="text-base font-semibold m-0 text-[var(--text-color)]"
                        >
                            Doccoon
                        </h3>
                    </div>
                    <p
                        class="m-0 text-sm leading-relaxed text-[var(--text-color)] opacity-60 max-w-[320px]"
                    >
                        A modern markdown-based book editor with a beautiful
                        two-page spread interface. Write, edit, and organize
                        your content with powerful features.
                    </p>
                </div>

                <!-- Product Links -->
                <div class="flex flex-col gap-4">
                    <h4
                        class="text-xs font-semibold m-0 text-[var(--text-color)] uppercase tracking-wider opacity-50"
                    >
                        Product
                    </h4>
                    <ul class="list-none p-0 m-0 flex flex-col gap-2">
                        <li class="m-0">
                            <router-link
                                to="/edit"
                                class="text-[var(--text-color)] no-underline text-sm opacity-70 transition-all duration-200 inline-block hover:opacity-100 hover:text-primary"
                                >Editor</router-link
                            >
                        </li>
                        <li class="m-0">
                            <router-link
                                to="/docs"
                                class="text-[var(--text-color)] no-underline text-sm opacity-70 transition-all duration-200 inline-block hover:opacity-100 hover:text-primary"
                                >Documentation</router-link
                            >
                        </li>
                        <li class="m-0">
                            <a
                                href="#features"
                                class="text-[var(--text-color)] no-underline text-sm opacity-70 transition-all duration-200 inline-block hover:opacity-100 hover:text-primary"
                                @click.prevent="scrollToFeatures"
                                >Features</a
                            >
                        </li>
                        <li class="m-0">
                            <a
                                href="#ai"
                                class="text-[var(--text-color)] no-underline text-sm opacity-70 transition-all duration-200 inline-block hover:opacity-100 hover:text-primary"
                                @click.prevent="scrollToAI"
                                >AI Assistant</a
                            >
                        </li>
                    </ul>
                </div>

                <!-- Resources Links -->
                <div class="flex flex-col gap-4">
                    <h4
                        class="text-xs font-semibold m-0 text-[var(--text-color)] uppercase tracking-wider opacity-50"
                    >
                        Resources
                    </h4>
                    <ul class="list-none p-0 m-0 flex flex-col gap-2">
                        <li class="m-0">
                            <a
                                href="https://www.markdownguide.org/"
                                target="_blank"
                                rel="noopener noreferrer"
                                class="text-[var(--text-color)] no-underline text-sm opacity-70 transition-all duration-200 inline-block hover:opacity-100 hover:text-primary"
                                >Markdown Guide</a
                            >
                        </li>
                        <li class="m-0">
                            <a
                                href="https://mermaid.js.org/intro/"
                                target="_blank"
                                rel="noopener noreferrer"
                                class="text-[var(--text-color)] no-underline text-sm opacity-70 transition-all duration-200 inline-block hover:opacity-100 hover:text-primary"
                                >Mermaid Docs</a
                            >
                        </li>
                        <li class="m-0">
                            <a
                                href="https://katex.org/docs/supported.html"
                                target="_blank"
                                rel="noopener noreferrer"
                                class="text-[var(--text-color)] no-underline text-sm opacity-70 transition-all duration-200 inline-block hover:opacity-100 hover:text-primary"
                                >KaTeX Reference</a
                            >
                        </li>
                    </ul>
                </div>

                <!-- Legal Links -->
                <div class="flex flex-col gap-4">
                    <h4
                        class="text-xs font-semibold m-0 text-[var(--text-color)] uppercase tracking-wider opacity-50"
                    >
                        Legal
                    </h4>
                    <ul class="list-none p-0 m-0 flex flex-col gap-2">
                        <li class="m-0">
                            <router-link
                                to="/privacy"
                                class="text-[var(--text-color)] no-underline text-sm opacity-70 transition-all duration-200 inline-block hover:opacity-100 hover:text-primary"
                                >Privacy Policy</router-link
                            >
                        </li>
                        <li class="m-0">
                            <router-link
                                to="/terms"
                                class="text-[var(--text-color)] no-underline text-sm opacity-70 transition-all duration-200 inline-block hover:opacity-100 hover:text-primary"
                                >Terms of Service</router-link
                            >
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Footer Bottom -->
            <div
                class="border-t border-[var(--border-color)] pt-6 flex items-center justify-between max-md:flex-col max-md:gap-4"
            >
                <p class="m-0 text-[13px] text-[var(--text-color)] opacity-50">
                    &copy; {{ new Date().getFullYear() }} Doccoon. All rights
                    reserved.
                </p>
                <div class="flex items-center gap-4">
                    <a
                        href="mailto:support@doccoon.com"
                        class="text-[13px] text-[var(--text-color)] opacity-50 no-underline hover:opacity-80 hover:text-primary transition-all duration-200"
                    >
                        Contact Support
                    </a>
                </div>
            </div>
        </div>
    </footer>
</template>

<script setup lang="ts">
import { useTheme } from "@/composables/useTheme";
import logoLight from "@/assets/logo-light.png";
import logoDark from "@/assets/logo-dark.png";

const { isDarkTheme } = useTheme();

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

function scrollToFeatures() {
    scrollToSection("features");
}

function scrollToAI() {
    scrollToSection("ai");
}
</script>
