import { onMounted, onUnmounted, ref } from "vue";

export interface KeyboardShortcut {
  key: string;
  ctrl?: boolean;
  shift?: boolean;
  alt?: boolean;
  meta?: boolean;
  description: string;
  category: "general" | "editing" | "navigation" | "view";
  action: () => void;
}

/**
 * Format a shortcut for display (e.g., "Ctrl+S", "Cmd+Shift+B")
 */
export function formatShortcut(shortcut: KeyboardShortcut): string {
  const isMac = navigator.platform.toUpperCase().indexOf("MAC") >= 0;
  const parts: string[] = [];

  if (shortcut.ctrl || shortcut.meta) {
    parts.push(isMac ? "⌘" : "Ctrl");
  }
  if (shortcut.alt) {
    parts.push(isMac ? "⌥" : "Alt");
  }
  if (shortcut.shift) {
    parts.push(isMac ? "⇧" : "Shift");
  }

  // Format the key nicely
  let keyDisplay = shortcut.key.toUpperCase();
  if (shortcut.key === "?") keyDisplay = "?";
  if (shortcut.key === "/") keyDisplay = "/";
  if (shortcut.key === "Escape") keyDisplay = "Esc";
  if (shortcut.key === "ArrowLeft") keyDisplay = "←";
  if (shortcut.key === "ArrowRight") keyDisplay = "→";
  if (shortcut.key === "ArrowUp") keyDisplay = "↑";
  if (shortcut.key === "ArrowDown") keyDisplay = "↓";

  parts.push(keyDisplay);

  return parts.join(isMac ? "" : "+");
}

/**
 * Composable for managing keyboard shortcuts
 */
export function useKeyboardShortcuts() {
  const shortcuts = ref<KeyboardShortcut[]>([]);
  const isHelpModalOpen = ref(false);

  function registerShortcut(shortcut: KeyboardShortcut) {
    // Check for duplicates
    const exists = shortcuts.value.some(
      (s) =>
        s.key === shortcut.key &&
        s.ctrl === shortcut.ctrl &&
        s.shift === shortcut.shift &&
        s.alt === shortcut.alt &&
        s.meta === shortcut.meta,
    );

    if (!exists) {
      shortcuts.value.push(shortcut);
    }
  }

  function unregisterShortcut(shortcut: Partial<KeyboardShortcut>) {
    shortcuts.value = shortcuts.value.filter(
      (s) =>
        !(
          s.key === shortcut.key &&
          s.ctrl === shortcut.ctrl &&
          s.shift === shortcut.shift &&
          s.alt === shortcut.alt &&
          s.meta === shortcut.meta
        ),
    );
  }

  function handleKeydown(event: KeyboardEvent) {
    // Don't trigger shortcuts when typing in inputs (except for specific shortcuts)
    const target = event.target as HTMLElement;
    const isInputField =
      target.tagName === "INPUT" ||
      target.tagName === "TEXTAREA" ||
      target.isContentEditable;

    for (const shortcut of shortcuts.value) {
      const ctrlOrMeta = event.ctrlKey || event.metaKey;
      const ctrlMatch = shortcut.ctrl ? ctrlOrMeta : !ctrlOrMeta;
      const shiftMatch = shortcut.shift ? event.shiftKey : !event.shiftKey;
      const altMatch = shortcut.alt ? event.altKey : !event.altKey;

      // Handle "?" key which requires shift
      let keyMatch = false;
      if (shortcut.key === "?") {
        keyMatch = event.key === "?" || (event.key === "/" && event.shiftKey);
      } else {
        keyMatch = event.key.toLowerCase() === shortcut.key.toLowerCase();
      }

      if (keyMatch && ctrlMatch && shiftMatch && altMatch) {
        // For input fields, only allow shortcuts with Ctrl/Cmd modifier
        if (isInputField && !shortcut.ctrl && !shortcut.meta) {
          continue;
        }

        event.preventDefault();
        shortcut.action();
        return;
      }
    }
  }

  function openHelpModal() {
    isHelpModalOpen.value = true;
  }

  function closeHelpModal() {
    isHelpModalOpen.value = false;
  }

  onMounted(() => {
    document.addEventListener("keydown", handleKeydown);
  });

  onUnmounted(() => {
    document.removeEventListener("keydown", handleKeydown);
    shortcuts.value = [];
  });

  return {
    shortcuts,
    isHelpModalOpen,
    registerShortcut,
    unregisterShortcut,
    openHelpModal,
    closeHelpModal,
    formatShortcut,
  };
}

