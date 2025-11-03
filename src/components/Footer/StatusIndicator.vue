<template>
  <span class="footer-text status-text">
    {{ status }}
  </span>
</template>

<script setup lang="ts">
defineProps<{
  status: 'Loaded' | 'Saving...' | 'Saved';
}>();
</script>

<style scoped>
.status-text {
  font-size: 12px;
  opacity: 0.8;
}
</style>

