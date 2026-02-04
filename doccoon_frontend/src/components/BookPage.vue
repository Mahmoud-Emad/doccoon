<template>
    <div
        class="bg-[var(--page-bg)] px-4 md:px-6 lg:px-10 pt-1.5 pb-12 relative h-full transition-colors duration-300 page flex flex-col"
        :class="[
            side === 'left' ? 'border-r border-[var(--border-color)]' : '',
            layoutMode === 'page' ? 'max-w-full w-full flex-1' : '',
            isViewMode ? 'overflow-y-auto' : 'overflow-hidden',
        ]"
        :style="{ flex: width }"
    >
        <!-- Action Buttons - Only in Edit Mode -->
        <div
            v-if="!isViewMode"
            class="flex items-center gap-0.5 px-1.5 py-1 border-b border-[var(--border-color)] bg-[var(--page-bg)] relative mb-1"
            :class="{ 'opacity-50 pointer-events-none': aiLoading }"
        >
            <!-- Group 1: Content actions -->
            <BaseTooltip text="Copy content" position="bottom">
                <button
                    class="p-1.5 rounded text-[var(--text-color)] cursor-pointer transition-all duration-150 hover:bg-[var(--section-alt-bg)] hover:text-primary active:scale-95 relative"
                    @click="copyContent"
                >
                    <BaseIcon name="copy" :size="16" />
                    <div
                        v-if="showCopyTooltip"
                        class="absolute top-[calc(100%+8px)] left-1/2 -translate-x-1/2 bg-primary text-white px-3 py-1.5 rounded text-xs whitespace-nowrap pointer-events-none shadow-md z-10 animate-fade-in"
                    >
                        Copied!
                    </div>
                </button>
            </BaseTooltip>
            <BaseTooltip text="Insert image" position="bottom">
                <button
                    class="p-1.5 rounded text-[var(--text-color)] cursor-pointer transition-all duration-150 hover:bg-[var(--section-alt-bg)] hover:text-primary active:scale-95 relative"
                    @click="triggerImageUpload"
                >
                    <BaseIcon name="image" :size="16" />
                    <div
                        v-if="uploadProgress > 0 && uploadProgress < 100"
                        class="absolute bottom-0 left-0 right-0 h-0.5 bg-[rgba(0,122,204,0.1)] overflow-hidden"
                    >
                        <div
                            class="h-full bg-primary transition-[width] duration-300"
                            :style="{ width: uploadProgress + '%' }"
                        />
                    </div>
                </button>
            </BaseTooltip>
            <BaseTooltip text="Clear content" position="bottom">
                <button
                    class="p-1.5 rounded text-[var(--text-color)] cursor-pointer transition-all duration-150 hover:bg-[var(--section-alt-bg)] hover:text-primary active:scale-95"
                    @click="clearContent"
                >
                    <BaseIcon name="trash" :size="16" />
                </button>
            </BaseTooltip>

            <!-- Separator -->
            <div class="w-px h-4 bg-[var(--border-color)] opacity-50 mx-0.5" />

            <!-- Group 2: View actions -->
            <BaseTooltip
                v-if="!livePreview"
                :text="layoutMode === 'page' ? 'Book view' : 'Page view'"
                position="bottom"
            >
                <button
                    class="p-1.5 rounded text-[var(--text-color)] cursor-pointer transition-all duration-150 hover:bg-[var(--section-alt-bg)] hover:text-primary active:scale-95"
                    @click="openInPageView"
                >
                    <BaseIcon name="layout" :size="16" />
                </button>
            </BaseTooltip>
            <BaseTooltip
                :text="livePreview ? 'Close preview' : 'Live preview'"
                position="bottom"
            >
                <button
                    class="p-1.5 rounded text-[var(--text-color)] cursor-pointer transition-all duration-150 hover:bg-[var(--section-alt-bg)] hover:text-primary active:scale-95"
                    :class="{
                        'bg-primary/10 text-primary': livePreview,
                    }"
                    @click="emit('toggle-preview')"
                >
                    <BaseIcon name="columns" :size="16" />
                </button>
            </BaseTooltip>

            <!-- Separator (hidden for anonymous users) -->
            <div
                v-if="!isAnonymous"
                class="w-px h-4 bg-[var(--border-color)] opacity-50 mx-0.5"
            />

            <!-- Group 3: AI & Share (hidden for anonymous users) -->
            <div v-if="!isAnonymous" class="relative" ref="aiDropdownRef">
                <BaseTooltip text="AI refine" position="bottom">
                    <button
                        class="p-1.5 rounded text-[var(--text-color)] cursor-pointer transition-all duration-150 hover:bg-[var(--section-alt-bg)] hover:text-primary active:scale-95 flex items-center gap-0.5"
                        @click="aiDropdownOpen = !aiDropdownOpen"
                    >
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
                            <path
                                d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"
                            />
                        </svg>
                        <svg
                            width="10"
                            height="10"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2.5"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        >
                            <polyline points="6 9 12 15 18 9" />
                        </svg>
                    </button>
                </BaseTooltip>
                <Transition
                    enter-active-class="transition ease-out duration-100"
                    enter-from-class="opacity-0 scale-95"
                    enter-to-class="opacity-100 scale-100"
                    leave-active-class="transition ease-in duration-75"
                    leave-from-class="opacity-100 scale-100"
                    leave-to-class="opacity-0 scale-95"
                >
                    <div
                        v-if="aiDropdownOpen"
                        class="absolute top-full left-0 mt-1 bg-[var(--page-bg)] border border-[var(--border-color)] rounded-md shadow-[0_4px_12px_rgba(0,0,0,0.15)] z-[100] min-w-[180px] p-1"
                    >
                        <button
                            class="w-full flex items-center gap-2.5 px-3 py-2 text-xs text-[var(--text-color)] bg-transparent border-none rounded cursor-pointer transition-colors duration-150 hover:bg-primary/10 hover:text-primary text-left"
                            @click="handleAiAction('refine')"
                        >
                            <svg
                                width="14"
                                height="14"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                            >
                                <path d="M12 20h9" />
                                <path
                                    d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"
                                />
                            </svg>
                            <div>
                                <div class="font-medium">Refine</div>
                                <div class="text-[10px] opacity-50 mt-0.5">
                                    Improve grammar, tone &amp; clarity
                                </div>
                            </div>
                        </button>
                        <button
                            class="w-full flex items-center gap-2.5 px-3 py-2 text-xs text-[var(--text-color)] bg-transparent border-none rounded cursor-pointer transition-colors duration-150 hover:bg-primary/10 hover:text-primary text-left"
                            @click="handleAiAction('rewrite')"
                        >
                            <svg
                                width="14"
                                height="14"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                            >
                                <polyline points="1 4 1 10 7 10" />
                                <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" />
                            </svg>
                            <div>
                                <div class="font-medium">Rewrite</div>
                                <div class="text-[10px] opacity-50 mt-0.5">
                                    Regenerate the content entirely
                                </div>
                            </div>
                        </button>
                    </div>
                </Transition>
            </div>
            <BaseTooltip
                v-if="!isAnonymous"
                text="Share page"
                position="bottom"
            >
                <button
                    class="p-1.5 rounded text-[var(--text-color)] cursor-pointer transition-all duration-150 hover:bg-[var(--section-alt-bg)] hover:text-primary active:scale-95"
                    @click="openShareDialog"
                >
                    <BaseIcon name="share" :size="16" />
                </button>
            </BaseTooltip>
        </div>

        <!-- Hidden file input for image upload -->
        <input
            ref="fileInputRef"
            type="file"
            accept="image/png,image/jpeg,image/jpg,image/gif,image/svg+xml,image/webp"
            multiple
            class="hidden"
            @change="handleFileSelect"
        />

        <div class="relative w-full flex-1 min-h-0">
            <!-- Edit Mode: Textarea with Line Numbers -->
            <div
                v-if="!isViewMode"
                class="flex h-full relative overflow-hidden"
            >
                <div
                    ref="lineNumbersRef"
                    class="shrink-0 w-[50px] bg-[var(--page-bg)] border-r border-[var(--border-color)] overflow-hidden select-none text-right text-base leading-[1.6] text-[var(--text-color)] opacity-35"
                >
                    <div
                        v-for="(height, i) in lineHeights"
                        :key="i"
                        class="pr-2 pl-1 box-border"
                        :style="{ height: height + 'px' }"
                    >
                        {{ i + 1 }}
                    </div>
                </div>
                <!-- Hidden mirror for measuring wrapped line heights -->
                <pre
                    ref="mirrorRef"
                    aria-hidden="true"
                    class="absolute -left-[9999px] top-0 pl-3 text-base leading-[1.6] whitespace-pre-wrap break-words border-none m-0 p-0 overflow-hidden"
                    style="visibility: hidden; pointer-events: none"
                />
                <textarea
                    ref="textareaRef"
                    class="flex-1 pl-3 border-none outline-none bg-transparent text-base leading-[1.6] text-[var(--text-color)] resize-none transition-all duration-200 w-full h-full break-words overflow-y-auto placeholder:text-[var(--placeholder-color)] placeholder:opacity-100"
                    :class="{
                        'border-2 border-dashed !border-primary !bg-[rgba(0,122,204,0.05)]':
                            isDragging,
                        'opacity-50 cursor-not-allowed': aiLoading,
                    }"
                    :value="displayContent"
                    :disabled="aiLoading"
                    :placeholder="`Start writing on the ${side} page...`"
                    @input="onInput"
                    @keydown="handleTextareaKeydown"
                    @scroll="syncScroll"
                    @dragover="onDragOver"
                    @dragleave="onDragLeave"
                    @drop="onDrop"
                    @focus="onFocus"
                    @blur="onBlur"
                />

                <!-- AI Loading Overlay -->
                <div
                    v-if="aiLoading"
                    class="absolute inset-0 flex items-center justify-center bg-[var(--page-bg)]/60 z-10"
                >
                    <div
                        class="flex items-center gap-2.5 px-4 py-2.5 rounded-lg bg-[var(--bg-color)] border border-[var(--border-color)] shadow-sm"
                    >
                        <svg
                            class="animate-spin h-4 w-4 text-primary"
                            viewBox="0 0 24 24"
                            fill="none"
                        >
                            <circle
                                class="opacity-25"
                                cx="12"
                                cy="12"
                                r="10"
                                stroke="currentColor"
                                stroke-width="4"
                            />
                            <path
                                class="opacity-75"
                                fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                            />
                        </svg>
                        <span
                            class="text-xs font-medium text-[var(--text-color)]"
                        >
                            AI is processing...
                        </span>
                    </div>
                </div>
            </div>

            <!-- View Mode: Rendered Markdown or Diff -->
            <div
                v-if="isViewMode"
                ref="viewRef"
                class="page-view w-full min-h-full text-base leading-[1.6] text-[var(--text-color)]"
                :class="{ 'font-mono text-sm leading-[1.6]': isDiffMode }"
            />
        </div>

        <!-- Share Dialog -->
        <BaseModal
            :visible="showShareDialog"
            title="Share Page"
            size="sm"
            @close="
                showShareDialog = false;
                shareLink = '';
                shareError = '';
            "
        >
            <div class="flex flex-col gap-4">
                <!-- Loading state -->
                <div
                    v-if="shareLoading"
                    class="flex items-center justify-center py-8"
                >
                    <div class="text-sm text-[var(--text-color)] opacity-60">
                        Generating share link...
                    </div>
                </div>

                <!-- Error state -->
                <div
                    v-else-if="shareError"
                    class="flex flex-col items-center gap-3 py-6"
                >
                    <p
                        class="text-sm text-red-500 m-0 text-center leading-relaxed"
                    >
                        {{ shareError }}
                    </p>
                    <button
                        class="px-4 py-2 text-xs font-medium text-white bg-primary border-none rounded-md cursor-pointer transition-opacity duration-200 hover:opacity-90"
                        @click="generateShareLink"
                    >
                        Try Again
                    </button>
                </div>

                <!-- Share options -->
                <template v-else-if="shareLink">
                    <p
                        class="text-sm text-[var(--text-color)] opacity-60 m-0 leading-relaxed"
                    >
                        This page will be visible to anyone who has the link.
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
                            Page Link
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
    </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, computed, onMounted, onUnmounted } from "vue";
