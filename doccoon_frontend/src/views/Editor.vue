<template>
    <LoadingScreen :visible="isLoading" />

    <div
        class="flex flex-col h-screen bg-[var(--bg-color)] transition-opacity duration-300"
        :class="{ 'opacity-0': isLoading, 'opacity-100': !isLoading }"
    >
        <!-- Editor Navbar -->
        <EditorNavbar
            :filename="book.filename"
            :is-view-mode="isViewMode"
            :layout-mode="layoutMode"
            :is-diff-mode="isDiffMode"
            :live-preview="livePreview"
            :book-status="book.status"
            @new="handleNewBook"
            @publish-book="handlePublishBook"
            @delete-book="handleDeleteBook"
            @share-book="handleShareBook"
            @add-page="handleAddSpread"
            @delete-page="handleDeletePage"
            @toggle-view="handleToggleView"
            @toggle-layout="handleToggleLayoutMode"
            @toggle-preview="handleTogglePreview"
            @toggle-diff="toggleDiffMode"
            @show-image-gallery="showImageGallery"
            @show-shortcuts="openHelpModal"
        />

        <BookSpread
            :spread="displaySpread"
            :is-view-mode="isViewMode"
            :layout-mode="layoutMode"
            :is-diff-mode="isDiffMode"
            :left-diff-content="leftDiffContent"
            :right-diff-content="rightDiffContent"
            :render-markdown="renderMarkdown"
            :book-id="book.id"
            :live-preview="livePreview"
            @update:spread="updateCurrentSpread"
            @open-page-view="handleOpenPageView"
            @toggle-layout="handleToggleLayoutMode"
            @toggle-preview="handleTogglePreview"
        />

        <FooterControls
            :current-index="currentSpreadIndex"
            :total-pages="totalSpreads"
            :can-go-previous="canGoPrevious"
            :can-go-next="canGoNext"
            :filename="book.filename"
            :status="saveStatus"
            @prev="goToPrevious"
            @next="goToNext"
            @add="handleAddSpread"
            @update:filename="updateFilename"
        />
    </div>

    <Modal
        :visible="modalState.visible"
        :title="modalState.title"
        :message="modalState.message"
        :is-danger="modalState.isDanger"
        @confirm="confirm"
        @cancel="cancel"
    />

    <PageSelectionModal
        :visible="pageSelectionModalVisible"
        title="Select Page to View"
        message="Which page would you like to view in Page View mode?"
        @select-left="handleSelectLeftPage"
        @select-right="handleSelectRightPage"
        @cancel="handleCancelPageSelection"
    />

    <ImageGallery
        :visible="imageGalleryVisible"
        :images="bookImages"
        @close="closeImageGallery"
        @insert-image="handleInsertImage"
    />

    <!-- Share Book Modal -->
    <BaseModal
        :visible="shareModalVisible"
        title="Share Book"
        size="sm"
        @close="closeShareModal"
    >
        <div class="flex flex-col gap-4">
            <div
                v-if="shareLoading"
                class="flex items-center justify-center py-8"
            >
                <div class="text-sm text-[var(--text-color)] opacity-60">
                    Generating share link...
                </div>
            </div>

            <div
                v-else-if="shareError"
                class="flex flex-col items-center gap-3 py-6"
            >
                <p
                    class="text-sm text-[var(--text-color)] opacity-70 m-0 text-center leading-relaxed"
                >
                    {{ shareError }}
                </p>
                <div
                    v-if="shareNeedsPublish"
                    class="flex items-center gap-2 mt-2"
                >
                    <button
                        class="px-4 py-2 text-xs font-medium text-white bg-primary border-none rounded-md cursor-pointer transition-opacity duration-200 hover:opacity-90"
                        @click="handlePublishAndShare"
                    >
                        Publish and Share
                    </button>
                    <button
                        class="px-4 py-2 text-xs font-medium text-[var(--text-color)] bg-[var(--section-alt-bg)] border border-[var(--border-color)] rounded-md cursor-pointer transition-opacity duration-200 hover:opacity-80"
                        @click="closeShareModal"
                    >
                        Cancel
                    </button>
                </div>
            </div>

            <template v-else-if="shareLink">
                <p
                    class="text-sm text-[var(--text-color)] opacity-60 m-0 leading-relaxed"
                >
                    Anyone with the link can view a snapshot of
                    <strong>{{ book.filename }}</strong
                    >.
                </p>

                <div class="flex flex-col gap-2">
                    <button
                        class="w-full flex items-center gap-3 px-4 py-3 text-sm font-medium text-[var(--text-color)] bg-[var(--bg-color)] border border-[var(--border-color)] rounded-lg cursor-pointer transition-all duration-200 hover:border-[#25D366] hover:text-[#25D366] hover:bg-[#25D366]/5"
                        @click="shareVia('whatsapp')"
                    >
                        <svg
                            width="20"
                            height="20"
                            viewBox="0 0 24 24"
                            fill="currentColor"
                        >
                            <path
                                d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"
                            />
                        </svg>
                        Share on WhatsApp
                    </button>

                    <button
                        class="w-full flex items-center gap-3 px-4 py-3 text-sm font-medium text-[var(--text-color)] bg-[var(--bg-color)] border border-[var(--border-color)] rounded-lg cursor-pointer transition-all duration-200 hover:border-[#1877F2] hover:text-[#1877F2] hover:bg-[#1877F2]/5"
                        @click="shareVia('facebook')"
                    >
                        <svg
                            width="20"
                            height="20"
                            viewBox="0 0 24 24"
                            fill="currentColor"
                        >
                            <path
                                d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"
                            />
                        </svg>
                        Share on Facebook
                    </button>

                    <button
                        class="w-full flex items-center gap-3 px-4 py-3 text-sm font-medium text-[var(--text-color)] bg-[var(--bg-color)] border border-[var(--border-color)] rounded-lg cursor-pointer transition-all duration-200 hover:border-[#0088cc] hover:text-[#0088cc] hover:bg-[#0088cc]/5"
                        @click="shareVia('telegram')"
                    >
                        <svg
                            width="20"
                            height="20"
                            viewBox="0 0 24 24"
                            fill="currentColor"
                        >
                            <path
                                d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.479.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"
                            />
                        </svg>
                        Share on Telegram
                    </button>
                </div>

                <div class="border-t border-[var(--border-color)] pt-4">
                    <label
                        class="text-xs font-medium text-[var(--text-color)] opacity-50 mb-2 block"
                    >
                        Book Link
                    </label>
                    <div class="flex gap-2">
                        <input
                            type="text"
                            readonly
                            :value="shareLink"
                            class="flex-1 px-3 py-2 text-xs text-[var(--text-color)] bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md outline-none"
                        />
                        <button
                            class="shrink-0 px-3 py-2 text-xs font-medium text-white bg-primary border-none rounded-md cursor-pointer transition-opacity duration-200 hover:opacity-90 active:opacity-80"
                            @click="copyShareLink"
                        >
                            {{ linkCopied ? "Copied!" : "Copy" }}
                        </button>
                    </div>
                </div>
            </template>
        </div>
    </BaseModal>

    <!-- Keyboard Shortcuts Modal -->
    <KeyboardShortcutsModal
        :visible="isHelpModalOpen"
        :shortcuts="shortcuts"
        @close="closeHelpModal"
    />
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useRoute, useRouter, onBeforeRouteLeave } from "vue-router";
import LoadingScreen from "@/components/LoadingScreen.vue";
import EditorNavbar from "@/components/EditorNavbar.vue";
import BookSpread from "@/components/BookSpread.vue";
import FooterControls from "@/components/Footer/FooterControls.vue";
import Modal from "@/components/Modal.vue";
import PageSelectionModal from "@/components/PageSelectionModal.vue";
import ImageGallery from "@/components/ImageGallery.vue";
import BaseModal from "@/components/ui/BaseModal.vue";
import KeyboardShortcutsModal from "@/components/KeyboardShortcutsModal.vue";

