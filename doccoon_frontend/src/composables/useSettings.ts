import { ref, computed } from "vue";
import { getSettings, updateSettings } from "@/api/settings";
import { isAuthenticated } from "@/api/auth";
import { logger } from "@/utils/logger";
import type { UserSettings } from "@/types";

/**
 * Default settings for unauthenticated users or before settings are loaded.
 * These are kept in memory only - no localStorage.
 */
const DEFAULT_SETTINGS: Omit<UserSettings, "id"> = {
  auto_save_enabled: true,
  auto_save_interval: 2,
  notification_enabled: true,
  theme: "light",
  profile_visible: true,
  view_mode: false,
  layout_mode: "book",
  live_preview: false,
};

// Singleton state - shared across all component instances
const settings = ref<UserSettings | null>(null);
const isLoading = ref(false);
const isInitialized = ref(false);
const pendingUpdate = ref<Partial<UserSettings> | null>(null);
let updateTimeout: number | null = null;

// Debounce delay for batching multiple rapid updates
const UPDATE_DEBOUNCE_MS = 500;

/**
 * Centralized settings management composable.
 *
 * - For authenticated users: fetches from and syncs to backend
 * - For unauthenticated users: uses in-memory defaults (no persistence)
 * - Provides debounced updates to avoid excessive API calls
 */
export function useSettings() {
  /**
   * Get current theme, falling back to default if not loaded
   */
  const theme = computed(() => settings.value?.theme ?? DEFAULT_SETTINGS.theme);

  /**
   * Get current view mode, falling back to default if not loaded
   */
  const viewMode = computed(
    () => settings.value?.view_mode ?? DEFAULT_SETTINGS.view_mode,
  );

  /**
   * Get current layout mode, falling back to default if not loaded
   */
  const layoutMode = computed(
    () => settings.value?.layout_mode ?? DEFAULT_SETTINGS.layout_mode,
  );

  /**
   * Get current live preview setting, falling back to default if not loaded
   */
  const livePreview = computed(
    () => settings.value?.live_preview ?? DEFAULT_SETTINGS.live_preview,
  );

  /**
   * Get auto-save enabled setting
   */
  const autoSaveEnabled = computed(
    () => settings.value?.auto_save_enabled ?? DEFAULT_SETTINGS.auto_save_enabled,
  );

  /**
   * Get auto-save interval in seconds
   */
  const autoSaveInterval = computed(
    () => settings.value?.auto_save_interval ?? DEFAULT_SETTINGS.auto_save_interval,
  );

  /**
   * Fetch settings from backend.
   * For authenticated users only.
   */
  async function fetchSettings(): Promise<void> {
    if (!isAuthenticated()) {
      // Use defaults for unauthenticated users
      isInitialized.value = true;
      return;
    }

    isLoading.value = true;
    try {
      const result = await getSettings();
      settings.value = result;
      isInitialized.value = true;
    } catch (error) {
      logger.error("Failed to fetch settings:", error);
      // Keep using defaults on error
      isInitialized.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Update settings - debounced to batch rapid changes.
   * For authenticated users, syncs to backend.
   * For unauthenticated users, updates in-memory only.
   */
  function updateSettingsDebounced(partial: Partial<UserSettings>): void {
    // Merge with any pending updates
    pendingUpdate.value = { ...pendingUpdate.value, ...partial };

    // Apply immediately to local state for responsive UI
    if (settings.value) {
      settings.value = { ...settings.value, ...partial };
    } else {
      // Create settings object from defaults + partial
      settings.value = {
        id: 0,
        ...DEFAULT_SETTINGS,
        ...partial,
      };
    }

    // Debounce the backend sync
    if (updateTimeout) {
      clearTimeout(updateTimeout);
    }

    updateTimeout = window.setTimeout(() => {
      flushPendingUpdates();
    }, UPDATE_DEBOUNCE_MS);
  }

  /**
   * Flush pending updates to backend immediately.
   */
  async function flushPendingUpdates(): Promise<void> {
    if (!pendingUpdate.value || !isAuthenticated()) {
      pendingUpdate.value = null;
      return;
    }

    const updates = pendingUpdate.value;
    pendingUpdate.value = null;

    try {
      const result = await updateSettings(updates);
      settings.value = result;
    } catch (error) {
      logger.error("Failed to update settings:", error);
      // Settings are already applied locally, so UI stays responsive
      // Backend will be out of sync until next fetch
    }
  }

  /**
   * Set theme preference
   */
  function setTheme(value: "light" | "dark"): void {
    updateSettingsDebounced({ theme: value });
  }

  /**
   * Set view mode preference
   */
  function setViewMode(value: boolean): void {
    updateSettingsDebounced({ view_mode: value });
  }

  /**
   * Set layout mode preference
   */
  function setLayoutMode(value: "book" | "page"): void {
    updateSettingsDebounced({ layout_mode: value });
  }

  /**
   * Set live preview preference
   */
  function setLivePreview(value: boolean): void {
    updateSettingsDebounced({ live_preview: value });
  }

  /**
   * Reset settings state (call on logout)
   */
  function resetSettings(): void {
    settings.value = null;
    isInitialized.value = false;
    pendingUpdate.value = null;
    if (updateTimeout) {
      clearTimeout(updateTimeout);
      updateTimeout = null;
    }
  }

  return {
    // State
    settings,
    isLoading,
    isInitialized,

    // Computed getters
    theme,
    viewMode,
    layoutMode,
    livePreview,
    autoSaveEnabled,
    autoSaveInterval,

    // Actions
    fetchSettings,
    updateSettingsDebounced,
    flushPendingUpdates,
    setTheme,
    setViewMode,
    setLayoutMode,
    setLivePreview,
    resetSettings,
  };
}
