<template>
  <footer class="footer">
    <div class="footer-left">
      <NavigationControls :current-index="currentIndex" :total-pages="totalPages" :can-go-previous="canGoPrevious"
        :can-go-next="canGoNext" @prev="$emit('prev')" @next="$emit('next')" @add="$emit('add')" />

      <div class="footer-separator"></div>

      <FileControls :filename="filename" @update:filename="$emit('update:filename', $event)" @new="$emit('new')"
        @delete-page="$emit('delete-page')" @delete-book="$emit('delete-book')" />
    </div>

    <div class="footer-right">
      <StatusIndicator :status="status" />

      <div class="footer-separator"></div>

      <button class="footer-btn" @click="$emit('toggle-layout')"
        :title="`Switch to ${layoutMode === 'book' ? 'page' : 'book'} view`">
        {{ layoutMode === 'book' ? 'Page View' : 'Book View' }}
      </button>

      <div class="footer-separator"></div>

      <button class="footer-btn" @click="$emit('toggle-view')"
        :title="`Switch to ${isViewMode ? 'edit' : 'view'} mode`">
        {{ isViewMode ? 'Edit' : 'View' }}
      </button>

      <div class="footer-separator"></div>

      <ThemeToggle :is-dark-theme="isDarkTheme" @toggle="$emit('toggle-theme')" />
    </div>
  </footer>
</template>

<script setup lang="ts">
import NavigationControls from './NavigationControls.vue';
import FileControls from './FileControls.vue';
import ThemeToggle from './ThemeToggle.vue';
import StatusIndicator from './StatusIndicator.vue';

defineProps<{
  currentIndex: number;
  totalPages: number;
  canGoPrevious: boolean;
  canGoNext: boolean;
  filename: string;
  status: 'Loaded' | 'Saving...' | 'Saved';
  isViewMode: boolean;
  isDarkTheme: boolean;
  layoutMode: 'book' | 'page';
}>();

defineEmits<{
  prev: [];
  next: [];
  add: [];
  'update:filename': [string];
  'new': [];
  'delete-page': [];
  'delete-book': [];
  'toggle-layout': [];
  'toggle-view': [];
  'toggle-theme': [];
}>();
</script>

<style scoped>
/* Styles are in main.css */
</style>
