<template>
  <div v-if="visible" class="loading-screen" :class="{ hidden: !visible }">
    <div class="loading-content">
      <div class="loading-spinner"></div>
      <div class="loading-text">Loading Open Book...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  visible: boolean;
}>();
</script>

<style scoped>
/* Styles are in main.css */
</style>
