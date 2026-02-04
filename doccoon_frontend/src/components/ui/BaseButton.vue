<template>
  <component
    :is="as"
    :class="buttonClasses"
    :disabled="disabled"
    v-bind="$attrs"
  >
    <slot />
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'footer';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
    icon?: boolean;
    as?: string;
  }>(),
  {
    variant: 'secondary',
    size: 'md',
    disabled: false,
    icon: false,
    as: 'button',
  }
);

const baseClasses = 'inline-flex items-center justify-center gap-2 cursor-pointer font-medium transition-all duration-200 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed select-none';

const variantClasses: Record<string, string> = {
  primary:
    'bg-primary text-white border-none rounded-md shadow-[0_4px_12px_rgba(0,122,204,0.3)] hover:translate-y-[-2px] hover:shadow-[0_6px_20px_rgba(0,122,204,0.4)] active:translate-y-0',
  secondary:
    'bg-transparent text-[var(--text-color)] border border-[var(--border-color)] rounded-md hover:border-primary hover:text-primary hover:bg-[rgba(0,122,204,0.05)]',
  ghost:
    'bg-transparent text-[var(--text-color)] border-none rounded hover:bg-[var(--border-color)]',
  danger:
    'bg-[var(--btn-delete-bg)] text-white border-none rounded-md hover:bg-[var(--btn-delete-hover)]',
  footer:
    'bg-transparent text-[var(--footer-text)] border-none border-r border-r-[rgba(0,0,0,0.1)] h-full px-3 text-xs font-normal whitespace-nowrap hover:bg-[var(--footer-item-hover)] rounded-none',
};

const sizeClasses: Record<string, string> = {
  sm: 'text-xs px-2 py-1',
  md: 'text-sm px-4 py-2',
  lg: 'text-base px-6 py-3',
};

const iconSizeClasses: Record<string, string> = {
  sm: 'w-7 h-7 p-0',
  md: 'w-10 h-10 p-0',
  lg: 'w-12 h-12 p-0',
};

const buttonClasses = computed(() => {
  const classes = [baseClasses, variantClasses[props.variant] ?? ''];
  if (props.icon) {
    classes.push(iconSizeClasses[props.size] ?? '');
  } else {
    classes.push(sizeClasses[props.size] ?? '');
  }
  return classes.join(' ');
});
</script>