import { useBook } from "@/composables/useBook";
import { useTheme } from "@/composables/useTheme";
import { useViewMode } from "@/composables/useViewMode";
import { useLayoutMode } from "@/composables/useLayoutMode";
import { useStorage } from "@/composables/useStorage";
import { useSettings } from "@/composables/useSettings";
import { useMarkdown } from "@/composables/useMarkdown";
import { useToast } from "@/composables/useToast";
import { useModal } from "@/composables/useModal";
import { useDiff } from "@/composables/useDiff";
import { useBookImages } from "@/composables/useBookImages";
import { useImage } from "@/composables/useImage";
import type { ImageInfo } from "@/composables/useImage";
import { useKeyboardShortcuts } from "@/composables/useKeyboardShortcuts";
import { logger } from "@/utils/logger";
import { isAuthenticated } from "@/api/auth";
import {
    getBooks,
    getBook,
    createBook as createBookApi,
    deleteBook as deleteBookApi,
    togglePublishBook,
} from "@/api/books";
import { deletePage } from "@/api/pages";
import { shareBook as shareBookApi } from "@/api/sharing";

import type { Spread } from "@/types";
import { getExample } from "@/data/examples";

const route = useRoute();
const router = useRouter();

// Track if we're viewing an example (don't auto-save examples)
const isViewingExample = ref(false);