import { useDragDrop } from "@/composables/useDragDrop";
import { useImage } from "@/composables/useImage";
import { useClickOutside } from "@/composables/useClickOutside";
import { useTextFormatting } from "@/composables/useKeyboardShortcuts";
import { logger } from "@/utils/logger";
import { isAuthenticated } from "@/api/auth";
import { refineContent } from "@/api/ai";
import { sharePage as sharePageApi } from "@/api/sharing";
import { useToast } from "@/composables/useToast";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import BaseTooltip from "@/components/ui/BaseTooltip.vue";
import BaseModal from "@/components/ui/BaseModal.vue";

const props = defineProps<{
    content: string;
    isViewMode: boolean;
    side: "left" | "right";
    width: string;
    layoutMode?: "book" | "page";
    isDiffMode?: boolean;
    diffContent?: string;
    renderMarkdown?: (markdown: string, element: HTMLElement) => Promise<void>;
    bookId?: number;
    pageId?: number;
    livePreview?: boolean;
}>();

const emit = defineEmits<{
    "update:content": [string];
    "copy-content": [];
    "clear-content": [];
    "open-in-page-view": [];
    "toggle-layout": [];
    "toggle-preview": [];
}>();

const toast = useToast();

// Check if user is anonymous (not authenticated)
const isAnonymous = computed(() => !isAuthenticated());

