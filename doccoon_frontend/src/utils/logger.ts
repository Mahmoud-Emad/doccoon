/**
 * Logger utility for consistent logging across the application.
 * In production, console statements are suppressed to improve performance
 * and prevent information leakage.
 */

const isDevelopment = import.meta.env.DEV;

export const logger = {
  /**
   * Log error messages.
   * In production, errors are suppressed from console but could be
   * sent to an error tracking service if configured.
   */
  error: (...args: unknown[]) => {
    if (isDevelopment) {
      console.error(...args);
    }
  },

  /**
   * Log warning messages
   */
  warn: (...args: unknown[]) => {
    if (isDevelopment) {
      console.warn(...args);
    }
  },

  /**
   * Log info messages
   */
  info: (...args: unknown[]) => {
    if (isDevelopment) {
      console.info(...args);
    }
  },

  /**
   * Log debug messages (only in development)
   */
  debug: (...args: unknown[]) => {
    if (isDevelopment) {
      console.log(...args);
    }
  },
};
