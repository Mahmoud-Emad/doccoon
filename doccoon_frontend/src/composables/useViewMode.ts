import { computed, watch } from "vue";
import { useSettings } from "./useSettings";

/**
 * View mode management composable.
 *
 * - For authenticated users: persists to backend via useSettings
 * - For unauthenticated users: uses in-memory state (no persistence)
 * - Manages edit/view mode for the editor
 */
export function useViewMode() {
  const { viewMode, setViewMode: setViewModeSetting } = useSettings();

  /**
   * Reactive view mode state
   */
  const isViewMode = computed(() => viewMode.value);

  /**
   * Apply view mode class to body
   */
  function applyViewMode() {
    if (viewMode.value) {
      document.body.classList.add("view-mode");
    } else {
      document.body.classList.remove("view-mode");
    }
  }

  /**
   * Toggle between edit and view mode
   */
  function toggleViewMode() {
    setViewModeSetting(!viewMode.value);
  }

  /**
   * Set view mode to a specific value
   */
  function setViewMode(value: boolean) {
    setViewModeSetting(value);
  }

  // Watch for view mode changes and apply to DOM
  watch(viewMode, () => {
    applyViewMode();
  });

  return {
    isViewMode,
    toggleViewMode,
    setViewMode,
  };
}
