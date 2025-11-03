<template>
  <button 
    class="footer-btn" 
    @click="$emit('toggle')"
    :title="`Switch to ${isDarkTheme ? 'light' : 'dark'} theme`"
  >
    {{ isDarkTheme ? '☀' : '🌙' }} {{ isDarkTheme ? 'Light' : 'Dark' }}
  </button>
</template>

<script setup lang="ts">
defineProps<{
  isDarkTheme: boolean;
}>();

defineEmits<{
  toggle: [];
}>();
</script>

<style scoped>
/* Styles are in main.css */
</style>

