<template>
  <button
    class="bg-transparent text-[var(--footer-text)] border-none border-r border-r-[rgba(0,0,0,0.1)] h-full px-3 text-xs font-normal whitespace-nowrap cursor-pointer transition-colors duration-150 hover:bg-[var(--footer-item-hover)] flex items-center gap-1.5"
    :title="`Switch to ${isDarkTheme ? 'light' : 'dark'} theme`"
    @click="$emit('toggle')"
  >
    <BaseIcon :name="isDarkTheme ? 'sun' : 'moon'" :size="14" />
    {{ isDarkTheme ? 'Light' : 'Dark' }}
  </button>
</template>

<script setup lang="ts">
import BaseIcon from '@/components/ui/BaseIcon.vue';

defineProps<{
  isDarkTheme: boolean;
}>();

defineEmits<{
  toggle: [];
}>();
</script>
