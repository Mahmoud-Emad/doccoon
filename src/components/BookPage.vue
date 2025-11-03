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
      <button class="page-action-btn" @click="triggerImageUpload" :title="`Insert image into ${side} page`">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <circle cx="8.5" cy="8.5" r="1.5"></circle>
          <polyline points="21 15 16 10 5 21"></polyline>
        </svg>
        Insert Image
        <!-- Upload progress indicator -->
        <div v-if="uploadProgress > 0 && uploadProgress < 100" class="upload-progress">
          <div class="upload-progress-bar" :style="{ width: uploadProgress + '%' }"></div>
        </div>
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

    <!-- Hidden file input for image upload -->
    <input ref="fileInputRef" type="file" accept="image/png,image/jpeg,image/jpg,image/gif,image/svg+xml,image/webp"
      multiple style="display: none" @change="handleFileSelect" />

    <div class="page-content">
      <!-- Edit Mode: Textarea with Line Numbers -->
      <div v-if="!isViewMode" class="editor-container">
        <div ref="lineNumbersRef" class="line-numbers">
          <div v-for="n in lineCount" :key="n" class="line-number">{{ n }}</div>
        </div>
        <textarea ref="textareaRef" class="page-textarea" :class="{ 'drag-over': isDragging }" :value="displayContent"
          :placeholder="`Start writing on the ${side} page...`" @input="onInput" @scroll="syncScroll"
          @dragover="onDragOver" @dragleave="onDragLeave" @drop="onDrop" @focus="onFocus" @blur="onBlur"></textarea>
      </div>

      <!-- View Mode: Rendered Markdown or Diff -->
      <div v-if="isViewMode" ref="viewRef" class="page-view" :class="{ 'diff-view': isDiffMode }"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, computed } from 'vue';
import { useDragDrop } from '@/composables/useDragDrop';
import { useImage } from '@/composables/useImage';
import { logger } from '@/utils/logger';

const props = defineProps<{
  content: string;
  isViewMode: boolean;
  side: 'left' | 'right';
  width: string;
  layoutMode?: 'book' | 'page';
  isDiffMode?: boolean;
  diffContent?: string;
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
const fileInputRef = ref<HTMLInputElement>();
const showCopyTooltip = ref(false);

const { isDragging, handleDragOver, handleDragLeave, handleDrop } = useDragDrop();
const { processImage, generateImageMarkdown, uploadProgress } = useImage();

/**
 * Shorten base64 image data URLs for display in editor
 * Keeps first 40 chars and last 10 chars of base64 for reference
 */
function shortenBase64Images(content: string): string {
  // Match both markdown images and HTML img tags with base64 data
  return content.replace(
    /(!?\[[^\]]*\]\(data:image\/[^;]+;base64,)([A-Za-z0-9+/=]{50,})(\))/g,
    (_match, prefix, base64, suffix) => {
      const start = base64.substring(0, 40);
      const end = base64.substring(base64.length - 10);
      return `${prefix}${start}...${end}${suffix}`;
    }
  ).replace(
    /(<img[^>]+src=["']data:image\/[^;]+;base64,)([A-Za-z0-9+/=]{50,})(["'][^>]*>)/g,
    (_match, prefix, base64, suffix) => {
      const start = base64.substring(0, 40);
      const end = base64.substring(base64.length - 10);
      return `${prefix}${start}...${end}${suffix}`;
    }
  );
}

/**
 * Restore full base64 data from shortened version
 */
function restoreBase64Images(shortenedContent: string, originalContent: string): string {
  // Build a map of shortened -> full base64 strings
  const base64Map = new Map<string, string>();

  // Extract all full base64 images from original content
  const fullRegex = /(!?\[[^\]]*\]\(data:image\/[^;]+;base64,)([A-Za-z0-9+/=]{50,})(\))/g;
  let match;

  while ((match = fullRegex.exec(originalContent)) !== null) {
    const prefix = match[1];
    const fullBase64 = match[2];
    const suffix = match[3];

    if (!fullBase64) continue;

    // Create the shortened version key
    const start = fullBase64.substring(0, 40);
    const end = fullBase64.substring(fullBase64.length - 10);
    const shortenedKey = `${prefix}${start}...${end}${suffix}`;
    const fullValue = `${prefix}${fullBase64}${suffix}`;

    base64Map.set(shortenedKey, fullValue);
  }

  // Also handle HTML img tags
  const htmlRegex = /(<img[^>]+src=["']data:image\/[^;]+;base64,)([A-Za-z0-9+/=]{50,})(["'][^>]*>)/g;
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

  // Replace shortened versions with full versions
  let restoredContent = shortenedContent;
  for (const [shortened, full] of base64Map.entries()) {
    restoredContent = restoredContent.replace(shortened, full);
  }

  return restoredContent;
}

/**
 * Display content with shortened base64 images
 */
const displayContent = computed(() => {
  return shortenBase64Images(props.content);
});

// Calculate line count based on display content
const lineCount = computed(() => {
  const lines = displayContent.value.split('\n').length;
  return Math.max(lines, 1); // At least 1 line
});

// Sync scroll between textarea and line numbers
function syncScroll() {
  if (textareaRef.value && lineNumbersRef.value) {
    lineNumbersRef.value.scrollTop = textareaRef.value.scrollTop;
  }
}

// Focus/blur handlers (kept for potential future use)
function onFocus() {
  // Currently not used, but available for future enhancements
}

function onBlur() {
  // Currently not used, but available for future enhancements
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
    logger.error('Failed to copy content:', err);
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

// Image upload functions
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
      logger.error('Failed to upload image:', error);
      alert(`Failed to upload ${file.name}: ${(error as Error).message}`);
    }
  }

  // Reset file input
  target.value = '';
}

function insertTextAtCursor(text: string, cursorPos: number) {
  const before = props.content.substring(0, cursorPos);
  const after = props.content.substring(cursorPos);
  const newContent = before + text + after;

  emit('update:content', newContent);

  nextTick(() => {
    if (textareaRef.value) {
      const newCursorPos = cursorPos + text.length;
      textareaRef.value.selectionStart = textareaRef.value.selectionEnd = newCursorPos;
      textareaRef.value.focus();
    }
  });
}

function onInput(e: Event) {
  const target = e.target as HTMLTextAreaElement;
  const editedContent = target.value;

  // Restore any shortened base64 images to their full versions
  const restoredContent = restoreBase64Images(editedContent, props.content);

  emit('update:content', restoredContent);
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

    // Set cursor position after the inserted content
    nextTick(() => {
      if (textareaRef.value) {
        textareaRef.value.selectionStart = textareaRef.value.selectionEnd = pos + text.length;
        textareaRef.value.focus();
      }
    });
  }, cursorPos);
}