// Auto-save settings come from useSettings (backend)
const disableAutoSave = computed(
    () => isViewingExample.value || !autoSaveEnabled.value,
);
const saveIntervalMs = computed(() => autoSaveInterval.value * 1000);

// Initialize composables
const {
    book,
    currentSpreadIndex,
    currentSpread,
    totalSpreads,
    canGoPrevious,
    canGoNext,
    addSpread,
    deleteSpread,
    updateSpread,
    goToNext,
    goToPrevious,
    generateFilename,
    createNewBook,
} = useBook();

const { isDarkTheme } = useTheme();
const toast = useToast();
const { isViewMode, setViewMode } = useViewMode();
const { layoutMode, toggleLayoutMode, setLayoutMode } = useLayoutMode();
const { saveStatus, debouncedSave } = useStorage(
    book,
    disableAutoSave,
    saveIntervalMs,
);
const { renderMarkdown } = useMarkdown(isDarkTheme);
const { modalState, showModal, confirm, cancel } = useModal();
const { isDiffMode, toggleDiffMode, computeDiff, renderDiffToHtml } = useDiff();
const { getImagesSync } = useBookImages(book);
const { generateImageMarkdown } = useImage();
const {
    shortcuts,
    isHelpModalOpen,
    registerShortcut,
    openHelpModal,
    closeHelpModal,
} = useKeyboardShortcuts();

// Loading state
const isLoading = ref(true);

// Anonymous user state
const isAnonymous = computed(() => !isAuthenticated());

// Anonymous user limits
const MAX_ANONYMOUS_SPREADS = 2;

// Wrapper for addSpread that checks anonymous user limits
async function handleAddSpread() {
    if (isAnonymous.value && totalSpreads.value >= MAX_ANONYMOUS_SPREADS) {
        await showModal({
            title: "Page Limit Reached",
            message: `Guest users can only create up to ${MAX_ANONYMOUS_SPREADS} page spreads. Sign up for a free account to create unlimited pages.`,
            isDanger: false,
        });
        return;
    }
    addSpread();
}

// Track if there are unsaved changes
const hasUnsavedChanges = computed(
    () => saveStatus.value === "Saving..." || saveStatus.value === "Error",
);

// Track which page to show in page view mode ('left' or 'right')
const pageViewSide = ref<"left" | "right">("left");

// Page selection modal state
const pageSelectionModalVisible = ref(false);

// Image gallery state
const imageGalleryVisible = ref(false);
const bookImages = computed(() => getImagesSync());

// Live preview state (from backend settings)
const { livePreview, setLivePreview, autoSaveEnabled, autoSaveInterval } =
    useSettings();
const layoutBeforePreview = ref<"book" | "page">("book");

// Computed spread to display based on layout mode and selected page
const displaySpread = computed(() => {
    const spread = currentSpread.value;
    if (!spread) {
        return {
            left: "",
            right: "",
            leftWidth: "50%",
            rightWidth: "50%",
        };
    }

    if (layoutMode.value === "page") {
        // In page view mode, show only the selected page
        if (pageViewSide.value === "left") {
            return spread;
        } else {
            // Show right page content in the left position
            return {
                ...spread,
                left: spread.right,
                right: "",
            };
        }
    }
    // In book view mode, show both pages normally
    return spread;
});

// Computed diff content for left and right pages
const leftDiffContent = computed(() => {
    if (!isDiffMode.value || !isViewMode.value || layoutMode.value !== "book") {
        return undefined;
    }
    const spread = currentSpread.value;
    if (!spread) return undefined;

    const diff = computeDiff(spread.left, spread.right);
    // Show removed lines on left (content in left but not in right)
    return renderDiffToHtml(diff.left);
});

