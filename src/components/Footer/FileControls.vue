<template>
  <div class="footer-section">
    <input
      type="text"
      class="filename-input"
      :value="filename"
      @input="onFilenameChange"
      placeholder="Enter filename..."
      title="Book filename"
    />
    
    <div class="footer-separator"></div>
    
    <button 
      class="footer-btn" 
      @click="$emit('new')"
      title="Create new book"
    >
      New
    </button>
    
    <button 
      class="footer-btn delete-btn" 
      @click="$emit('delete-page')"
      title="Delete current spread"
    >
      Delete Page
    </button>
    
    <button 
      class="footer-btn delete-btn" 
      @click="$emit('delete-book')"
      title="Delete entire book"
    >
      Delete Book
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  filename: string;
}>();

const emit = defineEmits<{
  'update:filename': [string];
  'new': [];
  'delete-page': [];
  'delete-book': [];
}>();

function onFilenameChange(e: Event) {
  const target = e.target as HTMLInputElement;
  emit('update:filename', target.value);
}
</script>

<style scoped>
/* Styles are in main.css */
</style>