// Render content based on mode (normal or diff)
async function renderContent() {
  if (!viewRef.value) return;

  if (props.isDiffMode && props.diffContent !== undefined) {
    // Render diff view
    viewRef.value.innerHTML = props.diffContent;
  } else if (props.renderMarkdown) {
    // Render normal markdown
    await props.renderMarkdown(props.content, viewRef.value);
  }
}

// Watch for view mode changes and render markdown or diff
watch(() => props.isViewMode, async (newValue) => {
  if (newValue && viewRef.value) {
    await nextTick();
    await renderContent();
  }
});

// Watch for content changes in view mode
watch(() => props.content, async () => {
  if (props.isViewMode && viewRef.value) {
    await nextTick();
    await renderContent();
  }
});

// Watch for diff mode changes
watch(() => props.isDiffMode, async () => {
  if (props.isViewMode && viewRef.value) {
    await nextTick();
    await renderContent();
  }
});

// Watch for diff content changes
watch(() => props.diffContent, async () => {
  if (props.isViewMode && viewRef.value && props.isDiffMode) {
    await nextTick();
    await renderContent();
  }
});

// Initial render when component mounts
watch(viewRef, async (newValue) => {
  if (newValue && props.isViewMode) {
    await nextTick();
    await renderContent();
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

/* Upload Progress Indicator */
.upload-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: rgba(0, 122, 204, 0.1);
  overflow: hidden;
}

.upload-progress-bar {
  height: 100%;
  background: #007ACC;
  transition: width 0.3s ease;
}

/* Drag Over State */
.page-textarea.drag-over {
  border: 2px dashed #007ACC !important;
  background: rgba(0, 122, 204, 0.05) !important;
}

/* Diff View Styles */
.diff-view {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
  font-size: 14px;
  line-height: 1.6;
}

.diff-view :deep(.diff-line) {
  padding: 2px 8px;
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  position: relative;
  line-height: 1.4;
}

.diff-view :deep(.diff-symbol) {
  display: inline-block;
  width: 20px;
  font-weight: bold;
  margin-right: 8px;
  user-select: none;
}

.diff-view :deep(.diff-line-added) {
  background-color: #e6ffed;
  border-left: 3px solid #28a745;
  color: #24292f;
}

.diff-view :deep(.diff-line-added .diff-symbol) {
  color: #28a745;
}

.diff-view :deep(.diff-line-removed) {
  background-color: #ffeef0;
  border-left: 3px solid #dc3545;
  color: #24292f;
}

.diff-view :deep(.diff-line-removed .diff-symbol) {
  color: #dc3545;
}

.diff-view :deep(.diff-line-placeholder) {
  background-color: #f5f5f5;
  border-left: 3px solid #d0d0d0;
  color: #57606a;
}

.diff-view :deep(.diff-line-placeholder .diff-symbol) {
  color: #999;
}

/* Dark theme diff colors */
:root[data-theme="dark"] .diff-view :deep(.diff-line-added) {
  background-color: #1e4620;
  border-left-color: #3fb950;
  color: #c9d1d9;
}

:root[data-theme="dark"] .diff-view :deep(.diff-line-added .diff-symbol) {
  color: #3fb950;
}

:root[data-theme="dark"] .diff-view :deep(.diff-line-removed) {
  background-color: #4a1c1c;
  border-left-color: #f85149;
  color: #c9d1d9;
}

:root[data-theme="dark"] .diff-view :deep(.diff-line-removed .diff-symbol) {
  color: #f85149;
}

:root[data-theme="dark"] .diff-view :deep(.diff-line-placeholder) {
  background-color: #0d1117;
  border-left-color: #444;
  color: #8b949e;
}

:root[data-theme="dark"] .diff-view :deep(.diff-line-placeholder .diff-symbol) {
  color: #666;
}
</style>
