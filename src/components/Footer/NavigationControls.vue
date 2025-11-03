<template>
  <div class="footer-section">
    <button 
      class="footer-btn" 
      :disabled="!canGoPrevious"
      @click="$emit('prev')"
      title="Previous spread"
    >
      ←
    </button>
    
    <span class="footer-text">
      Page {{ currentIndex + 1 }} / {{ totalPages }}
    </span>
    
    <button 
      class="footer-btn" 
      :disabled="!canGoNext"
      @click="$emit('next')"
      title="Next spread"
    >
      →
    </button>
    
    <div class="footer-separator"></div>
    
    <button 
      class="footer-btn" 
      @click="$emit('add')"
      title="Add new spread"
    >
      + Add Page
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  currentIndex: number;
  totalPages: number;
  canGoPrevious: boolean;
  canGoNext: boolean;
}>();

defineEmits<{
  prev: [];
  next: [];
  add: [];
}>();
</script>

<style scoped>
/* Styles are in main.css */
</style>

