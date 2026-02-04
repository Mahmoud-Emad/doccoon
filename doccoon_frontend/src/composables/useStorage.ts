import { ref, watch, type Ref } from "vue";
import type { Book } from "@/types";
import { logger } from "@/utils/logger";
import { isAuthenticated } from "@/api/auth";
import { createPage, updatePage } from "@/api/pages";
import {
  AUTO_SAVE_DEBOUNCE_MS,
  SAVE_STATUS_RESET_DELAY_MS,
} from "@/config/constants";

// Flag to suppress watcher re-triggers during save (when backfilling page IDs)
let isSavingInProgress = false;

/**
 * Save pages to the backend for a given book.
 * Each spread maps to 2 pages (left, right).
 * Backfills page IDs on spreads when new pages are created.
 */
async function saveToBackend(book: Book): Promise<boolean> {
  if (!book.id) return false;

  const bookId = book.id;
  isSavingInProgress = true;

  try {
    for (let i = 0; i < book.spreads.length; i++) {
      const spread = book.spreads[i];
      if (!spread) continue;

      const leftPageNum = i * 2 + 1;
      const rightPageNum = i * 2 + 2;

      // Save left page
      if (spread.leftPageId) {
        await updatePage(bookId, spread.leftPageId, {
          content: spread.left,
          page_number: leftPageNum,
        });
      } else {
        const created = await createPage(bookId, { content: spread.left });
        if (created) {
          spread.leftPageId = created.id;
        }
      }

      // Save right page
      if (spread.rightPageId) {
        await updatePage(bookId, spread.rightPageId, {
          content: spread.right,
          page_number: rightPageNum,
        });
      } else {
        const created = await createPage(bookId, { content: spread.right });
        if (created) {
          spread.rightPageId = created.id;
        }
      }
    }

    return true;
  } finally {
    isSavingInProgress = false;
  }
}

export type SaveStatus = "Loaded" | "Saving..." | "Saved" | "Error";

export function useStorage(
  book: Ref<Book>,
  disableAutoSave?: Ref<boolean>,
  saveIntervalMs?: Ref<number>,
) {
  const isSaving = ref(false);
  const saveStatus = ref<SaveStatus>("Loaded");
  let saveTimeout: number | null = null;

  function debouncedSave() {
    // Don't save if a save is mutating page IDs (would cause infinite loop)
    if (isSavingInProgress) {
      return;
    }

    // Don't save if auto-save is disabled or no book ID
    if (disableAutoSave?.value || !book.value.id) {
      return;
    }

    // Don't save if not authenticated
    if (!isAuthenticated()) {
      return;
    }

    if (saveTimeout) {
      clearTimeout(saveTimeout);
    }

    saveStatus.value = "Saving...";
    isSaving.value = true;

    const debounceMs = saveIntervalMs?.value ?? AUTO_SAVE_DEBOUNCE_MS;

    saveTimeout = window.setTimeout(async () => {
      try {
        await saveToBackend(book.value);
        saveStatus.value = "Saved";
      } catch (error) {
        logger.error("Failed to save to backend:", error);
        saveStatus.value = "Error";
      } finally {
        isSaving.value = false;
      }

      setTimeout(() => {
        if (saveStatus.value === "Saved") {
          saveStatus.value = "Loaded";
        }
      }, SAVE_STATUS_RESET_DELAY_MS);
    }, debounceMs);
  }

  // Auto-save on book changes
  watch(
    book,
    () => {
      debouncedSave();
    },
    { deep: true },
  );

  return {
    isSaving,
    saveStatus,
    debouncedSave,
  };
}
