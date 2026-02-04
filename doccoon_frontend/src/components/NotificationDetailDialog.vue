<template>
    <Teleport to="body">
        <Transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
        >
            <div
                v-if="visible"
                class="fixed inset-0 z-[1001] flex items-center justify-center p-4"
            >
                <!-- Backdrop -->
                <div
                    class="absolute inset-0 bg-black/40"
                    @click="$emit('close')"
                ></div>

                <!-- Dialog -->
                <Transition
                    enter-active-class="transition ease-out duration-200"
                    enter-from-class="opacity-0 scale-95 translate-y-2"
                    enter-to-class="opacity-100 scale-100 translate-y-0"
                    leave-active-class="transition ease-in duration-150"
                    leave-from-class="opacity-100 scale-100 translate-y-0"
                    leave-to-class="opacity-0 scale-95 translate-y-2"
                >
                    <div
                        v-if="visible"
                        class="relative w-full max-w-md bg-[var(--page-bg)] border border-[var(--border-color)] rounded-lg shadow-xl overflow-hidden"
                    >
                        <!-- Header -->
                        <div
                            class="px-5 py-4 border-b border-[var(--border-color)] bg-[var(--section-alt-bg)]/30"
                        >
                            <div class="flex items-start justify-between gap-4">
                                <div class="flex-1 min-w-0">
                                    <p
                                        class="text-[10px] font-medium text-[var(--text-color)] opacity-40 uppercase tracking-widest mb-1"
                                    >
                                        Notification
                                    </p>
                                    <h3
                                        class="text-base font-semibold text-[var(--text-color)] m-0 leading-tight"
                                    >
                                        {{ notification?.title }}
                                    </h3>
                                </div>
                                <button
                                    class="w-8 h-8 flex items-center justify-center rounded-md bg-transparent border border-[var(--border-color)] text-[var(--text-color)] opacity-60 cursor-pointer transition-all duration-200 hover:opacity-100 hover:bg-[var(--section-alt-bg)]"
                                    title="Close"
                                    @click="$emit('close')"
                                >
                                    <BaseIcon name="x" :size="14" />
                                </button>
                            </div>
                        </div>

                        <!-- Body -->
                        <div class="px-5 py-5">
                            <p
                                class="text-sm text-[var(--text-color)] opacity-80 leading-relaxed m-0 whitespace-pre-wrap"
                            >
                                {{ notification?.message }}
                            </p>
                        </div>

                        <!-- Footer -->
                        <div
                            class="flex items-center justify-between px-5 py-3 border-t border-[var(--border-color)] bg-[var(--section-alt-bg)]/30"
                        >
                            <span
                                class="text-xs text-[var(--text-color)] opacity-40"
                            >
                                {{ formattedDate }}
                            </span>
                            <button
                                class="px-4 py-2 text-sm font-medium text-[var(--text-color)] bg-transparent border border-[var(--border-color)] rounded-md cursor-pointer transition-all duration-200 hover:bg-[var(--section-alt-bg)]"
                                @click="$emit('close')"
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </Transition>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted } from "vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import type { Notification } from "@/types";

const props = defineProps<{
    visible: boolean;
    notification: Notification | null;
}>();

const emit = defineEmits<{
    close: [];
}>();

const formattedDate = computed(() => {
    if (!props.notification?.created_at) return "";
    const date = new Date(props.notification.created_at);
    return date.toLocaleDateString("en-US", {
        weekday: "short",
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
    });
});

function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Escape" && props.visible) {
        emit("close");
    }
}

onMounted(() => document.addEventListener("keydown", handleKeydown));
onUnmounted(() => document.removeEventListener("keydown", handleKeydown));
</script>
