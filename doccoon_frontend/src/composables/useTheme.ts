import { computed, watch, onMounted } from "vue";
import { useSettings } from "./useSettings";

/**
 * Theme management composable.
 *
 * - For authenticated users: persists to backend via useSettings
 * - For unauthenticated users: uses in-memory state (no persistence)
 * - Applies theme to DOM and manages highlight.js theme switching
 */
export function useTheme() {
  const { theme, setTheme, isInitialized, fetchSettings } = useSettings();

  /**
   * Apply current theme to the DOM
   */
  function applyTheme() {
    const isDark = theme.value === "dark";

    if (isDark) {
      document.body.classList.add("dark-theme");
    } else {
      document.body.classList.remove("dark-theme");
    }

    // Update highlight.js theme
    const lightTheme = document.getElementById("highlight-light");
    const darkTheme = document.getElementById("highlight-dark");

    if (lightTheme && darkTheme) {
      if (isDark) {
        lightTheme.setAttribute("disabled", "true");
        darkTheme.removeAttribute("disabled");
      } else {
        lightTheme.removeAttribute("disabled");
        darkTheme.setAttribute("disabled", "true");
      }
    }
  }

  /**
   * Toggle between light and dark theme
   */
  function toggleTheme() {
    const newTheme = theme.value === "dark" ? "light" : "dark";
    setTheme(newTheme);
  }

  /**
   * Check if dark theme is active
   */
  const isDarkTheme = computed(() => theme.value === "dark");

  // Watch for theme changes and apply
  watch(theme, () => {
    applyTheme();
  });

  // Watch for settings initialization
  watch(isInitialized, (initialized) => {
    if (initialized) {
      applyTheme();
    }
  });

  onMounted(async () => {
    // Fetch settings from backend (or use defaults for unauthenticated)
    await fetchSettings();
    applyTheme();
  });

  return {
    isDarkTheme,
    toggleTheme,
  };
}
