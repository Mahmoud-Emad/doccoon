<template>
  <div
    class="w-1 bg-[var(--separator-color)] cursor-col-resize relative shrink-0 transition-all duration-200 hover:bg-[var(--separator-hover)] hover:w-1.5 active:bg-[var(--btn-bg)]"
    @mousedown="$emit('start-resize', $event)"
    @touchstart="$emit('start-resize', $event)"
  >
    <div class="w-full h-full" />
  </div>
</template>

<script setup lang="ts">
defineEmits<{
  'start-resize': [event: MouseEvent | TouchEvent];
}>();
</script>
