<template>
  <div class="book-wrapper">
    <div class="book" :class="{ 'page-view': layoutMode === 'page' }">
      <BookPage :content="spread.left" :is-view-mode="isViewMode" side="left"
        :width="layoutMode === 'page' ? '1' : spread.leftWidth" :layout-mode="layoutMode" :is-diff-mode="isDiffMode"
        :diff-content="leftDiffContent" :render-markdown="renderMarkdown" @update:content="updateLeft"
        @open-in-page-view="openLeftInPageView" @toggle-layout="toggleLayout" />

      <BookmarkSeparator v-if="layoutMode === 'book'" @start-resize="startResize" />

      <BookPage v-if="layoutMode === 'book'" :content="spread.right" :is-view-mode="isViewMode" side="right"
        :width="spread.rightWidth" :layout-mode="layoutMode" :is-diff-mode="isDiffMode" :diff-content="rightDiffContent"
        :render-markdown="renderMarkdown" @update:content="updateRight" @open-in-page-view="openRightInPageView"
        @toggle-layout="toggleLayout" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue';
import BookPage from './BookPage.vue';
import BookmarkSeparator from './BookmarkSeparator.vue';
import { useResize } from '@/composables/useResize';
import type { Spread } from '@/types';

const props = defineProps<{
  spread: Spread;
  isViewMode: boolean;
  layoutMode: 'book' | 'page';
  isDiffMode?: boolean;
  leftDiffContent?: string;
  rightDiffContent?: string;
  renderMarkdown?: (markdown: string, element: HTMLElement) => Promise<void>;
}>();

const emit = defineEmits<{
  'update:spread': [Partial<Spread>];
  'open-page-view': ['left' | 'right'];
  'toggle-layout': [];
}>();

const { isResizing, startResize: startResizeComposable, handleResize, stopResize } = useResize();

function updateLeft(content: string) {
  emit('update:spread', { left: content });
}

function updateRight(content: string) {
  emit('update:spread', { right: content });
}

function openLeftInPageView() {
  emit('open-page-view', 'left');
}

function openRightInPageView() {
  emit('open-page-view', 'right');
}

function toggleLayout() {
  emit('toggle-layout');
}

function startResize(e: MouseEvent) {
  const leftWidth = parseFloat(props.spread.leftWidth);
  const rightWidth = parseFloat(props.spread.rightWidth);
  startResizeComposable(e, leftWidth, rightWidth);
}

function onMouseMove(e: MouseEvent) {
  handleResize(e, (leftWidth: number, rightWidth: number) => {
    emit('update:spread', {
      leftWidth: leftWidth.toString(),
      rightWidth: rightWidth.toString()
    });
  });
}

function onMouseUp() {
  stopResize();
}

onMounted(() => {
  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('mouseup', onMouseUp);
});

onUnmounted(() => {
  document.removeEventListener('mousemove', onMouseMove);
  document.removeEventListener('mouseup', onMouseUp);
});
</script>

<style scoped>
/* Styles are in main.css */
</style>
