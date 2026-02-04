<template>
    <Teleport to="body">
        <div class="fixed top-4 right-4 z-[10001] flex flex-col gap-2 max-w-[400px]">
            <TransitionGroup name="toast">
                <div
                    v-for="toast in toasts"
                    :key="toast.id"
                    class="flex items-start gap-3 px-4 py-3 rounded-lg shadow-[0_4px_12px_rgba(0,0,0,0.15)] border text-sm leading-relaxed cursor-pointer"
                    :class="toastClasses(toast.type)"
                    @click="remove(toast.id)"
                >
                    <BaseIcon
                        :name="toastIcon(toast.type)"
                        :size="16"
                        class="shrink-0 mt-0.5"
                    />
                    <span class="flex-1">{{ toast.message }}</span>
                </div>
            </TransitionGroup>
        </div>
    </Teleport>
</template>

<script setup lang="ts">
import { useToast } from "@/composables/useToast";
import BaseIcon from "@/components/ui/BaseIcon.vue";

const { toasts, remove } = useToast();

function toastClasses(type: string): string {
    switch (type) {
        case "success":
            return "bg-[var(--page-bg)] border-green-500/30 text-green-500";
        case "error":
            return "bg-[var(--page-bg)] border-red-500/30 text-red-500";
        default:
            return "bg-[var(--page-bg)] border-primary/30 text-primary";
    }
}

function toastIcon(type: string): string {
    switch (type) {
        case "success":
            return "check";
        case "error":
            return "x";
        default:
            return "info";
    }
}
</script>

<style scoped>
.toast-enter-active {
    transition: all 0.3s ease;
}
.toast-leave-active {
    transition: all 0.2s ease;
}
.toast-enter-from {
    opacity: 0;
    transform: translateX(30px);
}
.toast-leave-to {
    opacity: 0;
    transform: translateX(30px);
}
.toast-move {
    transition: transform 0.3s ease;
}
</style>
