import { ref, watch, onMounted } from 'vue';

const VIEW_MODE_KEY = 'openbook_viewmode';

export function useViewMode() {
  const isViewMode = ref(false);

  function applyViewMode() {
    if (isViewMode.value) {
      document.body.classList.add('view-mode');
    } else {
      document.body.classList.remove('view-mode');
    }
  }

  function toggleViewMode() {
    isViewMode.value = !isViewMode.value;
  }

  function loadViewMode() {
    const saved = localStorage.getItem(VIEW_MODE_KEY);
    if (saved) {
      isViewMode.value = saved === 'true';
    }
  }

  function saveViewMode() {
    localStorage.setItem(VIEW_MODE_KEY, isViewMode.value.toString());
  }

  // Watch for view mode changes and apply
  watch(isViewMode, () => {
    applyViewMode();
    saveViewMode();
  });

  onMounted(() => {
    loadViewMode();
    applyViewMode();
  });

  function setViewMode(value: boolean) {
    isViewMode.value = value;
  }

  return {
    isViewMode,
    toggleViewMode,
    setViewMode
  };
}

