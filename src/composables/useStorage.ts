import { ref, watch, type Ref } from 'vue';
import type { Book } from '@/types';
import { logger } from '@/utils/logger';

const BOOK_DATA_KEY = 'openbook_data';
const SAVE_DEBOUNCE_MS = 300;

/**
 * Validate that data conforms to Book interface
 */
function isValidBook(data: any): data is Book {
  return (
    data &&
    typeof data === 'object' &&
    typeof data.filename === 'string' &&
    Array.isArray(data.spreads) &&
    data.spreads.every((spread: any) =>
      spread &&
      typeof spread.left === 'string' &&
      typeof spread.right === 'string' &&
      typeof spread.leftWidth === 'string' &&
      typeof spread.rightWidth === 'string'
    )
  );
}

export function useStorage(book: Ref<Book>, disableAutoSave?: Ref<boolean>) {
  const isSaving = ref(false);
  const saveStatus = ref<'Loaded' | 'Saving...' | 'Saved'>('Loaded');
  let saveTimeout: number | null = null;

  function saveBook(): boolean {
    try {
      localStorage.setItem(BOOK_DATA_KEY, JSON.stringify(book.value));
      return true;
    } catch (error) {
      logger.error('Failed to save book:', error);
      return false;
    }
  }

  function loadBook(): Book | null {
    try {
      const saved = localStorage.getItem(BOOK_DATA_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (isValidBook(parsed)) {
          return parsed;
        } else {
          logger.warn('Invalid book data in localStorage, clearing...');
          localStorage.removeItem(BOOK_DATA_KEY);
        }
      }
    } catch (error) {
      logger.error('Failed to load book:', error);
      // Clear corrupted data
      localStorage.removeItem(BOOK_DATA_KEY);
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

