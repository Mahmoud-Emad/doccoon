<template>
    <div class="flex items-center h-full">
        <input
            type="text"
            class="bg-transparent text-[var(--footer-text)] border-none border-r border-r-[rgba(0,0,0,0.1)] px-3 text-xs font-normal outline-none max-w-[200px] h-full transition-colors duration-150 hover:bg-[var(--footer-item-hover)] focus:bg-[var(--footer-item-hover)] placeholder:text-[var(--footer-text)] placeholder:opacity-60"
            :value="filename"
            placeholder="Enter filename..."
            title="Book filename"
            @input="onFilenameChange"
        />
    </div>
</template>

<script setup lang="ts">
defineProps<{
    filename: string;
}>();

const emit = defineEmits<{
    "update:filename": [string];
}>();

function onFilenameChange(e: Event) {
    const target = e.target as HTMLInputElement;
    emit("update:filename", target.value);
}
</script>
