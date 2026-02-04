<template>
    <span
        class="text-[var(--footer-text)] text-xs px-3 h-full flex items-center opacity-80 italic min-w-[80px]"
    >
        {{ status }}
    </span>
</template>

<script setup lang="ts">
defineProps<{
    status: "Loaded" | "Saving..." | "Saved" | "Error";
}>();
</script>
