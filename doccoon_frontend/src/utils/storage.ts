/**
 * Centralized localStorage utility for authentication tokens only.
 *
 * All user preferences (theme, view mode, layout mode, etc.) are now
 * stored on the backend and managed via useSettings composable.
 *
 * Only auth tokens remain in localStorage as they are required
 * to make authenticated API requests.
 */

import { logger } from "./logger";

// Storage keys - only auth tokens
export const STORAGE_KEYS = {
  ACCESS_TOKEN: "access_token",
  REFRESH_TOKEN: "refresh_token",
} as const;

export type StorageKey = (typeof STORAGE_KEYS)[keyof typeof STORAGE_KEYS];

/**
 * Get a string value from localStorage
 */
export function getItem(key: StorageKey): string | null {
  try {
    return localStorage.getItem(key);
  } catch (error) {
    logger.error(`Failed to get item from localStorage: ${key}`, error);
    return null;
  }
}

/**
 * Set a string value in localStorage
 */
export function setItem(key: StorageKey, value: string): boolean {
  try {
    localStorage.setItem(key, value);
    return true;
  } catch (error) {
    logger.error(`Failed to set item in localStorage: ${key}`, error);
    return false;
  }
}

/**
 * Remove an item from localStorage
 */
export function removeItem(key: StorageKey): boolean {
  try {
    localStorage.removeItem(key);
    return true;
  } catch (error) {
    logger.error(`Failed to remove item from localStorage: ${key}`, error);
    return false;
  }
}

/**
 * Clear multiple storage keys at once
 */
export function clearKeys(keys: StorageKey[]): void {
  keys.forEach((key) => removeItem(key));
}

/**
 * Auth-specific storage helpers
 */
export const authStorage = {
  getAccessToken: () => getItem(STORAGE_KEYS.ACCESS_TOKEN),
  setAccessToken: (token: string) => setItem(STORAGE_KEYS.ACCESS_TOKEN, token),
  getRefreshToken: () => getItem(STORAGE_KEYS.REFRESH_TOKEN),
  setRefreshToken: (token: string) =>
    setItem(STORAGE_KEYS.REFRESH_TOKEN, token),
  clear: () =>
    clearKeys([STORAGE_KEYS.ACCESS_TOKEN, STORAGE_KEYS.REFRESH_TOKEN]),
};
