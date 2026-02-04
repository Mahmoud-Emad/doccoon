/**
 * API layer - centralized exports
 */

// Core client
export { api, setAuthToken, setRefreshToken, clearAuthToken } from "./client";
export type { ApiResponse, PaginatedResponse, RequestConfig } from "./client";

// Auth
export {
  login,
  register,
  loginWithGoogle,
  loginWithGithub,
  logout,
  isAuthenticated,
} from "./auth";

// Books
export {
  getBooks,
  getBook,
  createBook,
  updateBook,
  deleteBook,
  togglePublishBook,
} from "./books";
export type {
  CreateBookPayload,
  UpdateBookPayload,
  BookPage,
  BookInfo,
  BookDetail,
} from "./books";

// Pages
export { createPage, updatePage, deletePage } from "./pages";
export type { PageData, CreatePagePayload, UpdatePagePayload } from "./pages";

// Sharing
export {
  sharePage,
  unsharePage,
  getSharedPage,
  shareBook,
  unshareBook,
  getSharedBook,
} from "./sharing";
export type { ShareResponse, SharedPageData, SharedBookData } from "./sharing";

// Settings
export { getSettings, updateSettings } from "./settings";

// Notifications
export {
  getNotifications,
  markAsRead,
  markAllAsRead,
  deleteNotification,
} from "./notifications";

// Profile
export { getProfile, updateProfile } from "./profile";

// AI
export { refineContent } from "./ai";
export type { RefineRequest, RefineResponse } from "./ai";

// AI Keys
export { getAIKeys, createAIKey, updateAIKey, deleteAIKey } from "./ai-keys";
