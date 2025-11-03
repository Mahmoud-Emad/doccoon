<template>
  <div 
    class="bookmark-separator" 
    @mousedown="onMouseDown"
    @touchstart="onTouchStart"
  >
    <div class="bookmark-ribbon"></div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  startResize: [MouseEvent];
}>();

function onMouseDown(e: MouseEvent) {
  emit('startResize', e);
}

function onTouchStart(e: TouchEvent) {
  // Convert touch to mouse event
  const touch = e.touches[0];
  const mouseEvent = new MouseEvent('mousedown', {
    clientX: touch.clientX,
    clientY: touch.clientY
  });
  emit('startResize', mouseEvent);
}
</script>

<style scoped>
/* Styles are in main.css */
</style>