const rightDiffContent = computed(() => {
    if (!isDiffMode.value || !isViewMode.value || layoutMode.value !== "book") {
        return undefined;
    }
    const spread = currentSpread.value;
    if (!spread) return undefined;

    const diff = computeDiff(spread.left, spread.right);
    // Show added lines on right (content in right but not in left)
    return renderDiffToHtml(diff.right);
});

// Update current spread
function updateCurrentSpread(data: Partial<Spread>) {
    // If in page view mode showing the right page, map the left content to right
    if (
        layoutMode.value === "page" &&
        pageViewSide.value === "right" &&
        data.left !== undefined
    ) {
        updateSpread(currentSpreadIndex.value, { right: data.left });
    } else {
        updateSpread(currentSpreadIndex.value, data);
    }
}

// Handle opening a page in page view mode
function handleOpenPageView(side: "left" | "right") {
    pageViewSide.value = side;
    setLayoutMode("page");
}

// Handle live preview toggle
function handleTogglePreview() {
    if (livePreview.value) {
        // Turn off: restore previous layout
        setLivePreview(false);
        setLayoutMode(layoutBeforePreview.value);
    } else {
        // Turn on: save current layout, force book mode
        layoutBeforePreview.value = layoutMode.value;
        setLivePreview(true);
        setLayoutMode("book");
    }
}

// Restore live preview layout on load
if (livePreview.value) {
    setLayoutMode("book");
}

// Handle layout mode toggle with page selection
function handleToggleLayoutMode() {
    // If currently in book view and switching to page view, show selection modal
    if (layoutMode.value === "book") {
        pageSelectionModalVisible.value = true;
    } else {
        // If currently in page view, just toggle back to book view
        toggleLayoutMode();
    }
}

// Handle page selection modal - Left page
function handleSelectLeftPage() {
    pageViewSide.value = "left";
    pageSelectionModalVisible.value = false;
    setLayoutMode("page");
}

// Handle page selection modal - Right page
function handleSelectRightPage() {
    pageViewSide.value = "right";
    pageSelectionModalVisible.value = false;
    setLayoutMode("page");
}

// Handle page selection modal - Cancel
function handleCancelPageSelection() {
    pageSelectionModalVisible.value = false;
}

// Update filename
function updateFilename(newFilename: string) {
    book.value.filename = newFilename;
}

// Handle new book
async function handleNewBook() {
    const confirmed = await showModal({
        title: "Create New Book",
        message:
            "Are you sure you want to create a new book? All current content will be lost.",
        isDanger: false,
    });

    if (confirmed) {
        createNewBook();

        // Create on backend if authenticated
        if (isAuthenticated()) {
            try {
                const created = await createBookApi({
                    title: book.value.filename,
                    year: new Date().getFullYear(),
                });
                if (created) {
                    book.value.id = created.id;
                    router.replace({
                        path: route.path,
                        query: { book: String(created.id) },
                    });
                    // Explicitly save to create initial pages on backend
                    debouncedSave();
                }
            } catch {
                // Continue with local-only book if backend fails
            }
        }
    }
}

// Handle delete page
async function handleDeletePage() {
    if (totalSpreads.value === 1) {
        await showModal({
            title: "Cannot Delete",
            message: "You cannot delete the last page spread.",
            isDanger: false,
        });
        return;
    }

    const confirmed = await showModal({
        title: "Delete Page Spread",
        message: "Are you sure you want to delete this page spread?",
        isDanger: true,
    });

    if (confirmed) {
        // Delete pages from backend if they have IDs
        const spread = currentSpread.value;
        if (isAuthenticated() && book.value.id && spread) {
            try {
                if (spread.leftPageId) {
                    await deletePage(book.value.id, spread.leftPageId);
                }
                if (spread.rightPageId) {
                    await deletePage(book.value.id, spread.rightPageId);
                }
            } catch {
                // Continue with local delete
            }
        }
        deleteSpread(currentSpreadIndex.value);
    }
}

