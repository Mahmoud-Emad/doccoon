<template>
  <div v-if="visible" class="modal-overlay" @click="onCancel">
    <div class="modal" :class="{ 'modal-danger': isDanger }" @click.stop>
      <div class="modal-header">
        <h3>{{ title }}</h3>
      </div>
      <div class="modal-body">
        <p>{{ message }}</p>
      </div>
      <div class="modal-footer">
        <button class="modal-btn modal-btn-cancel" @click="onCancel">
          Cancel
        </button>
        <button class="modal-btn modal-btn-confirm" :class="{ 'modal-btn-danger': isDanger }" @click="onConfirm">
          Confirm
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onUnmounted, watch } from 'vue';

const props = defineProps<{
  visible: boolean;
  title: string;
  message: string;
  isDanger: boolean;
}>();

const emit = defineEmits<{
  confirm: [];
  cancel: [];
}>();

function onConfirm() {
  emit('confirm');
}

function onCancel() {
  emit('cancel');
}

// Handle Escape key
function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape' && props.visible) {
    onCancel();
  }
}

// Add/remove event listener based on visibility
watch(() => props.visible, (newValue) => {
  if (newValue) {
    document.addEventListener('keydown', handleKeydown);
  } else {
    document.removeEventListener('keydown', handleKeydown);
  }
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown);
});
</script>

<style scoped>
/* Styles are in main.css */
</style>
