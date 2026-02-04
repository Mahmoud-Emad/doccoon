<template>
    <div
        class="min-h-screen bg-[var(--bg-color)] text-[var(--text-color)] flex flex-col"
    >
        <!-- Navigation Bar -->
        <nav
            class="sticky top-0 z-100 bg-[var(--bg-color)] border-b border-[var(--border-color)]"
        >
            <div
                class="max-w-[1200px] mx-auto px-8 max-md:px-4 h-[60px] flex items-center justify-between"
            >
                <div class="flex items-center gap-2">
                    <img
                        :src="isDarkTheme ? logoDark : logoLight"
                        alt="Doccoon"
                        class="h-10"
                    />
                    <router-link
                        to="/"
                        class="flex items-center gap-2 text-[var(--text-color)] no-underline text-base font-semibold transition-opacity duration-200 hover:opacity-70"
                    >
                        Doccoon
                    </router-link>
                </div>

                <div class="flex items-center gap-3">
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
                </div>
            </div>
        </nav>

        <!-- Loading -->
        <div v-if="loading" class="flex-1 flex items-center justify-center">
            <p class="text-sm text-[var(--text-color)] opacity-60">
                Loading shared page...
            </p>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="flex-1 flex items-center justify-center">
            <div class="text-center">
                <h2 class="text-xl font-semibold mb-2 text-[var(--text-color)]">
                    Page not available
                </h2>
                <p class="text-sm text-[var(--text-color)] opacity-60 mb-6">
                    {{ error }}
                </p>
                <router-link
                    to="/"
                    class="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium text-white bg-primary no-underline rounded-md transition-opacity duration-200 hover:opacity-90"
                >
                    <BaseIcon name="home" :size="16" />
                    Go Home
                </router-link>
            </div>
        </div>

        <!-- Page Content -->
        <div v-else class="flex-1 flex flex-col overflow-hidden">
            <!-- Book title bar -->
            <div
                v-if="bookTitle"
                class="shrink-0 px-6 py-2 border-b border-[var(--border-color)] bg-[var(--bg-color)]"
            >
                <div class="flex items-center justify-center gap-3">
                    <span
                        class="text-sm font-medium text-[var(--text-color)] opacity-70"
                    >
                        {{ bookTitle }}
                    </span>
                    <span class="text-xs text-[var(--text-color)] opacity-40">
                        Page {{ pageNumber }}
                    </span>
                </div>
            </div>

            <!-- Page area - matches editor viewer -->
            <div
                ref="pageRef"
                class="page-view page flex-1 bg-[var(--page-bg)] px-4 md:px-6 lg:px-10 pt-6 pb-12 overflow-y-auto text-base leading-[1.6] text-[var(--text-color)] transition-colors duration-300"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { useRoute } from "vue-router";
import { useTheme } from "@/composables/useTheme";
import { useMarkdown } from "@/composables/useMarkdown";
import { getSharedPage } from "@/api/sharing";
import BaseIcon from "@/components/ui/BaseIcon.vue";

import logoLight from "@/assets/logo-light.png";
import logoDark from "@/assets/logo-dark.png";

const route = useRoute();
const { isDarkTheme, toggleTheme } = useTheme();
const { renderMarkdown } = useMarkdown(isDarkTheme);

const loading = ref(true);
const error = ref("");
const bookTitle = ref("");
const pageNumber = ref(0);
const pageContent = ref("");
const pageRef = ref<HTMLElement>();

onMounted(async () => {
    const token = route.params.token as string;
    if (!token) {
        error.value = "Invalid share link.";
        loading.value = false;
        return;
    }

    try {
        const result = await getSharedPage(token);
        if (result) {
            bookTitle.value = result.book_title;
            pageNumber.value = result.page_number;
            pageContent.value = result.content;

            loading.value = false;

            await nextTick();
            if (pageRef.value) {
                await renderMarkdown(pageContent.value, pageRef.value);
            }
        } else {
            error.value = "This shared page is no longer available.";
            loading.value = false;
        }
    } catch {
        error.value =
            "This shared page was not found or the link has been revoked.";
        loading.value = false;
    }
});
</script>