// Handle delete book
async function handleDeleteBook() {
    const confirmed = await showModal({
        title: "Delete Book",
        message:
            "Are you sure you want to delete the entire book? This action cannot be undone.",
        isDanger: true,
    });

    if (confirmed) {
        // Delete from backend if it has an ID
        if (isAuthenticated() && book.value.id) {
            try {
                await deleteBookApi(book.value.id);
            } catch {
                // Continue even if backend fails
            }
        }

        // Load another book or prompt to create one
        if (isAuthenticated()) {
            try {
                const books = await getBooks();
                const firstBook = books[0];
                if (firstBook) {
                    await loadBookFromBackend(firstBook.id);
                    router.replace({
                        path: route.path,
                        query: { book: String(firstBook.id) },
                    });
                    return;
                }
            } catch {
                // Fall through to create new
            }
            // No books left - prompt to create
            await promptCreateFirstBook();
        } else {
            createNewBook();
            router.replace({ path: route.path, query: {} });
        }
    }
}

// Image Gallery functions
function showImageGallery() {
    imageGalleryVisible.value = true;
}

function closeImageGallery() {
    imageGalleryVisible.value = false;
}

function handleInsertImage(image: ImageInfo) {
    // Insert image into the current page
    const spread = currentSpread.value;
    if (!spread) return;

    const markdown = generateImageMarkdown(image);

    // Insert at the end of the left page (or right page if in page view showing right)
    if (layoutMode.value === "page" && pageViewSide.value === "right") {
        spread.right += "\n\n" + markdown;
    } else {
        spread.left += "\n\n" + markdown;
    }

    updateCurrentSpread(spread);
    closeImageGallery();
}

// ── Share Book ────────────────────────────────────────────────────────
const shareModalVisible = ref(false);
const shareLoading = ref(false);
const shareError = ref("");
const shareNeedsPublish = ref(false);
const shareLink = ref("");
const linkCopied = ref(false);

const shareMessage =
    "This book was written on Doccoon editor. View it by clicking on the link below!";

async function handlePublishBook() {
    if (!isAuthenticated() || !book.value.id) {
        toast.error("Please save the book to your account first.");
        return;
    }

    const isPublished = book.value.status === "Published";
    const confirmed = await showModal({
        title: isPublished ? "Unpublish Book" : "Publish Book",
        message: isPublished
            ? "This will revert the book to draft status. Existing share links will stop working."
            : "Publishing makes the book available for sharing. You can unpublish at any time.",
        isDanger: isPublished,
    });

    if (!confirmed) return;

    try {
        const result = await togglePublishBook(book.value.id);
        if (result) {
            book.value.status = result.status;
            toast.success(
                result.status === "Published"
                    ? "Book published successfully."
                    : "Book unpublished successfully.",
            );
        }
    } catch (err: unknown) {
        const error = err as { message?: string };
        logger.error("Publish book error:", error);
        toast.error(error.message || "Failed to update book status.");
    }
}

async function handleShareBook() {
    if (!isAuthenticated() || !book.value.id) {
        await showModal({
            title: "Cannot Share",
            message: "Please save the book to your account before sharing.",
            isDanger: false,
        });
        return;
    }

    shareLink.value = "";
    shareError.value = "";
    shareNeedsPublish.value = false;
    shareLoading.value = true;
    shareModalVisible.value = true;

    try {
        const result = await shareBookApi(book.value.id);
        if (result?.share_token) {
            shareLink.value = `${window.location.origin}/shared/book/${result.share_token}`;
        } else {
            shareError.value = "Failed to generate share link.";
        }
    } catch (err: unknown) {
        const error = err as { message?: string };
        logger.error("Share book error:", error);
        const msg = error.message || "Failed to share book. Please try again.";
        if (msg.toLowerCase().includes("publish")) {
            shareNeedsPublish.value = true;
            shareError.value =
                "This book must be published before it can be shared.";
        } else {
            shareError.value = msg;
        }
    } finally {
        shareLoading.value = false;
    }
}

async function handlePublishAndShare() {
    if (!book.value.id) return;

    shareLoading.value = true;
    shareError.value = "";
    shareNeedsPublish.value = false;

    try {
        const result = await togglePublishBook(book.value.id);
        if (result) {
            book.value.status = result.status;
        }
        // Now share
        const shareResult = await shareBookApi(book.value.id);
        if (shareResult?.share_token) {
            shareLink.value = `${window.location.origin}/shared/book/${shareResult.share_token}`;
        } else {
            shareError.value =
                "Book published, but failed to generate share link.";
        }
    } catch (err: unknown) {
        const error = err as { message?: string };
        logger.error("Publish and share error:", error);
        shareError.value = error.message || "Failed to publish and share book.";
    } finally {
        shareLoading.value = false;
    }
}

