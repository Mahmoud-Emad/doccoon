import { api, setAuthToken, setRefreshToken } from "./client";
import { authStorage } from "@/utils/storage";
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  SocialAuthRequest,
} from "@/types";

function storeTokens(data: AuthResponse): void {
  setAuthToken(data.access_token);
  setRefreshToken(data.refresh_token);
  // User profile data is fetched from API when needed, not cached in localStorage
}

export async function login(data: LoginRequest): Promise<AuthResponse> {
  const response = await api.post<AuthResponse>("/auth/login/", data);
  if (response.results) {
    storeTokens(response.results);
  }
  return response.results!;
}

export async function register(data: RegisterRequest): Promise<AuthResponse> {
  await api.post("/auth/signup/", data);
  // Auto-login after successful registration
  return login({ email: data.email, password: data.password });
}

export async function loginWithGoogle(
  data: SocialAuthRequest,
): Promise<AuthResponse> {
  const response = await api.post<AuthResponse>("/auth/social/google/", data);
  if (response.results) {
    storeTokens(response.results);
  }
  return response.results!;
}

export async function loginWithGithub(
  data: SocialAuthRequest,
): Promise<AuthResponse> {
  const response = await api.post<AuthResponse>("/auth/social/github/", data);
  if (response.results) {
    storeTokens(response.results);
  }
  return response.results!;
}

export function logout(): void {
  authStorage.clear();
  window.location.href = "/login";
}

export async function deleteAccount(): Promise<void> {
  await api.del("/auth/delete-account/");
  authStorage.clear();
}

export function isAuthenticated(): boolean {
  return !!authStorage.getAccessToken();
}
