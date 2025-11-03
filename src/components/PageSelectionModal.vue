<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="modal-overlay" @click="handleOverlayClick">
        <div class="modal-container" @click.stop>
          <div class="modal-header">
            <h3>{{ title }}</h3>
          </div>

          <div class="modal-body">
            <p class="modal-message">{{ message }}</p>

            <div class="page-selection-buttons">
              <button class="page-select-btn left-page-btn" @click="selectLeft">
                <div class="page-preview">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="7" y1="8" x2="17" y2="8"></line>
                    <line x1="7" y1="12" x2="17" y2="12"></line>
                    <line x1="7" y1="16" x2="13" y2="16"></line>
                  </svg>
                </div>
                <span class="page-label">Left Page</span>
                <span class="page-hint">Current left content</span>
              </button>

              <button class="page-select-btn right-page-btn" @click="selectRight">
                <div class="page-preview">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="7" y1="8" x2="17" y2="8"></line>
                    <line x1="7" y1="12" x2="17" y2="12"></line>
                    <line x1="7" y1="16" x2="13" y2="16"></line>
                  </svg>
                </div>
                <span class="page-label">Right Page</span>
                <span class="page-hint">Current right content</span>
              </button>
            </div>
          </div>

          <div class="modal-footer">
            <button class="modal-btn cancel-btn" @click="cancel">Cancel</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
// Props are used in the template
defineProps<{
  visible: boolean;
  title?: string;
  message?: string;
}>();

const emit = defineEmits<{
  'select-left': [];
  'select-right': [];
  'cancel': [];
}>();

function selectLeft() {
  emit('select-left');
}

function selectRight() {
  emit('select-right');
}

function cancel() {
  emit('cancel');
}

function handleOverlayClick() {
  cancel();
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  backdrop-filter: blur(2px);
}

.modal-container {
  background: var(--page-bg);
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.modal-message {
  margin: 0 0 24px 0;
  color: var(--text-color);
  opacity: 0.8;
  font-size: 14px;
  line-height: 1.5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
}

.page-selection-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.page-select-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px 16px;
  background: transparent;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
  color: var(--text-color);
}

.page-select-btn:hover {
  border-color: #007ACC;
  background: rgba(0, 122, 204, 0.05);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 122, 204, 0.15);
}

.page-select-btn:active {
  transform: translateY(0);
}

.page-preview {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--border-color);
  border-radius: 6px;
  transition: all 0.2s ease;
}

.page-select-btn:hover .page-preview {
  background: rgba(0, 122, 204, 0.1);
  color: #007ACC;
}

.page-preview svg {
  display: block;
}

.page-label {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
}

.page-hint {
  font-size: 12px;
  color: var(--text-color);
  opacity: 0.6;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.modal-btn {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
}

.cancel-btn {
  background: transparent;
  color: var(--text-color);
  border: 1px solid var(--border-color);
}

.cancel-btn:hover {
  background: var(--border-color);
}

.cancel-btn:active {
  transform: scale(0.95);
}

/* Modal transition */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.2s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
}

/* Dark theme adjustments */
body.dark-theme .modal-overlay {
  background: rgba(0, 0, 0, 0.7);
}

body.dark-theme .modal-container {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}
</style>
