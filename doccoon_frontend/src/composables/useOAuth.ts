import { ref } from "vue";
import { useRouter } from "vue-router";
import { loginWithGoogle, loginWithGithub } from "@/api/auth";
import type { ApiResponse } from "@/api/client";
import {
  OAUTH_POPUP_TIMEOUT_MS,
  OAUTH_POPUP_CHECK_INTERVAL_MS,
  OAUTH_CONFIG,
  GOOGLE_CLIENT_ID,
  GITHUB_CLIENT_ID,
} from "@/config/constants";

export function useOAuth() {
  const router = useRouter();
  const isLoading = ref(false);
  const errorMessage = ref("");

  function waitForOAuthCallback(
    popup: Window,
    provider: string,
  ): Promise<string | null> {
    return new Promise((resolve) => {
      const interval = setInterval(() => {
        if (popup.closed) {
          clearInterval(interval);
          resolve(null);
        }
        try {
          const url = popup.location.href;
          if (url.includes("/auth/" + provider + "/callback")) {
            clearInterval(interval);

            let token: string | null = null;

            if (provider === "google") {
              const hash = popup.location.hash;
              const params = new URLSearchParams(hash.substring(1));
              token = params.get("access_token");
            } else {
              const params = new URLSearchParams(popup.location.search);
              token = params.get("code");
            }

            popup.close();
            resolve(token);
          }
        } catch {
          // Cross-origin - popup hasn't redirected back yet
        }
      }, OAUTH_POPUP_CHECK_INTERVAL_MS);

      setTimeout(() => {
        clearInterval(interval);
        if (!popup.closed) popup.close();
        resolve(null);
      }, OAUTH_POPUP_TIMEOUT_MS);
    });
  }

  function openPopup(authUrl: string, name: string): Window | null {
    const config =
      name === "google-auth" ? OAUTH_CONFIG.google : OAUTH_CONFIG.github;
    const popup = window.open(authUrl, name, config.popupFeatures);
    if (!popup) {
      errorMessage.value = "Popup blocked. Please allow popups for this site.";
      isLoading.value = false;
    }
    return popup;
  }

  async function handleGoogle() {
    errorMessage.value = "";
    isLoading.value = true;

    try {
      if (!GOOGLE_CLIENT_ID) {
        errorMessage.value = "Google login is not configured.";
        isLoading.value = false;
        return;
      }

      const redirectUri = `${window.location.origin}/auth/google/callback`;
      const { scope, responseType } = OAUTH_CONFIG.google;
      const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${encodeURIComponent(redirectUri)}&response_type=${responseType}&scope=${encodeURIComponent(scope)}`;

      const popup = openPopup(authUrl, "google-auth");
      if (!popup) return;

      const token = await waitForOAuthCallback(popup, "google");
      if (token) {
        await loginWithGoogle({ access_token: token });
        router.push("/edit");
      }
    } catch (err: unknown) {
      const apiErr = err as ApiResponse<unknown>;
      errorMessage.value = apiErr?.message || "Failed to sign in with Google.";
    } finally {
      isLoading.value = false;
    }
  }

  async function handleGithub() {
    errorMessage.value = "";
    isLoading.value = true;

    try {
      if (!GITHUB_CLIENT_ID) {
        errorMessage.value = "GitHub login is not configured.";
        isLoading.value = false;
        return;
      }

      const redirectUri = `${window.location.origin}/auth/github/callback`;
      const { scope } = OAUTH_CONFIG.github;
      const authUrl = `https://github.com/login/oauth/authorize?client_id=${GITHUB_CLIENT_ID}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scope)}`;

      const popup = openPopup(authUrl, "github-auth");
      if (!popup) return;

      const token = await waitForOAuthCallback(popup, "github");
      if (token) {
        await loginWithGithub({ access_token: token });
        router.push("/edit");
      }
    } catch (err: unknown) {
      const apiErr = err as ApiResponse<unknown>;
      errorMessage.value = apiErr?.message || "Failed to sign in with GitHub.";
    } finally {
      isLoading.value = false;
    }
  }

  return {
    isLoading,
    errorMessage,
    handleGoogle,
    handleGithub,
  };
}
