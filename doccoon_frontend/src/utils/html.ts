/**
 * HTML utility functions for safe text handling.
 */

/**
 * Escape HTML special characters to prevent XSS.
 * Uses DOM-based escaping for reliability.
 */
export function escapeHtml(text: string): string {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Escape special regex characters in a string.
 * Useful for creating regex patterns from user input.
 */
export function escapeRegExp(string: string): string {
  return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