function closeShareModal() {
    shareModalVisible.value = false;
    shareLink.value = "";
    shareError.value = "";
    shareNeedsPublish.value = false;
    linkCopied.value = false;
}

function shareVia(platform: "whatsapp" | "facebook" | "telegram") {
    if (!shareLink.value) return;
    const text = `${shareMessage}\n${shareLink.value}`;
    let url = "";

    switch (platform) {
        case "whatsapp":
            url = `https://wa.me/?text=${encodeURIComponent(text)}`;
            break;
        case "facebook":
            url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareLink.value)}&quote=${encodeURIComponent(shareMessage)}`;
            break;
        case "telegram":
            url = `https://t.me/share/url?url=${encodeURIComponent(shareLink.value)}&text=${encodeURIComponent(shareMessage)}`;
            break;
    }

    window.open(url, "_blank", "noopener,noreferrer");
}

async function copyShareLink() {
    if (!shareLink.value) return;
    try {
        await navigator.clipboard.writeText(shareLink.value);
        linkCopied.value = true;
        setTimeout(() => {
            linkCopied.value = false;
        }, 2000);
    } catch (err) {
        logger.error("Failed to copy link:", err);
    }
}

// Load a book from the backend by ID
async function loadBookFromBackend(bookId: number): Promise<boolean> {
    try {
        const data = await getBook(bookId);
        if (!data) return false;

        const pages = data.pages.sort((a, b) => a.page_number - b.page_number);

        // Convert pages into spreads (2 pages per spread)
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

// Prompt user to create their first book
async function promptCreateFirstBook() {
    const confirmed = await showModal({
        title: "Create Your First Book",
        message: "You don't have any books yet. Would you like to create one?",
        isDanger: false,
    });

    if (confirmed) {
        createNewBook();
        try {
            const created = await createBookApi({
                title: book.value.filename,
                year: new Date().getFullYear(),
            });
            if (created) {
                book.value.id = created.id;
                router.replace({
                    path: route.path,
                    query: { book: String(created.id) },
                });
                // Explicitly save to create initial pages on backend
                debouncedSave();
            }
        } catch {
            // Continue with local-only book
        }
    }
}

// Initialize app
async function init() {
    // Check if we have an example in the URL query parameter
    const exampleKey = route.query.example as string | undefined;

    if (exampleKey) {
        // Try to load from predefined examples first (simple key like "typescript", "flowchart")
        const predefinedExample = getExample(exampleKey);

        if (predefinedExample) {
            book.value = { ...predefinedExample };
            isViewingExample.value = true;

            // Check if diff mode should be enabled (for diff example)
            const diffParam = route.query.diff as string | undefined;
            if (diffParam === "true" || exampleKey === "diff") {
                // Enable diff mode: view mode + diff mode + book layout
                setViewMode(true);
                isDiffMode.value = true;
                setLayoutMode("book");
            } else {
                // Enable live preview mode (left pane edit, right pane preview)
                setLivePreview(true);
                setLayoutMode("book");
            }
            // Show loading screen briefly
            await new Promise((resolve) => setTimeout(resolve, 500));
            isLoading.value = false;
            return;
        }

        // Fall back to base64 encoded data for backwards compatibility
        try {
            const decodedData = decodeURIComponent(atob(exampleKey));
            const exampleBook = JSON.parse(decodedData);
            book.value = exampleBook;
            isViewingExample.value = true;
            // Enable live preview mode (left pane edit, right pane preview)
            setLivePreview(true);
            setLayoutMode("book");
            // Show loading screen briefly
            await new Promise((resolve) => setTimeout(resolve, 500));
            isLoading.value = false;
            return;
        } catch (error) {
            logger.error("Failed to load example data:", error);
            // Fall through to load saved book
        }
    }

    isViewingExample.value = false;

    // Auto-save settings are now loaded reactively via useSettings composable

    // Check if we should create a new book
    const newBookParam = route.query.new as string | undefined;
    if (newBookParam === "true" && isAuthenticated()) {
        // Create a new book immediately
        createNewBook();
        try {
            const created = await createBookApi({
                title: book.value.filename,
                year: new Date().getFullYear(),
            });
            if (created) {
                book.value.id = created.id;
                router.replace({
                    path: route.path,
                    query: { book: String(created.id) },
                });
                debouncedSave();
            }
        } catch {
            // Continue with local-only book
        }
        await new Promise((resolve) => setTimeout(resolve, 500));
        isLoading.value = false;
        return;
    }

    // Check if we should load a specific book from the backend
    const bookIdParam = route.query.book as string | undefined;
    if (bookIdParam && isAuthenticated()) {
        const bookId = parseInt(bookIdParam, 10);
        if (!isNaN(bookId)) {
            const loaded = await loadBookFromBackend(bookId);
            if (loaded) {
                await new Promise((resolve) => setTimeout(resolve, 500));
                isLoading.value = false;
                return;
            }
        }
    }

    // No specific book requested - check for existing books or prompt to create
    if (isAuthenticated()) {
        try {
            const books = await getBooks();
            const firstBook = books[0];
            if (firstBook) {
                // Load the most recently modified book
                const loaded = await loadBookFromBackend(firstBook.id);
                if (loaded) {
                    router.replace({
                        path: route.path,
                        query: { book: String(firstBook.id) },
                    });
                    await new Promise((resolve) => setTimeout(resolve, 500));
                    isLoading.value = false;
                    return;
                }
            }
        } catch {
            // Fall through to prompt
        }

        // No books exist - hide loading first, then prompt
        isLoading.value = false;
        await promptCreateFirstBook();
        return;
    }

    // Not authenticated - allow in-memory editing
    book.value.filename = generateFilename();

    // Wait a bit to show loading screen
    await new Promise((resolve) => setTimeout(resolve, 500));
    isLoading.value = false;
}

// Handle toggle view - change route instead of just toggling state
function handleToggleView() {
    if (isViewMode.value) {
        // Currently in view mode, switch to edit mode
        router.push("/edit");
    } else {
        // Currently in edit mode, switch to view mode
        router.push("/view");
    }
}

// Apply view mode based on route
function applyRouteViewMode() {
    const defaultViewMode = route.meta.defaultViewMode as boolean | undefined;

    if (defaultViewMode !== undefined) {
        // Set view mode based on route meta using the composable
        setViewMode(defaultViewMode);
    } else {
        // For /edit route, use setting from backend (via useViewMode which uses useSettings)
        // The viewMode is already loaded from settings, no localStorage needed
        // Default to edit mode (false) if not explicitly set
        setViewMode(isViewMode.value);
    }
}

// Watch for route changes
watch(
    () => route.path,
    () => {
        applyRouteViewMode();
    },
);

// ── Unsaved Changes Warning ───────────────────────────────────────────
function handleBeforeUnload(e: BeforeUnloadEvent) {
    if (hasUnsavedChanges.value && !isViewingExample.value) {
        e.preventDefault();
        // Modern browsers ignore custom messages, but we still need to set returnValue
        e.returnValue =
            "You have unsaved changes. Are you sure you want to leave?";
        return e.returnValue;
    }
}

// Navigation guard for Vue Router
onBeforeRouteLeave(async (_to, _from) => {
    if (hasUnsavedChanges.value && !isViewingExample.value) {
        const confirmed = await showModal({
            title: "Unsaved Changes",
            message:
                "You have unsaved changes. Are you sure you want to leave? Your changes will be lost.",
            isDanger: true,
        });
        if (!confirmed) {
            return false; // Cancel navigation
        }
    }
    return true;
});

// ── Keyboard Shortcuts ────────────────────────────────────────────────
function registerKeyboardShortcuts() {
    // Help modal
    registerShortcut({
        key: "?",
        ctrl: true,
        description: "Show keyboard shortcuts",
        category: "general",
        action: openHelpModal,
    });

    // Save
    registerShortcut({
        key: "s",
        ctrl: true,
        description: "Save changes",
        category: "general",
        action: () => {
            if (isViewingExample.value) return;

            if (isAnonymous.value) {
                toast.error("Please log in to save your work.");
                return;
            }

            debouncedSave();
            toast.success("Saving...");
        },
    });

    // New book
    registerShortcut({
        key: "n",
        ctrl: true,
        shift: true,
        description: "Create new book",
        category: "general",
        action: handleNewBook,
    });

    // Navigation
    registerShortcut({
        key: "ArrowLeft",
        ctrl: true,
        description: "Previous page",
        category: "navigation",
        action: () => {
            if (canGoPrevious.value) goToPrevious();
        },
    });

    registerShortcut({
        key: "ArrowRight",
        ctrl: true,
        description: "Next page",
        category: "navigation",
        action: () => {
            if (canGoNext.value) goToNext();
        },
    });

    // Add page
    registerShortcut({
        key: "Enter",
        ctrl: true,
        shift: true,
        description: "Add new page",
        category: "navigation",
        action: handleAddSpread,
    });

    // View mode toggle
    registerShortcut({
        key: "e",
        ctrl: true,
        description: "Toggle edit/view mode",
        category: "view",
        action: handleToggleView,
    });

    // Layout toggle
    registerShortcut({
        key: "l",
        ctrl: true,
        description: "Toggle book/page layout",
        category: "view",
        action: handleToggleLayoutMode,
    });

    // Live preview toggle
    registerShortcut({
        key: "p",
        ctrl: true,
        description: "Toggle live preview",
        category: "view",
        action: handleTogglePreview,
    });

    // Diff mode toggle
    registerShortcut({
        key: "d",
        ctrl: true,
        shift: true,
        description: "Toggle diff mode",
        category: "view",
        action: toggleDiffMode,
    });

    // Escape to close modals
    registerShortcut({
        key: "Escape",
        description: "Close modal/dialog",
        category: "general",
        action: () => {
            if (isHelpModalOpen.value) {
                closeHelpModal();
            } else if (shareModalVisible.value) {
                closeShareModal();
            } else if (imageGalleryVisible.value) {
                closeImageGallery();
            }
        },
    });

    // Text formatting shortcuts (handled by BookPage, but listed here for help modal)
    registerShortcut({
        key: "b",
        ctrl: true,
        description: "Bold text",
        category: "editing",
        action: () => {}, // Handled by BookPage
    });

    registerShortcut({
        key: "i",
        ctrl: true,
        description: "Italic text",
        category: "editing",
        action: () => {}, // Handled by BookPage
    });

    registerShortcut({
        key: "k",
        ctrl: true,
        description: "Insert link",
        category: "editing",
        action: () => {}, // Handled by BookPage
    });

    registerShortcut({
        key: "`",
        ctrl: true,
        description: "Inline code",
        category: "editing",
        action: () => {}, // Handled by BookPage
    });

    registerShortcut({
        key: "`",
        ctrl: true,
        shift: true,
        description: "Code block",
        category: "editing",
        action: () => {}, // Handled by BookPage
    });

    registerShortcut({
        key: "1",
        ctrl: true,
        shift: true,
        description: "Heading 1",
        category: "editing",
        action: () => {}, // Handled by BookPage
    });

    registerShortcut({
        key: "2",
        ctrl: true,
        shift: true,
        description: "Heading 2",
        category: "editing",
        action: () => {}, // Handled by BookPage
    });

    registerShortcut({
        key: "3",
        ctrl: true,
        shift: true,
        description: "Heading 3",
        category: "editing",
        action: () => {}, // Handled by BookPage
    });

    registerShortcut({
        key: "u",
        ctrl: true,
        shift: true,
        description: "Bullet list",
        category: "editing",
        action: () => {}, // Handled by BookPage
    });

    registerShortcut({
        key: "o",
        ctrl: true,
        shift: true,
        description: "Numbered list",
        category: "editing",
        action: () => {}, // Handled by BookPage
    });

    registerShortcut({
        key: "'",
        ctrl: true,
        shift: true,
        description: "Block quote",
        category: "editing",
        action: () => {}, // Handled by BookPage
    });
}

onMounted(() => {
    // Apply view mode based on route
    applyRouteViewMode();

    // Register keyboard shortcuts
    registerKeyboardShortcuts();

    // Add beforeunload listener for browser close/refresh
    window.addEventListener("beforeunload", handleBeforeUnload);

    init();
});

onUnmounted(() => {
    window.removeEventListener("beforeunload", handleBeforeUnload);
});
</script>
