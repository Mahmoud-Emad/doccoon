import { ref } from "vue";
import {
  DEFAULT_TOAST_DURATION_MS,
  ERROR_TOAST_DURATION_MS,
} from "@/config/constants";

export interface Toast {
  id: number;
  message: string;
  type: "success" | "error" | "info";
}

const toasts = ref<Toast[]>([]);
let nextId = 0;

function addToast(
  message: string,
  type: Toast["type"] = "info",
  duration = DEFAULT_TOAST_DURATION_MS,
) {
  const id = nextId++;
  toasts.value.push({ id, message, type });

  if (duration > 0) {
    setTimeout(() => {
      removeToast(id);
    }, duration);
  }
}

function removeToast(id: number) {
  const index = toasts.value.findIndex((t) => t.id === id);
  if (index !== -1) {
    toasts.value.splice(index, 1);
  }
}

export function useToast() {
  return {
    toasts,
    success(message: string, duration?: number) {
      addToast(message, "success", duration);
    },
    error(message: string, duration?: number) {
      addToast(message, "error", duration ?? ERROR_TOAST_DURATION_MS);
    },
    info(message: string, duration?: number) {
      addToast(message, "info", duration);
    },
    remove: removeToast,
  };
}
