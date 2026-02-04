import { ref, computed, onMounted, onUnmounted } from "vue";
import {
  getNotifications,
  markAsRead,
  markAllAsRead,
} from "@/api/notifications";
import { isAuthenticated } from "@/api/auth";
import { useToast } from "./useToast";
import { NOTIFICATION_POLL_INTERVAL_MS } from "@/config/constants";
import type { Notification } from "@/types";

const notifications = ref<Notification[]>([]);
const loading = ref(false);
let pollInterval: ReturnType<typeof setInterval> | null = null;

export function useNotifications() {
  const toast = useToast();

  const unreadCount = computed(
    () => notifications.value.filter((n) => !n.is_read).length,
  );

  async function fetchNotifications() {
    if (!isAuthenticated()) return;
    loading.value = true;
    try {
      notifications.value = await getNotifications();
    } catch {
      // Silent fail for background polling - don't interrupt user
    } finally {
      loading.value = false;
    }
  }

  async function markRead(id: number) {
    try {
      await markAsRead(id);
      const n = notifications.value.find((n) => n.id === id);
      if (n) n.is_read = true;
    } catch {
      toast.error("Failed to mark notification as read");
    }
  }

  async function markAllRead() {
    try {
      await markAllAsRead();
      notifications.value.forEach((n) => (n.is_read = true));
    } catch {
      toast.error("Failed to mark all notifications as read");
    }
  }

  function startPolling() {
    if (pollInterval) return;
    fetchNotifications();
    pollInterval = setInterval(
      fetchNotifications,
      NOTIFICATION_POLL_INTERVAL_MS,
    );
  }

  function stopPolling() {
    if (pollInterval) {
      clearInterval(pollInterval);
      pollInterval = null;
    }
  }

  onMounted(() => {
    if (isAuthenticated()) {
      startPolling();
    }
  });

  onUnmounted(() => {
    stopPolling();
  });

  return {
    notifications,
    unreadCount,
    loading,
    fetchNotifications,
    markRead,
    markAllRead,
    startPolling,
    stopPolling,
  };
}
