<template>
    <Teleport to="body">
        <Transition name="modal">
            <div
                v-if="visible"
                class="fixed inset-0 z-[10000] flex items-center justify-center bg-[var(--modal-overlay)] backdrop-blur-sm animate-fade-in"
                @click="handleOverlay"
            >
                <div
                    role="dialog"
                    aria-modal="true"
                    :aria-label="title || 'Dialog'"
                    :class="containerClasses"
                    @click.stop
                >
                    <div
                        v-if="title"
                        class="px-6 py-5 border-b border-[var(--border-color)]"
                    >
                        <h3
                            class="m-0 text-lg font-semibold text-[var(--text-color)]"
                        >
                            {{ title }}
                        </h3>
                    </div>

                    <div class="p-6 overflow-y-auto flex-1">
                        <slot />
                    </div>

                    <div
                        v-if="$slots.footer"
                        class="px-6 py-4 border-t border-[var(--border-color)] flex justify-end gap-3"
                    >
                        <slot name="footer" />
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
import { computed, watch, onUnmounted } from "vue";

const props = withDefaults(
    defineProps<{
        visible: boolean;
        title?: string;
        size?: "sm" | "md" | "lg" | "xl" | "full";
        closeOnOverlay?: boolean;
    }>(),
    {
        title: "",
        size: "md",
        closeOnOverlay: true,
    },
);

const emit = defineEmits<{
    close: [];
}>();

const sizeClasses: Record<string, string> = {
    sm: "max-w-sm",
    md: "max-w-lg",
    lg: "max-w-2xl",
    xl: "max-w-5xl",
    full: "max-w-[95vw] max-h-[95vh]",
};

const containerClasses = computed(() => {
    return [
        "bg-[var(--page-bg)] rounded-lg shadow-[0_8px_32px_rgba(0,0,0,0.2)] w-[90%] max-h-[90vh] overflow-hidden flex flex-col animate-slide-in",
        sizeClasses[props.size] ?? sizeClasses.md,
    ].join(" ");
});

function handleOverlay() {
    if (props.closeOnOverlay) {
        emit("close");
    }
}

function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Escape" && props.visible) {
        emit("close");
    }
}

watch(
    () => props.visible,
    (val) => {
        if (val) {
            document.addEventListener("keydown", handleKeydown);
        } else {
            document.removeEventListener("keydown", handleKeydown);
        }
    },
);

onUnmounted(() => {
    document.removeEventListener("keydown", handleKeydown);
});
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}
</style>
