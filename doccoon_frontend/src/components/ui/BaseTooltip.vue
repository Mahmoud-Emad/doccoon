<template>
  <div class="relative inline-flex group">
    <slot />
    <div
      v-if="text"
      class="absolute z-50 px-2.5 py-1.5 text-xs font-normal text-white bg-gray-900 rounded shadow-lg whitespace-nowrap opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 pointer-events-none"
      :class="positionClasses"
    >
      {{ text }}
      <div class="absolute w-2 h-2 bg-gray-900 rotate-45" :class="arrowClasses" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    text: string;
    position?: 'top' | 'bottom' | 'left' | 'right';
  }>(),
  {
    position: 'top',
  }
);

const positionClasses = computed(() => {
  switch (props.position) {
    case 'top':
      return 'bottom-full left-1/2 -translate-x-1/2 mb-2';
    case 'bottom':
      return 'top-full left-1/2 -translate-x-1/2 mt-2';
    case 'left':
      return 'right-full top-1/2 -translate-y-1/2 mr-2';
    case 'right':
      return 'left-full top-1/2 -translate-y-1/2 ml-2';
    default:
      return 'bottom-full left-1/2 -translate-x-1/2 mb-2';
  }
});

const arrowClasses = computed(() => {
  switch (props.position) {
    case 'top':
      return 'top-full left-1/2 -translate-x-1/2 -mt-1';
    case 'bottom':
      return 'bottom-full left-1/2 -translate-x-1/2 -mb-1';
    case 'left':
      return 'left-full top-1/2 -translate-y-1/2 -ml-1';
    case 'right':
      return 'right-full top-1/2 -translate-y-1/2 -mr-1';
    default:
      return 'top-full left-1/2 -translate-x-1/2 -mt-1';
  }
});
</script>
