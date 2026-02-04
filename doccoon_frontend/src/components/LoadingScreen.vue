<template>
    <div
        v-if="visible"
        class="fixed inset-0 z-[9999] flex items-center justify-center bg-[var(--bg-color)] transition-opacity duration-300"
        :class="{ 'opacity-0 invisible': !visible }"
    >
        <div class="text-center">
            <div
                class="w-[50px] h-[50px] border-4 border-[var(--border-color)] border-t-[var(--btn-bg)] rounded-full animate-spin mx-auto mb-5"
            />
            <div class="text-[var(--text-color)] text-base font-medium">
                Loading Doccoon...
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    visible: boolean;
}>();
</script>
