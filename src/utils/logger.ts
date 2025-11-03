/**
 * Logger utility for consistent logging across the application
 * In production, console statements are suppressed to improve performance
 * and prevent information leakage
 */

const isDevelopment = import.meta.env.DEV;

export const logger = {
  /**
   * Log error messages
   * In production, these could be sent to an error tracking service
   */
  error: (...args: any[]) => {
    if (isDevelopment) {
      console.error(...args);
    }
    // TODO: In production, send to error tracking service (e.g., Sentry)
  },

  /**
   * Log warning messages
   */
  warn: (...args: any[]) => {
    if (isDevelopment) {
      console.warn(...args);
    }
  },

  /**
   * Log info messages
   */
  info: (...args: any[]) => {
    if (isDevelopment) {
      console.info(...args);
    }
  },

  /**
   * Log debug messages (only in development)
   */
  debug: (...args: any[]) => {
    if (isDevelopment) {
      console.log(...args);
    }
  }
};

