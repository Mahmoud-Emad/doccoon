/**
 * Centralized API client with automatic token refresh and request cancellation support.
 *
 * Features:
 * - Automatic JWT token management
 * - Token refresh on 401 responses
 * - Request cancellation via AbortController
 * - Consistent error handling
 */

import { authStorage } from "@/utils/storage";

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api";

export interface ApiResponse<T> {
  message: string;
  results: T | null;
  error?: unknown;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface RequestConfig {
  method: "GET" | "POST" | "PUT" | "DELETE";
  url: string;
  data?: unknown;
  headers?: Record<string, string>;
  signal?: AbortSignal;
}

interface RefreshResponse {
  access: string;
}

export function setAuthToken(token: string): void {
  authStorage.setAccessToken(token);
}

export function setRefreshToken(token: string): void {
  authStorage.setRefreshToken(token);
}

export function clearAuthToken(): void {
  authStorage.clear();
}

// Track if we're currently refreshing to avoid multiple refresh requests
let isRefreshing = false;
let refreshPromise: Promise<boolean> | null = null;

async function refreshAccessToken(): Promise<boolean> {
  const refreshToken = authStorage.getRefreshToken();
  if (!refreshToken) {
    return false;
  }

  try {
    const response = await fetch(`${BASE_URL}/auth/token/refresh/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (!response.ok) {
      return false;
    }

    const data: ApiResponse<RefreshResponse> = await response.json();
    if (data.results?.access) {
      authStorage.setAccessToken(data.results.access);
      return true;
    }
    return false;
  } catch {
    return false;
  }
}

async function handleTokenRefresh(): Promise<boolean> {
  // If already refreshing, wait for that request
  if (isRefreshing && refreshPromise) {
    return refreshPromise;
  }

  isRefreshing = true;
  refreshPromise = refreshAccessToken().finally(() => {
    isRefreshing = false;
    refreshPromise = null;
  });

  return refreshPromise;
}

// Auth endpoints that should not trigger token refresh/redirect on 401
const AUTH_ENDPOINTS = [
  "/auth/login/",
  "/auth/signup/",
  "/auth/token/refresh/",
];

function isAuthEndpoint(url: string): boolean {
  return AUTH_ENDPOINTS.some((endpoint) => url.includes(endpoint));
}

async function apiClient<T>(
  config: RequestConfig,
  isRetry = false,
): Promise<ApiResponse<T>> {
  const { method, url, data, headers = {}, signal } = config;

  const token = authStorage.getAccessToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const fetchOptions: RequestInit = {
    method,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
    signal,
  };

  if (data && method !== "GET") {
    fetchOptions.body = JSON.stringify(data);
  }

  const fullUrl = url.startsWith("http") ? url : `${BASE_URL}${url}`;

  const response = await fetch(fullUrl, fetchOptions);

  // Handle 401 - but skip token refresh logic for auth endpoints
  if (response.status === 401 && !isAuthEndpoint(url)) {
    if (!isRetry) {
      const refreshed = await handleTokenRefresh();
      if (refreshed) {
        // Retry the original request with new token
        return apiClient<T>(config, true);
      }
    }
    // Refresh failed or already retried, clear auth and redirect
    authStorage.clear();
    window.location.href = "/login";
    return { message: "Unauthorized", results: null };
  }

  const json: ApiResponse<T> = await response.json();
  if (!response.ok) {
    throw json;
  }

  return json;
}

/**
 * Fetch all pages of a paginated endpoint.
 * Useful for endpoints that return PaginatedResponse.
 */
async function fetchAllPaginated<T>(
  initialUrl: string,
  signal?: AbortSignal,
): Promise<T[]> {
  const allResults: T[] = [];
  let url: string | null = initialUrl.startsWith("http")
    ? initialUrl
    : `${BASE_URL}${initialUrl}`;

  while (url) {
    const token = authStorage.getAccessToken();
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(url, { headers, signal });

    if (response.status === 401) {
      const refreshed = await handleTokenRefresh();
      if (refreshed) {
        // Retry with new token
        continue;
      }
      authStorage.clear();
      window.location.href = "/login";
      return [];
    }

    if (!response.ok) {
      throw new Error(`Failed to fetch: ${response.statusText}`);
    }

    const data: PaginatedResponse<T> = await response.json();
    allResults.push(...data.results);
    url = data.next;
  }

  return allResults;
}

export const api = {
  get<T>(url: string, headers?: Record<string, string>, signal?: AbortSignal) {
    return apiClient<T>({ method: "GET", url, headers, signal });
  },

  post<T>(
    url: string,
    data?: unknown,
    headers?: Record<string, string>,
    signal?: AbortSignal,
  ) {
    return apiClient<T>({ method: "POST", url, data, headers, signal });
  },

  put<T>(
    url: string,
    data?: unknown,
    headers?: Record<string, string>,
    signal?: AbortSignal,
  ) {
    return apiClient<T>({ method: "PUT", url, data, headers, signal });
  },

  del<T>(url: string, headers?: Record<string, string>, signal?: AbortSignal) {
    return apiClient<T>({ method: "DELETE", url, headers, signal });
  },

  /**
   * Fetch all pages from a paginated endpoint.
   */
  getAllPaginated<T>(url: string, signal?: AbortSignal) {
    return fetchAllPaginated<T>(url, signal);
  },
};
