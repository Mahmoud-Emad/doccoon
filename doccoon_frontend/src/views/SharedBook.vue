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

                <div class="flex items-center gap-2">
                    <BaseTooltip
                        v-if="pages.length > 1"
                        :text="
                            layoutMode === 'page' ? 'Book view' : 'Page view'
                        "
                        position="bottom"
                    >
                        <button
                            class="flex items-center justify-center w-8 h-8 bg-transparent border border-[var(--border-color)] rounded-md text-[var(--text-color)] cursor-pointer transition-colors duration-200 hover:bg-[var(--section-alt-bg)]"
                            @click="toggleLayoutMode"
                        >
                            <BaseIcon
                                :name="
                                    layoutMode === 'page' ? 'book-open' : 'file'
                                "
                                :size="16"
                            />
                        </button>
                    </BaseTooltip>
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
                Loading shared book...
            </p>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="flex-1 flex items-center justify-center">
            <div class="text-center">
                <h2 class="text-xl font-semibold mb-2 text-[var(--text-color)]">
                    Book not available
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

        <!-- Book Content -->
        <template v-else>
            <!-- Title bar -->
            <div
                class="shrink-0 px-6 py-2 border-b border-[var(--border-color)] bg-[var(--bg-color)]"
            >
                <div class="flex items-center justify-center gap-3">
                    <span
                        class="text-sm font-medium text-[var(--text-color)] opacity-70"
                    >
                        {{ bookTitle }}
                    </span>
                    <span
                        v-if="bookDescription"
                        class="text-xs text-[var(--text-color)] opacity-40"
                    >
                        {{ bookDescription }}
                    </span>
                </div>
            </div>

            <!-- Spread viewer -->
            <BookSpread
                :spread="displaySpread"
                :is-view-mode="true"
                :layout-mode="layoutMode"
                :is-diff-mode="false"
                :render-markdown="renderMarkdown"
                @toggle-layout="toggleLayoutMode"
            />

            <!-- Footer navigation -->
            <div
                class="flex items-center justify-between px-6 py-4 bg-[var(--bg-color)] border-t border-[var(--border-color)] min-h-[70px]"
            >
                <BaseButton
                    variant="secondary"
                    size="md"
                    :disabled="!canGoPrevious"
                    @click="goToPrevious"
                >
                    <BaseIcon name="chevron-left" :size="20" />
                    Previous
                </BaseButton>

                <div
                    class="text-sm font-medium text-[var(--text-color)] opacity-70"
                >
                    {{ navigationLabel }}
                </div>

                <BaseButton
                    variant="secondary"
                    size="md"
                    :disabled="!canGoNext"
                    @click="goToNext"
                >
                    Next
                    <BaseIcon name="chevron-right" :size="20" />
                </BaseButton>
            </div>
        </template>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from "vue";
import { useRoute } from "vue-router";
import { useTheme } from "@/composables/useTheme";
import { useLayoutMode } from "@/composables/useLayoutMode";
import { useMarkdown } from "@/composables/useMarkdown";
import { getSharedBook } from "@/api/sharing";
import BookSpread from "@/components/BookSpread.vue";
import BaseButton from "@/components/ui/BaseButton.vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import BaseTooltip from "@/components/ui/BaseTooltip.vue";

import logoLight from "@/assets/logo-light.png";
import logoDark from "@/assets/logo-dark.png";

const route = useRoute();
const { isDarkTheme, toggleTheme } = useTheme();
const { layoutMode, toggleLayoutMode } = useLayoutMode();
const { renderMarkdown } = useMarkdown(isDarkTheme);

const loading = ref(true);
const error = ref("");
const bookTitle = ref("");
const bookDescription = ref("");

interface SnapshotPage {
    page_number: number;
    content: string;
}

const pages = ref<SnapshotPage[]>([]);

// Build spreads from pages: pair pages[0]+pages[1], pages[2]+pages[3], etc.
const spreads = computed(() => {
    const result: {
        left: string;
        right: string;
        leftWidth: string;
        rightWidth: string;
    }[] = [];
    const p = pages.value;
    for (let i = 0; i < p.length; i += 2) {
        result.push({
            left: p[i]?.content ?? "",
            right: p[i + 1]?.content ?? "",
            leftWidth: "1",
            rightWidth: "1",
        });
    }
    if (result.length === 0) {
        result.push({
            left: "",
            right: "",
            leftWidth: "1",
            rightWidth: "1",
        });
    }
    return result;
});

const currentSpreadIndex = ref(0);
const currentPageIndex = ref(0);

// Navigation adapts to layout mode
const totalItems = computed(() =>
    layoutMode.value === "book" ? spreads.value.length : pages.value.length,
);
const currentIndex = computed(() =>
    layoutMode.value === "book"
        ? currentSpreadIndex.value
        : currentPageIndex.value,
);
const canGoPrevious = computed(() => currentIndex.value > 0);
const canGoNext = computed(() => currentIndex.value < totalItems.value - 1);

const displaySpread = computed(() => {
    if (layoutMode.value === "book") {
        const spread = spreads.value[currentSpreadIndex.value];
        return (
            spread ?? { left: "", right: "", leftWidth: "1", rightWidth: "1" }
        );
    }
    // Page view: show single page in a spread
    const p = pages.value[currentPageIndex.value];
    return {
        left: p?.content ?? "",
        right: "",
        leftWidth: "1",
        rightWidth: "1",
    };
});

const navigationLabel = computed(() => {
    if (layoutMode.value === "book") {
        return `Spread ${currentSpreadIndex.value + 1} of ${spreads.value.length}`;
    }
    return `Page ${currentPageIndex.value + 1} of ${pages.value.length}`;
});

function goToPrevious() {
    if (!canGoPrevious.value) return;
    if (layoutMode.value === "book") {
        currentSpreadIndex.value--;
    } else {
        currentPageIndex.value--;
    }
}

function goToNext() {
    if (!canGoNext.value) return;
    if (layoutMode.value === "book") {
        currentSpreadIndex.value++;
    } else {
        currentPageIndex.value++;
    }
}

// Sync indices when switching layout modes
watch(layoutMode, (newMode, oldMode) => {
    if (newMode === "page" && oldMode === "book") {
        // Switching to page view: jump to the first page of the current spread
        currentPageIndex.value = currentSpreadIndex.value * 2;
    } else if (newMode === "book" && oldMode === "page") {
        // Switching to book view: jump to the spread containing the current page
        currentSpreadIndex.value = Math.floor(currentPageIndex.value / 2);
    }
});

onMounted(async () => {
    const token = route.params.token as string;
    if (!token) {
        error.value = "Invalid share link.";
        loading.value = false;
        return;
    }

    try {
        const result = await getSharedBook(token);
        if (result) {
            bookTitle.value = result.title;
            bookDescription.value = result.description ?? "";
            pages.value = (result.pages ?? []).sort(
                (a: SnapshotPage, b: SnapshotPage) =>
                    a.page_number - b.page_number,
            );
            loading.value = false;
            await nextTick();
        } else {
            error.value = "This shared book is no longer available.";
            loading.value = false;
        }
    } catch {
        error.value =
            "This shared book was not found or the link has been revoked.";
        loading.value = false;
    }
});
</script>