/**
 * Text formatting utilities for textarea
 */
export function useTextFormatting(
  textareaRef: () => HTMLTextAreaElement | null,
  onUpdate: (newValue: string) => void,
) {
  function wrapSelection(before: string, after: string) {
    const textarea = textareaRef();
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;
    const selectedText = text.substring(start, end);

    // Check if already wrapped - if so, unwrap
    const beforeSelected = text.substring(
      Math.max(0, start - before.length),
      start,
    );
    const afterSelected = text.substring(end, end + after.length);

    if (beforeSelected === before && afterSelected === after) {
      // Unwrap
      const newText =
        text.substring(0, start - before.length) +
        selectedText +
        text.substring(end + after.length);
      onUpdate(newText);

      // Restore selection
      requestAnimationFrame(() => {
        textarea.focus();
        textarea.setSelectionRange(start - before.length, end - before.length);
      });
    } else {
      // Wrap
      const newText =
        text.substring(0, start) +
        before +
        selectedText +
        after +
        text.substring(end);
      onUpdate(newText);

      // Restore selection (inside the wrapper)
      requestAnimationFrame(() => {
        textarea.focus();
        textarea.setSelectionRange(start + before.length, end + before.length);
      });
    }
  }

  function insertAtCursor(text: string) {
    const textarea = textareaRef();
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const currentText = textarea.value;

    const newText =
      currentText.substring(0, start) + text + currentText.substring(end);
    onUpdate(newText);

    // Move cursor after inserted text
    requestAnimationFrame(() => {
      textarea.focus();
      textarea.setSelectionRange(start + text.length, start + text.length);
    });
  }

  function insertLinePrefix(prefix: string) {
    const textarea = textareaRef();
    if (!textarea) return;

    const start = textarea.selectionStart;
    const text = textarea.value;

    // Find the start of the current line
    let lineStart = start;
    while (lineStart > 0 && text[lineStart - 1] !== "\n") {
      lineStart--;
    }

    // Check if line already starts with prefix
    const linePrefix = text.substring(lineStart, lineStart + prefix.length);
    if (linePrefix === prefix) {
      // Remove prefix
      const newText =
        text.substring(0, lineStart) +
        text.substring(lineStart + prefix.length);
      onUpdate(newText);

      requestAnimationFrame(() => {
        textarea.focus();
        textarea.setSelectionRange(
          start - prefix.length,
          start - prefix.length,
        );
      });
    } else {
      // Add prefix
      const newText =
        text.substring(0, lineStart) + prefix + text.substring(lineStart);
      onUpdate(newText);

      requestAnimationFrame(() => {
        textarea.focus();
        textarea.setSelectionRange(
          start + prefix.length,
          start + prefix.length,
        );
      });
    }
  }

  return {
    bold: () => wrapSelection("**", "**"),
    italic: () => wrapSelection("*", "*"),
    strikethrough: () => wrapSelection("~~", "~~"),
    code: () => wrapSelection("`", "`"),
    codeBlock: () => wrapSelection("```\n", "\n```"),
    link: () => {
      const textarea = textareaRef();
      if (!textarea) return;

      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const text = textarea.value;
      const selectedText = text.substring(start, end);

      if (selectedText) {
        // Wrap selected text as link text
        const newText =
          text.substring(0, start) +
          `[${selectedText}](url)` +
          text.substring(end);
        onUpdate(newText);

        // Select "url" for easy replacement
        requestAnimationFrame(() => {
          textarea.focus();
          textarea.setSelectionRange(
            start + selectedText.length + 3,
            start + selectedText.length + 6,
          );
        });
      } else {
        // Insert link template
        insertAtCursor("[link text](url)");
      }
    },
    heading: (level: 1 | 2 | 3) => insertLinePrefix("#".repeat(level) + " "),
    bulletList: () => insertLinePrefix("- "),
    numberedList: () => insertLinePrefix("1. "),
    quote: () => insertLinePrefix("> "),
    insertAtCursor,
  };
}
