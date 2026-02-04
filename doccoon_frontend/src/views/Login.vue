<template>
    <div
        class="relative flex items-center justify-center min-h-screen bg-[var(--bg-color)] text-[var(--text-color)] p-5"
    >
        <div class="w-full max-w-[420px]">
            <!-- Header -->
            <div class="text-center mb-10">
                <router-link
                    to="/"
                    class="inline-block no-underline hover:opacity-70 transition-opacity duration-200"
                >
                    <img
                        :src="isDarkTheme ? logoDark : logoLight"
                        alt="Doccoon"
                        class="h-16 mx-auto"
                    />
                </router-link>
                <p class="mt-3 text-sm text-[var(--text-color)] opacity-60">
                    Sign in to your account
                </p>
            </div>

            <!-- Social Auth -->
            <div class="flex flex-col gap-3 mb-6">
                <button
                    class="flex items-center justify-center gap-3 w-full px-4 py-2.5 rounded-md border border-[var(--border-color)] bg-[var(--page-bg)] text-[var(--text-color)] text-sm font-medium cursor-pointer transition-all duration-200 hover:border-primary/40 hover:shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                    :disabled="isAnyLoading"
                    @click="handleGoogleLogin"
                >
                    <BaseIcon name="google" :size="18" />
                    Continue with Google
                </button>
                <button
                    class="flex items-center justify-center gap-3 w-full px-4 py-2.5 rounded-md border border-[var(--border-color)] bg-[var(--page-bg)] text-[var(--text-color)] text-sm font-medium cursor-pointer transition-all duration-200 hover:border-primary/40 hover:shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                    :disabled="isAnyLoading"
                    @click="handleGithubLogin"
                >
                    <BaseIcon name="github" :size="18" />
                    Continue with GitHub
                </button>
            </div>

            <!-- Divider -->
            <div class="flex items-center gap-4 mb-6">
                <div class="flex-1 h-px bg-[var(--border-color)]" />
                <span
                    class="text-xs text-[var(--text-color)] opacity-40 uppercase tracking-wider"
                    >or</span
                >
                <div class="flex-1 h-px bg-[var(--border-color)]" />
            </div>

            <!-- Login Form -->
            <form class="flex flex-col gap-4" @submit.prevent="handleLogin">
                <div class="flex flex-col gap-1.5">
                    <label
                        for="email"
                        class="text-xs font-medium text-[var(--text-color)] opacity-70"
                        >Email</label
                    >
                    <div class="relative">
                        <BaseIcon
                            name="mail"
                            :size="16"
                            class="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--text-color)] opacity-40"
                        />
                        <input
                            id="email"
                            v-model="email"
                            type="email"
                            placeholder="you@example.com"
                            required
                            autocomplete="email"
                            class="w-full pl-9 pr-3 py-2.5 rounded-md border border-[var(--border-color)] bg-[var(--page-bg)] text-[var(--text-color)] text-sm outline-none transition-all duration-200 focus:border-primary focus:ring-1 focus:ring-primary/30 placeholder:text-[var(--placeholder-color)]"
                        />
                    </div>
                </div>

                <div class="flex flex-col gap-1.5">
                    <div class="flex items-center justify-between">
                        <label
                            for="password"
                            class="text-xs font-medium text-[var(--text-color)] opacity-70"
                            >Password</label
                        >
                        <router-link
                            to="/forgot-password"
                            class="text-xs text-primary no-underline hover:underline"
                            >Forgot password?</router-link
                        >
                    </div>
                    <div class="relative">
                        <BaseIcon
                            name="lock"
                            :size="16"
                            class="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--text-color)] opacity-40"
                        />
                        <input
                            id="password"
                            v-model="password"
                            type="password"
                            placeholder="Enter your password"
                            required
                            autocomplete="current-password"
                            class="w-full pl-9 pr-3 py-2.5 rounded-md border border-[var(--border-color)] bg-[var(--page-bg)] text-[var(--text-color)] text-sm outline-none transition-all duration-200 focus:border-primary focus:ring-1 focus:ring-primary/30 placeholder:text-[var(--placeholder-color)]"
                        />
                    </div>
                </div>

                <!-- Error Message -->
                <div
                    v-if="errorMessage"
                    class="text-xs text-danger leading-relaxed bg-danger/10 border border-danger/20 rounded-md px-3 py-2"
                >
                    {{ errorMessage }}
                </div>

                <BaseButton
                    variant="primary"
                    size="lg"
                    class="w-full mt-1"
                    :disabled="isAnyLoading"
                >
                    {{ isAnyLoading ? "Signing in..." : "Sign In" }}
                </BaseButton>
            </form>

            <!-- Footer -->
            <p
                class="text-center mt-8 text-sm text-[var(--text-color)] opacity-60"
            >
                Don't have an account?
                <router-link
                    to="/register"
                    class="text-primary no-underline font-medium hover:underline"
                    >Sign up</router-link
                >
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import BaseButton from "@/components/ui/BaseButton.vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import { useTheme } from "@/composables/useTheme";
import { useOAuth } from "@/composables/useOAuth";
import { login } from "@/api/auth";
import logoLight from "@/assets/logo-light.png";
import logoDark from "@/assets/logo-dark.png";
import type { ApiResponse } from "@/api/client";

const router = useRouter();
const { isDarkTheme } = useTheme();
const {
    isLoading: isOAuthLoading,
    errorMessage: oauthError,
    handleGoogle,
    handleGithub,
} = useOAuth();

const email = ref("");
const password = ref("");
const isLoading = ref(false);
const errorMessage = ref("");

const isAnyLoading = computed(() => isLoading.value || isOAuthLoading.value);

async function handleLogin() {
    errorMessage.value = "";
    isLoading.value = true;

    try {
        await login({ email: email.value, password: password.value });
        router.push("/edit");
    } catch (err: unknown) {
        const apiErr = err as ApiResponse<unknown>;
        errorMessage.value =
            apiErr?.message ||
            "Failed to sign in. Please check your credentials.";
    } finally {
        isLoading.value = false;
    }
}

async function handleGoogleLogin() {
    await handleGoogle();
    errorMessage.value = oauthError.value;
}

async function handleGithubLogin() {
    await handleGithub();
    errorMessage.value = oauthError.value;
}
</script>
