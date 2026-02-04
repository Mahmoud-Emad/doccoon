<template>
    <div
        class="flex flex-col h-screen bg-[var(--bg-color)] text-[var(--text-color)]"
    >
        <!-- Header -->
        <div
            class="flex items-center justify-between px-6 py-4 bg-primary text-white shadow-md"
        >
            <BaseButton
                variant="ghost"
                size="sm"
                class="!border-white/20 !text-white hover:!bg-white/20"
                @click="goHome"
            >
                <BaseIcon name="chevron-left" :size="20" />
                Back to Home
            </BaseButton>

            <div class="text-lg font-semibold">
                {{ book.filename || "Untitled Book" }}
            </div>

            <BaseButton
                variant="ghost"
                size="sm"
                icon
                class="!border-white/20 !text-white hover:!bg-white/20"
                @click="toggleTheme"
            >
                <BaseIcon :name="isDarkTheme ? 'moon' : 'sun'" :size="20" />
            </BaseButton>
        </div>

        <!-- Page Content -->
        <div class="flex-1 overflow-y-auto py-10 px-5">
            <div
                v-if="!pageExists"
                class="max-w-[600px] mx-auto mt-24 text-center"
            >
                <h2 class="text-3xl font-bold mb-4 text-[var(--text-color)]">
                    Page Not Found
                </h2>
                <p class="text-lg mb-8 text-[var(--text-color)] opacity-70">
                    The requested page does not exist in this book.
                </p>
                <BaseButton variant="primary" size="lg" @click="goToPage(1)"
                    >Go to First Page</BaseButton
                >
            </div>

            <div v-else class="max-w-[800px] mx-auto">
                <div
                    ref="pageRef"
                    class="bg-[var(--page-bg)] border border-[var(--border-color)] rounded-lg p-10 min-h-[400px] shadow-md font-sans text-base leading-relaxed text-[var(--text-color)] page-view"
                ></div>
            </div>
        </div>

        <!-- Footer Controls -->
        <FooterControls
            :current-index="currentSpreadIndex"
            :total-pages="totalSpreads"
            :can-go-previous="canGoPrevious"
            :can-go-next="canGoNext"
            :filename="book.filename"
            status="Loaded"
            @prev="previousPage"
            @next="nextPage"
            @add="() => {}"
            @update:filename="() => {}"
        />
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useBook } from "@/composables/useBook";
import { useTheme } from "@/composables/useTheme";
import { useMarkdown } from "@/composables/useMarkdown";
import { getBook } from "@/api/books";
import { isAuthenticated } from "@/api/auth";
import { logger } from "@/utils/logger";
import BaseButton from "@/components/ui/BaseButton.vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import FooterControls from "@/components/Footer/FooterControls.vue";
import type { Spread } from "@/types";

const route = useRoute();
const router = useRouter();

// Initialize composables
const { book } = useBook();
const { isDarkTheme, toggleTheme } = useTheme();
const { renderMarkdown } = useMarkdown(isDarkTheme);

// Page reference
const pageRef = ref<HTMLElement>();

// Get current page from query parameter
const currentPage = computed(() => {
    const page = parseInt((route.query.page as string) || "1");
    return isNaN(page) || page < 1 ? 1 : page;
});

// Calculate total pages (each spread has 2 pages)
const totalPages = computed(() => {
    return book.value.spreads.length * 2;
});

// Spread-based navigation for FooterControls
const currentSpreadIndex = computed(() => {
    return Math.floor((currentPage.value - 1) / 2);
});

const totalSpreads = computed(() => {
    return book.value.spreads.length;
});

const canGoPrevious = computed(() => currentPage.value > 1);
const canGoNext = computed(() => currentPage.value < totalPages.value);

// Check if page exists
const pageExists = computed(() => {
    return currentPage.value <= totalPages.value;
});

// Get page content
const pageContent = computed(() => {
    if (!pageExists.value) return "";

    const spreadIndex = Math.floor((currentPage.value - 1) / 2);
    const isLeftPage = (currentPage.value - 1) % 2 === 0;

    const spread = book.value.spreads[spreadIndex];
    if (!spread) return "";

    return isLeftPage ? spread.left : spread.right;
});

// Navigation functions
function goHome() {
    router.push("/");
}

function goToPage(page: number) {
    router.push({ path: "/view", query: { page: page.toString() } });
}

function previousPage() {
    if (currentPage.value > 1) {
        goToPage(currentPage.value - 1);
    }
}

function nextPage() {
    if (currentPage.value < totalPages.value) {
        goToPage(currentPage.value + 1);
    }
}

// Load book from backend
async function loadBookFromBackend(bookId: number): Promise<boolean> {
    try {
        const data = await getBook(bookId);
        if (!data) return false;

        const pages = data.pages.sort((a, b) => a.page_number - b.page_number);

        const spreads: Spread[] = [];
        for (let i = 0; i < pages.length; i += 2) {
            const left = pages[i];
            const right = pages[i + 1];
            spreads.push({
                left: left?.content ?? "",
                right: right?.content ?? "",
                leftWidth: "1",
                rightWidth: "1",
                leftPageId: left?.id,
                rightPageId: right?.id,
            });
        }

        if (spreads.length === 0) {
            spreads.push({
                left: "",
                right: "",
                leftWidth: "1",
                rightWidth: "1",
            });
        }

        book.value = {
            id: data.id,
            filename: data.title,
            status: data.status,
            spreads,
        };

        return true;
    } catch (err) {
        logger.error("Failed to load book from backend:", err);
        return false;
    }
}

// Render markdown when page changes
async function renderPage() {
    if (pageRef.value && pageExists.value) {
        await nextTick();
        await renderMarkdown(pageContent.value, pageRef.value);
    }
}

// Watch for page changes
watch([currentPage, pageContent], () => {
    renderPage();
});

// Initialize
onMounted(async () => {
    // Try to load book from query parameter
    const bookIdParam = route.query.book as string | undefined;
    if (bookIdParam && isAuthenticated()) {
        const bookId = parseInt(bookIdParam, 10);
        if (!isNaN(bookId)) {
            await loadBookFromBackend(bookId);
        }
    }

    // Render initial page
    renderPage();
});
</script>