const textareaRef = ref<HTMLTextAreaElement>();
const lineNumbersRef = ref<HTMLElement>();
const mirrorRef = ref<HTMLPreElement>();
const viewRef = ref<HTMLElement>();
const fileInputRef = ref<HTMLInputElement>();
const showCopyTooltip = ref(false);

// AI dropdown state
const aiDropdownRef = ref<HTMLElement | null>(null);
const aiDropdownOpen = ref(false);
const aiLoading = ref(false);

// Share dialog state
const showShareDialog = ref(false);
const linkCopied = ref(false);

const { isDragging, handleDragOver, handleDragLeave, handleDrop } =
    useDragDrop();
const { processImage, generateImageMarkdown, uploadProgress } = useImage();

// Text formatting shortcuts
const textFormatting = useTextFormatting(
    () => textareaRef.value ?? null,
    (newContent) => emit("update:content", newContent),
);

useClickOutside(aiDropdownRef, () => {
    aiDropdownOpen.value = false;
});

// Handle keyboard shortcuts for text formatting
function handleTextareaKeydown(e: KeyboardEvent) {
    // Only process when Ctrl/Cmd is pressed
    if (!e.ctrlKey && !e.metaKey) return;

    const key = e.key.toLowerCase();

    // Text formatting shortcuts
    if (key === "b") {
        e.preventDefault();
        textFormatting.bold();
    } else if (key === "i") {
        e.preventDefault();
        textFormatting.italic();
    } else if (key === "k") {
        e.preventDefault();
        textFormatting.link();
    } else if (key === "`") {
        e.preventDefault();
        if (e.shiftKey) {
            textFormatting.codeBlock();
        } else {
            textFormatting.code();
        }
    } else if (key === "1" && e.shiftKey) {
        e.preventDefault();
        textFormatting.heading(1);
    } else if (key === "2" && e.shiftKey) {
        e.preventDefault();
        textFormatting.heading(2);
    } else if (key === "3" && e.shiftKey) {
        e.preventDefault();
        textFormatting.heading(3);
    } else if (key === "u" && e.shiftKey) {
        e.preventDefault();
        textFormatting.bulletList();
    } else if (key === "o" && e.shiftKey) {
        e.preventDefault();
        textFormatting.numberedList();
    } else if (key === "'" && e.shiftKey) {
        e.preventDefault();
        textFormatting.quote();
    }
}

