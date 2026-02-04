<template>
    <div class="relative" ref="dropdownRef">
        <button
            class="relative flex items-center justify-center w-8 h-8 bg-transparent border border-[var(--border-color)] rounded-md text-[var(--text-color)] cursor-pointer transition-colors duration-200 hover:bg-[var(--page-bg)]"
            :aria-expanded="isOpen"
            aria-haspopup="true"
            aria-label="Notifications"
            @click="isOpen = !isOpen"
        >
            <BaseIcon name="bell" :size="18" />
            <span
                v-if="unreadCount > 0"
                class="absolute -top-1 -right-1 flex items-center justify-center min-w-[16px] h-4 px-1 text-[10px] font-bold text-white bg-red-500 rounded-full leading-none"
            >
                {{ unreadCount > 99 ? "99+" : unreadCount }}
            </span>
        </button>

        <Transition
            enter-active-class="transition ease-out duration-150"
            enter-from-class="opacity-0 scale-95"
            enter-to-class="opacity-100 scale-100"
            leave-active-class="transition ease-in duration-100"
            leave-from-class="opacity-100 scale-100"
            leave-to-class="opacity-0 scale-95"
        >
            <div
                v-if="isOpen"
                class="absolute right-0 top-full mt-1 w-80 bg-[var(--page-bg)] border border-[var(--border-color)] rounded-lg shadow-[0_4px_12px_rgba(0,0,0,0.15)] z-[1000] overflow-hidden"
            >
                <div
                    class="flex items-center justify-between px-4 py-3 border-b border-[var(--border-color)]"
                >
                    <span class="text-sm font-semibold text-[var(--text-color)]"
                        >Notifications</span
                    >
                    <button
                        v-if="unreadCount > 0"
                        class="text-xs text-primary bg-transparent border-none cursor-pointer hover:underline"
                        @click="handleMarkAllRead"
                    >
                        Mark all as read
                    </button>
                </div>

                <div class="max-h-[320px] overflow-y-auto">
                    <div
                        v-if="notifications.length === 0"
                        class="py-8 text-center text-sm text-[var(--text-color)] opacity-50"
                    >
                        No notifications
                    </div>

                    <button
                        v-for="notification in notifications"
                        :key="notification.id"
                        class="w-full flex items-start gap-3 px-4 py-3 bg-transparent border-none text-left cursor-pointer transition-colors duration-150 hover:bg-[var(--section-alt-bg)]"
                        :class="{ 'opacity-60': notification.is_read }"
                        @click="handleNotificationClick(notification)"
                    >
                        <span
                            v-if="!notification.is_read"
                            class="mt-1.5 w-2 h-2 rounded-full bg-primary shrink-0"
                        />
                        <span v-else class="mt-1.5 w-2 h-2 shrink-0" />
                        <div class="min-w-0 flex-1">
                            <div
                                class="text-sm font-medium text-[var(--text-color)] truncate"
                            >
                                {{ notification.title }}
                            </div>
                            <div
                                class="text-xs text-[var(--text-color)] opacity-60 mt-0.5 line-clamp-2"
                            >
                                {{ notification.message }}
                            </div>
                            <div
                                class="text-[10px] text-[var(--text-color)] opacity-40 mt-1"
                            >
                                {{ formatTime(notification.created_at) }}
                            </div>
                        </div>
                    </button>
                </div>
            </div>
        </Transition>

        <!-- Notification Detail Dialog -->
        <NotificationDetailDialog
            :visible="detailDialogVisible"
            :notification="selectedNotification"
            @close="detailDialogVisible = false"
        />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import NotificationDetailDialog from "@/components/NotificationDetailDialog.vue";
import { useNotifications } from "@/composables/useNotifications";
import { useClickOutside } from "@/composables/useClickOutside";
import type { Notification } from "@/types";

const { notifications, unreadCount, markRead, markAllRead } =
    useNotifications();

const isOpen = ref(false);
const dropdownRef = ref<HTMLElement | null>(null);
const detailDialogVisible = ref(false);
const selectedNotification = ref<Notification | null>(null);

function handleNotificationClick(notification: Notification) {
    if (!notification.is_read) {
        markRead(notification.id);
    }
    // Open detail dialog
    selectedNotification.value = notification;
    detailDialogVisible.value = true;
    isOpen.value = false;
}

function handleMarkAllRead() {
    markAllRead();
}

function formatTime(dateStr: string): string {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMin = Math.floor(diffMs / 60000);
    const diffHr = Math.floor(diffMin / 60);
    const diffDay = Math.floor(diffHr / 24);

    if (diffMin < 1) return "Just now";
    if (diffMin < 60) return `${diffMin}m ago`;
    if (diffHr < 24) return `${diffHr}h ago`;
    if (diffDay < 7) return `${diffDay}d ago`;
    return date.toLocaleDateString();
}

useClickOutside(dropdownRef, () => {
    isOpen.value = false;
});

function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Escape" && isOpen.value) {
        isOpen.value = false;
    }
}

onMounted(() => document.addEventListener("keydown", handleKeydown));
onUnmounted(() => document.removeEventListener("keydown", handleKeydown));
</script>
