import { ref, watch, onMounted } from 'vue';

const THEME_KEY = 'openbook_theme';

export function useTheme() {
  const isDarkTheme = ref(false);
  
  function applyTheme() {
    if (isDarkTheme.value) {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
    
    // Update highlight.js theme
    const lightTheme = document.getElementById('highlight-light');
    const darkTheme = document.getElementById('highlight-dark');
    
    if (lightTheme && darkTheme) {
      if (isDarkTheme.value) {
        lightTheme.setAttribute('disabled', 'true');
        darkTheme.removeAttribute('disabled');
      } else {
        lightTheme.removeAttribute('disabled');
        darkTheme.setAttribute('disabled', 'true');
      }
    }
  }
  
  function toggleTheme() {
    isDarkTheme.value = !isDarkTheme.value;
  }
  
  function loadTheme() {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved) {
      isDarkTheme.value = saved === 'dark';
    }
  }
  
  function saveTheme() {
    localStorage.setItem(THEME_KEY, isDarkTheme.value ? 'dark' : 'light');
  }
  
  // Watch for theme changes and apply
  watch(isDarkTheme, () => {
    applyTheme();
    saveTheme();
  });
  
  onMounted(() => {
    loadTheme();
    applyTheme();
  });
  
  return {
    isDarkTheme,
    toggleTheme
  };
}