function handleAiKeydown(e: KeyboardEvent) {
    if (e.key === "Escape" && aiDropdownOpen.value) {
        aiDropdownOpen.value = false;
    }
}

let resizeObserver: ResizeObserver | null = null;

onMounted(() => {
    document.addEventListener("keydown", handleAiKeydown);
    nextTick(() => measureLineHeights());

    // Re-measure when textarea resizes (e.g. window resize, layout change)
    if (textareaRef.value) {
        resizeObserver = new ResizeObserver(() => measureLineHeights());
        resizeObserver.observe(textareaRef.value);
    }
});
onUnmounted(() => {
    document.removeEventListener("keydown", handleAiKeydown);
    resizeObserver?.disconnect();
});

// Share state
const shareLink = ref("");
const shareLoading = ref(false);
const shareError = ref("");

const shareMessage =
    "This document was written on Doccoon editor. View it by clicking on the link below!";

async function generateShareLink(): Promise<boolean> {
    if (!props.content.trim()) {
        shareError.value = "Cannot share an empty page.";
        return false;
    }

    if (!isAuthenticated()) {
        shareError.value = "Please sign in to share pages.";
        return false;
    }

    if (!props.bookId || !props.pageId) {
        shareError.value =
            "This page must be saved to the server before sharing. Please save your book first.";
        return false;
    }

    shareLoading.value = true;
    shareError.value = "";

    try {
        const result = await sharePageApi(props.bookId!, props.pageId!);
        if (result?.share_token) {
            shareLink.value = `${window.location.origin}/shared/page/${result.share_token}`;
            return true;
        }
        shareError.value = "Failed to generate share link.";
        return false;
    } catch (err: unknown) {
        const error = err as { message?: string };
        logger.error("Share error:", error);
        shareError.value =
            error.message || "Failed to share page. Please try again.";
        return false;
    } finally {
        shareLoading.value = false;
    }
}

