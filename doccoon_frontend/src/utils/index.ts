/**
 * Utility functions - centralized exports
 */

export { logger } from "./logger";
export {
  STORAGE_KEYS,
  getItem,
  setItem,
  removeItem,
  clearKeys,
  authStorage,
} from "./storage";
export { escapeHtml, escapeRegExp } from "./html";
