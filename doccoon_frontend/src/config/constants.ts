/**
 * Application-wide constants and configuration values.
 *
 * Centralizes all magic numbers and configuration to make the codebase
 * easier to maintain and modify.
 */

// ============================================
// Timing Constants (in milliseconds)
// ============================================

/** Debounce delay for auto-save functionality */
export const AUTO_SAVE_DEBOUNCE_MS = 2000;

/** Interval for polling notifications from backend */
export const NOTIFICATION_POLL_INTERVAL_MS = 60000;

/** Duration to show "Saved" status before resetting */
export const SAVE_STATUS_RESET_DELAY_MS = 2000;

/** Timeout for OAuth popup before giving up */
export const OAUTH_POPUP_TIMEOUT_MS = 120000;

/** Interval for checking OAuth popup state */
export const OAUTH_POPUP_CHECK_INTERVAL_MS = 200;

/** Delay before resetting upload progress indicator */
export const UPLOAD_PROGRESS_RESET_DELAY_MS = 500;

/** Duration for code copy button feedback */
export const COPY_BUTTON_FEEDBACK_MS = 2000;

// ============================================
// Image Constants
// ============================================

/** Maximum file size for uploaded images (5MB) */
export const MAX_IMAGE_FILE_SIZE = 5 * 1024 * 1024;

/** Maximum dimension (width/height) before image compression */
export const MAX_IMAGE_DIMENSION = 2000;

/** JPEG compression quality (0-1) */
export const IMAGE_COMPRESSION_QUALITY = 0.85;

/** Maximum total storage for images in localStorage (8MB) */
export const MAX_IMAGE_STORAGE_SIZE = 8 * 1024 * 1024;

/** Supported image MIME types */
export const SUPPORTED_IMAGE_FORMATS = [
  "image/png",
  "image/jpeg",
  "image/jpg",
  "image/gif",
  "image/svg+xml",
  "image/webp",
] as const;

// ============================================
// UI Constants
// ============================================

/** Minimum flex width for resizable panels */
export const MIN_PANEL_FLEX_WIDTH = 0.2;

/** Default toast duration for info/success messages */
export const DEFAULT_TOAST_DURATION_MS = 4000;

/** Default toast duration for error messages */
export const ERROR_TOAST_DURATION_MS = 6000;

// ============================================
// OAuth Configuration
// ============================================

export const OAUTH_CONFIG = {
  google: {
    scope: "openid email profile",
    responseType: "token",
    popupFeatures: "width=500,height=600,menubar=no,toolbar=no",
  },
  github: {
    scope: "user:email",
    popupFeatures: "width=500,height=600,menubar=no,toolbar=no",
  },
} as const;

// ============================================
// API Configuration
// ============================================

/** Base URL for API requests */
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api";

/** Google OAuth client ID */
export const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID ?? "";

/** GitHub OAuth client ID */
export const GITHUB_CLIENT_ID = import.meta.env.VITE_GITHUB_CLIENT_ID ?? "";
