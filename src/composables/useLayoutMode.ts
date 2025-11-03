import { ref, watch, onMounted } from 'vue';

const LAYOUT_MODE_KEY = 'openbook_layoutmode';

export type LayoutMode = 'book' | 'page';

export function useLayoutMode() {
  const layoutMode = ref<LayoutMode>('book');

  // Load saved layout mode from localStorage
  function loadLayoutMode() {
    try {
      const saved = localStorage.getItem(LAYOUT_MODE_KEY);
      if (saved === 'book' || saved === 'page') {
        layoutMode.value = saved;
      }
    } catch (error) {
      console.error('Failed to load layout mode:', error);
    }
  }

  // Save layout mode to localStorage
  function saveLayoutMode() {
    try {
      localStorage.setItem(LAYOUT_MODE_KEY, layoutMode.value);
    } catch (error) {
      console.error('Failed to save layout mode:', error);
    }
  }

  // Toggle between book and page view
  function toggleLayoutMode() {
    layoutMode.value = layoutMode.value === 'book' ? 'page' : 'book';
  }

  // Set specific layout mode
  function setLayoutMode(mode: LayoutMode) {
    layoutMode.value = mode;
  }

  // Computed properties for convenience
  const isBookView = () => layoutMode.value === 'book';
  const isPageView = () => layoutMode.value === 'page';

  // Watch for changes and save to localStorage
  watch(layoutMode, () => {
    saveLayoutMode();
  });

  // Load on mount
  onMounted(() => {
    loadLayoutMode();
  });

  return {
    layoutMode,
    isBookView,
    isPageView,
    toggleLayoutMode,
    setLayoutMode
  };
}

