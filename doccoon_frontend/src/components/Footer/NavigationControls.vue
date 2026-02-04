<template>
  <div class="flex items-center h-full">
    <button
      class="bg-transparent text-[var(--footer-text)] border-none border-r border-r-[rgba(0,0,0,0.1)] h-full px-2.5 text-sm font-normal cursor-pointer transition-colors duration-150 hover:bg-[var(--footer-item-hover)] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-transparent"
      :disabled="!canGoPrevious"
      title="Previous spread"
      @click="$emit('prev')"
    >
      &larr;
    </button>

    <span class="text-[var(--footer-text)] text-xs px-3 min-w-[60px] text-center select-none font-normal h-full flex items-center border-r border-r-[rgba(0,0,0,0.1)]">
      Page {{ currentIndex + 1 }} / {{ totalPages }}
    </span>

    <button
      class="bg-transparent text-[var(--footer-text)] border-none border-r border-r-[rgba(0,0,0,0.1)] h-full px-2.5 text-sm font-normal cursor-pointer transition-colors duration-150 hover:bg-[var(--footer-item-hover)] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-transparent"
      :disabled="!canGoNext"
      title="Next spread"
      @click="$emit('next')"
    >
      &rarr;
    </button>

    <div class="w-px h-full bg-[rgba(0,0,0,0.1)]" />

    <button
      class="bg-transparent text-[var(--footer-text)] border-none border-r border-r-[rgba(0,0,0,0.1)] h-full px-3 text-xs font-normal whitespace-nowrap cursor-pointer transition-colors duration-150 hover:bg-[var(--footer-item-hover)]"
      title="Add new spread"
      @click="$emit('add')"
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
