import { ref, watch, type Ref } from 'vue';
import type { Book } from '@/types';

const BOOK_DATA_KEY = 'openbook_data';
const SAVE_DEBOUNCE_MS = 300;

export function useStorage(book: Ref<Book>, disableAutoSave?: Ref<boolean>) {
  const isSaving = ref(false);
  const saveStatus = ref<'Loaded' | 'Saving...' | 'Saved'>('Loaded');
  let saveTimeout: number | null = null;

  function saveBook(): boolean {
    try {
      localStorage.setItem(BOOK_DATA_KEY, JSON.stringify(book.value));
      return true;
    } catch (error) {
      console.error('Failed to save book:', error);
      return false;
    }
  }

  function loadBook(): Book | null {
    try {
      const saved = localStorage.getItem(BOOK_DATA_KEY);
      if (saved) {
        return JSON.parse(saved);
      }
    } catch (error) {
      console.error('Failed to load book:', error);
    }
    return null;
  }

  function debouncedSave() {
    // Don't save if auto-save is disabled
    if (disableAutoSave?.value) {
      return;
    }

    if (saveTimeout) {
      clearTimeout(saveTimeout);
    }

    saveStatus.value = 'Saving...';
    isSaving.value = true;

    saveTimeout = window.setTimeout(() => {
      saveBook();
      saveStatus.value = 'Saved';
      isSaving.value = false;

      setTimeout(() => {
        if (saveStatus.value === 'Saved') {
          saveStatus.value = 'Loaded';
        }
      }, 2000);
    }, SAVE_DEBOUNCE_MS);
  }

  function deleteBook() {
    localStorage.removeItem(BOOK_DATA_KEY);
  }

  // Auto-save on book changes
  watch(book, () => {
    debouncedSave();
  }, { deep: true });

  return {
    isSaving,
    saveStatus,
    saveBook,
    loadBook,
    debouncedSave,
    deleteBook
  };
}

