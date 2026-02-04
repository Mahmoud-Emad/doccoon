<template>
    <footer
        class="flex justify-between items-center bg-[var(--footer-bg)] border-t border-[var(--footer-border)] h-[30px] text-xs transition-colors duration-300"
    >
        <div class="flex items-center flex-1 h-full">
            <NavigationControls
                :current-index="currentIndex"
                :total-pages="totalPages"
                :can-go-previous="canGoPrevious"
                :can-go-next="canGoNext"
                @prev="$emit('prev')"
                @next="$emit('next')"
                @add="$emit('add')"
            />

            <div class="w-px h-full bg-[rgba(0,0,0,0.1)]" />

            <FileControls
                :filename="filename"
                @update:filename="$emit('update:filename', $event)"
            />
        </div>

        <div class="flex items-center h-full">
            <StatusIndicator :status="status" />
        </div>
    </footer>
</template>

<script setup lang="ts">
import NavigationControls from "./NavigationControls.vue";
import FileControls from "./FileControls.vue";
import StatusIndicator from "./StatusIndicator.vue";

defineProps<{
    currentIndex: number;
    totalPages: number;
    canGoPrevious: boolean;
    canGoNext: boolean;
    filename: string;
    status: "Loaded" | "Saving..." | "Saved" | "Error";
}>();

defineEmits<{
    prev: [];
    next: [];
    add: [];
    "update:filename": [string];
}>();
</script>
