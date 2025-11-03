<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="modal-overlay" @click="handleOverlayClick">
        <div class="gallery-container" @click.stop>
          <div class="gallery-header">
            <h2>Image Gallery</h2>
            <button class="close-btn" @click="close" title="Close">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <div class="gallery-body">
            <div v-if="images.length === 0" class="empty-state">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                <polyline points="21 15 16 10 5 21"></polyline>
              </svg>
              <p>No images in this book yet</p>
              <p class="hint">Drag & drop images into the editor or use the "Insert Image" button</p>
            </div>

            <div v-else class="gallery-grid">
              <div v-for="image in images" :key="image.id" class="gallery-item">
                <div class="image-preview" @click="previewImage(image)">
                  <img :src="image.dataUrl" :alt="image.filename" />
                  <div class="image-overlay">
                    <button class="overlay-btn" @click.stop="insertImage(image)" title="Insert into page">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                      </svg>
                    </button>
                    <button class="overlay-btn" @click.stop="copyMarkdown(image)" title="Copy markdown">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                      </svg>
                    </button>
                  </div>
                </div>
                <div class="image-info">
                  <div class="image-filename" :title="image.filename">{{ image.filename }}</div>
                  <div class="image-meta">
                    <span>{{ image.width }} × {{ image.height }}</span>
                    <span>{{ formatFileSize(image.size) }}</span>
                  </div>
                  <div v-if="image.usedInPages.length > 0" class="image-usage">
                    Used in {{ image.usedInPages.length }} page(s)
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="gallery-footer">
            <div class="gallery-stats">
              {{ images.length }} image(s) • {{ totalSize }}
            </div>
            <button class="btn-secondary" @click="close">Close</button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Image Preview Modal -->
    <Transition name="modal">
      <div v-if="previewImageData" class="modal-overlay preview-overlay" @click="closePreview">
        <div class="preview-container" @click.stop>
          <button class="close-btn preview-close" @click="closePreview" title="Close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
          <img :src="previewImageData.dataUrl" :alt="previewImageData.filename" class="preview-image" />
          <div class="preview-info">
            <div class="preview-filename">{{ previewImageData.filename }}</div>
            <div class="preview-meta">
              {{ previewImageData.width }} × {{ previewImageData.height }} • {{ formatFileSize(previewImageData.size) }}
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { ImageInfo } from '@/composables/useImage';
import { useImage } from '@/composables/useImage';

// Props are used in the template
defineProps<{
  visible: boolean;
  images: ImageInfo[];
}>();

const emit = defineEmits<{
  'close': [];
  'insert-image': [ImageInfo];
}>();

const { formatFileSize, generateImageMarkdown } = useImage();
const previewImageData = ref<ImageInfo | null>(null);
const copiedImageId = ref<string | null>(null);

const totalSize = computed(() => {
  const total = (window as any).props?.images?.reduce((sum: number, img: ImageInfo) => sum + img.size, 0) || 0;
  return formatFileSize(total);
});

function close() {
  emit('close');
}

function handleOverlayClick() {
  close();
}

function insertImage(image: ImageInfo) {
  emit('insert-image', image);
}

async function copyMarkdown(image: ImageInfo) {
  const markdown = generateImageMarkdown(image);
  try {
    await navigator.clipboard.writeText(markdown);
    copiedImageId.value = image.id;
    setTimeout(() => {
      copiedImageId.value = null;
    }, 2000);
  } catch (error) {
    console.error('Failed to copy markdown:', error);
  }
}

function previewImage(image: ImageInfo) {
  previewImageData.value = image;
}

function closePreview() {
  previewImageData.value = null;
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.gallery-container {
  background: var(--page-bg);
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 1000px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
}

.gallery-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
}

.gallery-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-color);
}

.close-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  color: var(--text-color);
  opacity: 0.6;
  transition: opacity 0.2s;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  opacity: 1;
}

.gallery-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--text-color);
  opacity: 0.6;
  text-align: center;
}

.empty-state svg {
  margin-bottom: 16px;
  opacity: 0.4;
}

.empty-state p {
  margin: 8px 0;
}

.empty-state .hint {
  font-size: 14px;
  opacity: 0.7;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.gallery-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.image-preview {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  background: var(--border-color);
  cursor: pointer;
  transition: transform 0.2s;
}

.image-preview:hover {
  transform: scale(1.02);
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  opacity: 0;
  transition: opacity 0.2s;
}

.image-preview:hover .image-overlay {
  opacity: 1;
}

.overlay-btn {
  background: white;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s;
  color: #333;
}

.overlay-btn:hover {
  transform: scale(1.1);
}

.image-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.image-filename {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-color);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.image-meta {
  font-size: 12px;
  color: var(--text-color);
  opacity: 0.6;
  display: flex;
  gap: 8px;
}

.image-usage {
  font-size: 11px;
  color: #007ACC;
  font-weight: 500;
}

.gallery-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-top: 1px solid var(--border-color);
}

.gallery-stats {
  font-size: 13px;
  color: var(--text-color);
  opacity: 0.7;
}

.btn-secondary {
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  color: var(--text-color);
  font-size: 14px;
  transition: all 0.2s;
}

.btn-secondary:hover {
  border-color: #007ACC;
  color: #007ACC;
  background: rgba(0, 122, 204, 0.05);
}

/* Preview Modal */
.preview-overlay {
  background: rgba(0, 0, 0, 0.9);
}

.preview-container {
  position: relative;
  max-width: 90%;
  max-height: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.preview-close {
  position: absolute;
  top: -50px;
  right: 0;
  color: white;
}

.preview-image {
  max-width: 100%;
  max-height: calc(90vh - 100px);
  object-fit: contain;
  border-radius: 4px;
}

.preview-info {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 12px 20px;
  border-radius: 8px;
  text-align: center;
}

.preview-filename {
  color: white;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
}

.preview-meta {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .gallery-container,
.modal-enter-active .preview-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .gallery-container,
.modal-enter-from .preview-container {
  transform: scale(0.9);
}
</style>

