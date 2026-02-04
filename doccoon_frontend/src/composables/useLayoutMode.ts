import { computed } from "vue";
import { useSettings } from "./useSettings";

export type LayoutMode = "book" | "page";

/**
 * Layout mode management composable.
 *
 * - For authenticated users: persists to backend via useSettings
 * - For unauthenticated users: uses in-memory state (no persistence)
 * - Manages book (spread) vs page (single) view layout
 */
export function useLayoutMode() {
  const { layoutMode, setLayoutMode: setLayoutModeSetting } = useSettings();

  /**
   * Reactive layout mode state
   */
  const currentLayoutMode = computed(() => layoutMode.value);

  /**
   * Check if in book view mode
   */
  const isBookView = computed(() => layoutMode.value === "book");

  /**
   * Check if in page view mode
   */
  const isPageView = computed(() => layoutMode.value === "page");

  /**
   * Toggle between book and page view
   */
  function toggleLayoutMode() {
    const newMode = layoutMode.value === "book" ? "page" : "book";
    setLayoutModeSetting(newMode);
  }

  /**
   * Set layout mode to a specific value
   */
  function setLayoutMode(mode: LayoutMode) {
    setLayoutModeSetting(mode);
  }

  return {
    layoutMode: currentLayoutMode,
    isBookView,
    isPageView,
    toggleLayoutMode,
    setLayoutMode,
  };
}