async function openShareDialog() {
    showShareDialog.value = true;
    if (!shareLink.value) {
        await generateShareLink();
    }
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

// AI typewriter effect state
let typewriterTimer: ReturnType<typeof setTimeout> | null = null;

function stopTypewriter() {
    if (typewriterTimer !== null) {
        clearTimeout(typewriterTimer);
        typewriterTimer = null;
    }
}

onUnmounted(() => stopTypewriter());

function stripMarkdownFences(text: string): string {
    let result = text.trim();
    if (result.startsWith("```markdown")) {
        result = result.slice("```markdown".length);
    } else if (result.startsWith("```md")) {
        result = result.slice("```md".length);
    } else if (result.startsWith("```")) {
        result = result.slice(3);
    }
    if (result.endsWith("```")) {
        result = result.slice(0, -3);
    }
    return result.trim();
}

function typewriterEmit(fullText: string, onDone: () => void) {
    stopTypewriter();
    const cleaned = stripMarkdownFences(fullText);
    const chunkSize = 3;
    const intervalMs = 12;
    let index = 0;

    function tick() {
        index = Math.min(index + chunkSize, cleaned.length);
        emit("update:content", cleaned.slice(0, index));
        if (index < cleaned.length) {
            typewriterTimer = setTimeout(tick, intervalMs);
        } else {
            typewriterTimer = null;
            onDone();
        }
    }

    tick();
}

// AI actions
async function handleAiAction(mode: "refine" | "rewrite") {
    aiDropdownOpen.value = false;

    if (!props.content.trim()) return;

    if (!isAuthenticated()) {
        toast.error("Please sign in to use AI features.");
        return;
    }

    aiLoading.value = true;
    try {
        const result = await refineContent({ content: props.content, mode });
        if (result?.refined) {
            typewriterEmit(result.refined, () => {
                aiLoading.value = false;
            });
            return;
        }
    } catch (err: unknown) {
        const error = err as { message?: string };
        logger.error("AI refine error:", error);
        toast.error(
            error.message ||
                "Failed to process with AI. Please check your AI provider key in settings.",
        );
    }
    aiLoading.value = false;
}

function shortenBase64Images(content: string): string {
    return content
        .replace(
            /(!?\[[^\]]*\]\(data:image\/[^;]+;base64,)([A-Za-z0-9+/=]{50,})(\))/g,
            (_match, prefix, base64, suffix) => {
                const start = base64.substring(0, 40);
                const end = base64.substring(base64.length - 10);
                return `${prefix}${start}...${end}${suffix}`;
            },
        )
        .replace(
            /(<img[^>]+src=["']data:image\/[^;]+;base64,)([A-Za-z0-9+/=]{50,})(["'][^>]*>)/g,
            (_match, prefix, base64, suffix) => {
                const start = base64.substring(0, 40);
                const end = base64.substring(base64.length - 10);
                return `${prefix}${start}...${end}${suffix}`;
            },
        );
}

function restoreBase64Images(
    shortenedContent: string,
    originalContent: string,
): string {
    const base64Map = new Map<string, string>();
    const fullRegex =
        /(!?\[[^\]]*\]\(data:image\/[^;]+;base64,)([A-Za-z0-9+/=]{50,})(\))/g;
    let match;

    while ((match = fullRegex.exec(originalContent)) !== null) {
        const prefix = match[1];
        const fullBase64 = match[2];
        const suffix = match[3];
        if (!fullBase64) continue;
        const start = fullBase64.substring(0, 40);
        const end = fullBase64.substring(fullBase64.length - 10);
        const shortenedKey = `${prefix}${start}...${end}${suffix}`;
        const fullValue = `${prefix}${fullBase64}${suffix}`;
        base64Map.set(shortenedKey, fullValue);
    }

    const htmlRegex =
        /(<img[^>]+src=["']data:image\/[^;]+;base64,)([A-Za-z0-9+/=]{50,})(["'][^>]*>)/g;
    while ((match = htmlRegex.exec(originalContent)) !== null) {
        const prefix = match[1];
        const fullBase64 = match[2];
        const suffix = match[3];
        if (!fullBase64) continue;
        const start = fullBase64.substring(0, 40);
        const end = fullBase64.substring(fullBase64.length - 10);
        const shortenedKey = `${prefix}${start}...${end}${suffix}`;
        const fullValue = `${prefix}${fullBase64}${suffix}`;
        base64Map.set(shortenedKey, fullValue);
    }

    let restoredContent = shortenedContent;
    for (const [shortened, full] of base64Map.entries()) {
        restoredContent = restoredContent.replace(shortened, full);
    }
    return restoredContent;
}

const displayContent = computed(() => shortenBase64Images(props.content));

const lineHeights = ref<number[]>([26]);

function measureLineHeights() {
    const mirror = mirrorRef.value;
    const textarea = textareaRef.value;
    if (!mirror || !textarea) return;

    // Match mirror width to textarea
    const style = window.getComputedStyle(textarea);
    mirror.style.width = style.width;
    mirror.style.fontFamily = style.fontFamily;
    mirror.style.fontSize = style.fontSize;
    mirror.style.lineHeight = style.lineHeight;
    mirror.style.paddingLeft = style.paddingLeft;
    mirror.style.paddingRight = style.paddingRight;
    mirror.style.boxSizing = style.boxSizing;
    mirror.style.overflowWrap = "break-word";
    mirror.style.wordBreak = style.wordBreak;

    const lines = displayContent.value.split("\n");
    const singleLineHeight =
        parseFloat(style.lineHeight) || parseFloat(style.fontSize) * 1.6;
    const heights: number[] = [];

    for (const line of lines) {
        // Use a zero-width space for empty lines so the pre still renders one line height
        mirror.textContent = line || "\u200b";
        const h = mirror.getBoundingClientRect().height;
        heights.push(Math.max(h, singleLineHeight));
    }

    lineHeights.value = heights;
}

function syncScroll() {
    if (textareaRef.value && lineNumbersRef.value) {
        lineNumbersRef.value.scrollTop = textareaRef.value.scrollTop;
    }
}

function onFocus() {
    /* reserved */
}
function onBlur() {
    /* reserved */
}

async function copyContent() {
    try {
        await navigator.clipboard.writeText(props.content);
        showCopyTooltip.value = true;
        setTimeout(() => {
            showCopyTooltip.value = false;
        }, 2000);
    } catch (err) {
        logger.error("Failed to copy content:", err);
    }
}

function clearContent() {
    emit("update:content", "");
}

function openInPageView() {
    if (props.layoutMode === "page") {
        emit("toggle-layout");
    } else {
        emit("open-in-page-view");
    }
}

function triggerImageUpload() {
    fileInputRef.value?.click();
}

async function handleFileSelect(e: Event) {
    const target = e.target as HTMLInputElement;
    const files = target.files;
    if (!files || files.length === 0) return;

    const cursorPos = textareaRef.value?.selectionStart || props.content.length;

    for (const file of Array.from(files)) {
        try {
            const imageInfo = await processImage(file);
            const markdown = generateImageMarkdown(imageInfo);
            insertTextAtCursor(markdown, cursorPos);
        } catch (error) {
            logger.error("Failed to upload image:", error);
            toast.error(
                `Failed to upload ${file.name}: ${(error as Error).message}`,
            );
        }
    }
    target.value = "";
}

function insertTextAtCursor(text: string, cursorPos: number) {
    const before = props.content.substring(0, cursorPos);
    const after = props.content.substring(cursorPos);
    emit("update:content", before + text + after);

    nextTick(() => {
        if (textareaRef.value) {
            const newCursorPos = cursorPos + text.length;
            textareaRef.value.selectionStart = textareaRef.value.selectionEnd =
                newCursorPos;
            textareaRef.value.focus();
        }
    });
}

function onInput(e: Event) {
    const target = e.target as HTMLTextAreaElement;
    const restoredContent = restoreBase64Images(target.value, props.content);
    emit("update:content", restoredContent);
}

function onDragOver(e: DragEvent) {
    handleDragOver(e);
}
function onDragLeave(e: DragEvent) {
    handleDragLeave(e);
}

function onDrop(e: DragEvent) {
    if (!textareaRef.value) return;
    const cursorPos = textareaRef.value.selectionStart;

    handleDrop(
        e,
        (text: string, pos: number) => {
            if (!textareaRef.value) return;
            const before = props.content.substring(0, pos);
            const after = props.content.substring(pos);
            emit("update:content", before + text + after);

            nextTick(() => {
                if (textareaRef.value) {
                    textareaRef.value.selectionStart =
                        textareaRef.value.selectionEnd = pos + text.length;
                    textareaRef.value.focus();
                }
            });
        },
        cursorPos,
    );
}

async function renderContent() {
    if (!viewRef.value) return;
    if (props.isDiffMode && props.diffContent !== undefined) {
        viewRef.value.innerHTML = props.diffContent;
    } else if (props.renderMarkdown) {
        await props.renderMarkdown(props.content, viewRef.value);
    }
}

watch(displayContent, () => {
    nextTick(() => measureLineHeights());
});
watch(
    () => props.isViewMode,
    async (newValue) => {
        if (newValue && viewRef.value) {
            await nextTick();
            await renderContent();
        }
    },
);
watch(
    () => props.content,
    async () => {
        if (props.isViewMode && viewRef.value) {
            await nextTick();
            await renderContent();
        }
    },
);
watch(
    () => props.isDiffMode,
    async () => {
        if (props.isViewMode && viewRef.value) {
            await nextTick();
            await renderContent();
        }
    },
);
watch(
    () => props.diffContent,
    async () => {
        if (props.isViewMode && viewRef.value && props.isDiffMode) {
            await nextTick();
            await renderContent();
        }
    },
);
watch(
    viewRef,
    async (newValue) => {
        if (newValue && props.isViewMode) {
            await nextTick();
            await renderContent();
        }
    },
    { immediate: true },
);
</script>
