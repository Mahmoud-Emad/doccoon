<template>
    <div class="relative w-full flex-1 flex flex-col overflow-hidden pt-4 pb-4">
        <div
            class="flex max-md:flex-col bg-[var(--bg-color)] overflow-hidden h-full relative flex-1"
            :class="{ 'justify-center': layoutMode === 'page' }"
        >
            <BookPage
                :content="spread.left"
                :is-view-mode="isViewMode"
                side="left"
                :width="
                    livePreview
                        ? '1'
                        : layoutMode === 'page'
                          ? '1'
                          : spread.leftWidth
                "
                :layout-mode="livePreview ? 'book' : layoutMode"
                :is-diff-mode="isDiffMode"
                :diff-content="leftDiffContent"
                :render-markdown="renderMarkdown"
                :book-id="bookId"
                :page-id="spread.leftPageId"
                :live-preview="livePreview"
                @update:content="updateLeft"
                @open-in-page-view="openLeftInPageView"
                @toggle-layout="toggleLayout"
                @toggle-preview="$emit('toggle-preview')"
            />

            <BookmarkSeparator
                v-if="layoutMode === 'book' || livePreview"
                class="max-md:hidden"
                @start-resize="startResize"
            />

            <!-- Mobile divider between stacked pages -->
            <div
                v-if="layoutMode === 'book' || livePreview"
                class="hidden max-md:block h-px bg-[var(--border-color)] shrink-0"
            />

            <!-- Live Preview: right pane shows rendered left content -->
            <BookPage
                v-if="livePreview"
                :content="spread.left"
                :is-view-mode="true"
                side="right"
                width="1"
                layout-mode="book"
                :render-markdown="renderMarkdown"
                :book-id="bookId"
            />

            <!-- Normal book mode: right page editor -->
            <BookPage
                v-else-if="layoutMode === 'book'"
                :content="spread.right"
                :is-view-mode="isViewMode"
                side="right"
                :width="spread.rightWidth"
                :layout-mode="layoutMode"
                :is-diff-mode="isDiffMode"
                :diff-content="rightDiffContent"
                :render-markdown="renderMarkdown"
                :book-id="bookId"
                :page-id="spread.rightPageId"
                @update:content="updateRight"
                @open-in-page-view="openRightInPageView"
                @toggle-layout="toggleLayout"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from "vue";
import BookPage from "./BookPage.vue";
import BookmarkSeparator from "./BookmarkSeparator.vue";
import { useResize } from "@/composables/useResize";
import type { Spread } from "@/types";

const props = defineProps<{
    spread: Spread;
    isViewMode: boolean;
    layoutMode: "book" | "page";
    isDiffMode?: boolean;
    leftDiffContent?: string;
    rightDiffContent?: string;
    renderMarkdown?: (markdown: string, element: HTMLElement) => Promise<void>;
    bookId?: number;
    livePreview?: boolean;
}>();

const emit = defineEmits<{
    "update:spread": [Partial<Spread>];
    "open-page-view": ["left" | "right"];
    "toggle-layout": [];
    "toggle-preview": [];
}>();

const {
    startResize: startResizeComposable,
    handleResize,
    stopResize,
} = useResize();

function updateLeft(content: string) {
    emit("update:spread", { left: content });
}

function updateRight(content: string) {
    emit("update:spread", { right: content });
}

function openLeftInPageView() {
    emit("open-page-view", "left");
}

function openRightInPageView() {
    emit("open-page-view", "right");
}

function toggleLayout() {
    emit("toggle-layout");
}

function startResize(e: MouseEvent | TouchEvent) {
    const leftWidth = parseFloat(props.spread.leftWidth);
    const rightWidth = parseFloat(props.spread.rightWidth);
    startResizeComposable(e, leftWidth, rightWidth);
}

function onMouseMove(e: MouseEvent) {
    handleResize(e, (leftWidth: number, rightWidth: number) => {
        emit("update:spread", {
            leftWidth: leftWidth.toString(),
            rightWidth: rightWidth.toString(),
        });
    });
}

function onMouseUp() {
    stopResize();
}

onMounted(() => {
    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
});

onUnmounted(() => {
    document.removeEventListener("mousemove", onMouseMove);
    document.removeEventListener("mouseup", onMouseUp);
});
</script>
