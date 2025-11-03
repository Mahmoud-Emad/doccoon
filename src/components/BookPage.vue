<template>
  <div class="page" :class="`${side}-page`" :style="{ flex: width }">
    <!-- Action Buttons - Only in Edit Mode -->
    <div v-if="!isViewMode" class="page-actions">
      <button class="page-action-btn copy-btn" @click="copyContent" :title="`Copy ${side} page content`">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
        Copy Content
        <!-- Copy tooltip -->
        <div v-if="showCopyTooltip" class="action-tooltip">Copied!</div>
      </button>
      <button class="page-action-btn" @click="clearContent" :title="`Clear ${side} page content`">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="3 6 5 6 21 6"></polyline>
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
        </svg>
        Clear Content
      </button>
      <button class="page-action-btn" @click="openInPageView"
        :title="layoutMode === 'page' ? 'Open in book view' : `Open ${side} page in page view`">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
          <polyline points="15 3 21 3 21 9"></polyline>
          <line x1="10" y1="14" x2="21" y2="3"></line>
        </svg>
        {{ layoutMode === 'page' ? 'Open in Book View' : 'Open in Page View' }}
      </button>
    </div>

    <div class="page-content">
      <!-- Edit Mode: Textarea with Line Numbers -->
      <div v-if="!isViewMode" class="editor-container">
        <div ref="lineNumbersRef" class="line-numbers">
          <div v-for="n in lineCount" :key="n" class="line-number">{{ n }}</div>
        </div>
        <textarea ref="textareaRef" class="page-textarea" :class="{ 'drag-over': isDragging }" :value="content"
          :placeholder="`Start writing on the ${side} page...`" @input="onInput" @scroll="syncScroll"
          @dragover="onDragOver" @dragleave="onDragLeave" @drop="onDrop"></textarea>
      </div>

      <!-- View Mode: Rendered Markdown -->
      <div v-if="isViewMode" ref="viewRef" class="page-view"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, computed } from 'vue';
import { useDragDrop } from '@/composables/useDragDrop';

const props = defineProps<{
  content: string;
  isViewMode: boolean;
  side: 'left' | 'right';
  width: string;
  layoutMode?: 'book' | 'page';
  renderMarkdown?: (markdown: string, element: HTMLElement) => Promise<void>;
}>();

const emit = defineEmits<{
  'update:content': [string];
  'copy-content': [];
  'clear-content': [];
  'open-in-page-view': [];
  'toggle-layout': [];
}>();

const textareaRef = ref<HTMLTextAreaElement>();
const lineNumbersRef = ref<HTMLElement>();
const viewRef = ref<HTMLElement>();
const showCopyTooltip = ref(false);

const { isDragging, handleDragOver, handleDragLeave, handleDrop } = useDragDrop();

// Calculate line count
const lineCount = computed(() => {
  const lines = props.content.split('\n').length;
  return Math.max(lines, 1); // At least 1 line
});

// Sync scroll between textarea and line numbers
function syncScroll() {
  if (textareaRef.value && lineNumbersRef.value) {
    lineNumbersRef.value.scrollTop = textareaRef.value.scrollTop;
  }
}

// Action button handlers
async function copyContent() {
  try {
    await navigator.clipboard.writeText(props.content);
    showCopyTooltip.value = true;
    setTimeout(() => {
      showCopyTooltip.value = false;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy content:', err);
  }
}

function clearContent() {
  emit('update:content', '');
}

function openInPageView() {
  if (props.layoutMode === 'page') {
    // If in page view, switch to book view
    emit('toggle-layout');
  } else {
    // If in book view, open this page in page view
    emit('open-in-page-view');
  }
}

function onInput(e: Event) {
  const target = e.target as HTMLTextAreaElement;
  emit('update:content', target.value);
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

  handleDrop(e, (text: string, pos: number) => {
    if (!textareaRef.value) return;

    const before = props.content.substring(0, pos);
    const after = props.content.substring(pos);
    const newContent = before + text + after;

    emit('update:content', newContent);

    nextTick(() => {
      if (textareaRef.value) {
        textareaRef.value.selectionStart = textareaRef.value.selectionEnd = pos + text.length;
        textareaRef.value.focus();
      }
    });
  }, cursorPos);
}

// Watch for view mode changes and render markdown
watch(() => props.isViewMode, async (newValue) => {
  if (newValue && viewRef.value && props.renderMarkdown) {
    await nextTick();
    await props.renderMarkdown(props.content, viewRef.value);
  }
});

// Watch for content changes in view mode
watch(() => props.content, async (newValue) => {
  if (props.isViewMode && viewRef.value && props.renderMarkdown) {
    await nextTick();
    await props.renderMarkdown(newValue, viewRef.value);
  }
});

// Initial render when component mounts
watch(viewRef, async (newValue) => {
  if (newValue && props.isViewMode && props.renderMarkdown) {
    await nextTick();
    await props.renderMarkdown(props.content, newValue);
  }
}, { immediate: true });
</script>

<style scoped>
.editor-container {
  display: flex;
  height: 100%;
  position: relative;
}

.line-numbers {
  flex-shrink: 0;
  width: 50px;
  background: var(--page-bg);
  border-right: 1px solid var(--border-color);
  overflow: hidden;
  user-select: none;
  padding: 0;
  text-align: right;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-color);
  opacity: 0.35;
}

.line-number {
  padding-right: 8px;
  padding-left: 4px;
  /* Line height is inherited from .line-numbers (1.6) */
  /* This matches the textarea exactly: 16px * 1.6 = 25.6px per line */
}

.page-textarea {
  flex: 1;
  padding: 0 0 0 12px !important;
  /* Ensure no top/bottom padding to match line numbers */
}

.page-actions {
  display: flex;
  gap: 8px;
  padding: 5px;
  border-bottom: 1px solid var(--border-color);
  background: var(--page-bg);
  position: relative;
  margin-bottom: 10px;
}

.page-action-btn {
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 6px 8px;
  cursor: pointer;
  color: var(--text-color);
  opacity: 0.6;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
  position: relative;
}

.page-action-btn:hover {
  opacity: 1;
  border-color: #007ACC;
  color: #007ACC;
  background: rgba(0, 122, 204, 0.05);
}

.page-action-btn:active {
  transform: scale(0.95);
}

.page-action-btn svg {
  display: block;
  flex-shrink: 0;
}

.action-tooltip {
  position: absolute;
  top: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  background: #007ACC;
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  pointer-events: none;
  animation: tooltipFadeIn 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 10;
}

.action-tooltip::after {
  content: '';
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 4px solid transparent;
  border-bottom-color: #007ACC;
}

@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
