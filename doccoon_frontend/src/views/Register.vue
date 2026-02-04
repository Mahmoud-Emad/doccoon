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
                    Create your account
                </p>
            </div>

            <!-- Social Auth -->
            <div class="flex flex-col gap-3 mb-6">
                <button
                    class="flex items-center justify-center gap-3 w-full px-4 py-2.5 rounded-md border border-[var(--border-color)] bg-[var(--page-bg)] text-[var(--text-color)] text-sm font-medium cursor-pointer transition-all duration-200 hover:border-primary/40 hover:shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                    :disabled="isLoading"
                    @click="handleGoogleSignup"
                >
                    <BaseIcon name="google" :size="18" />
                    Continue with Google
                </button>
                <button
                    class="flex items-center justify-center gap-3 w-full px-4 py-2.5 rounded-md border border-[var(--border-color)] bg-[var(--page-bg)] text-[var(--text-color)] text-sm font-medium cursor-pointer transition-all duration-200 hover:border-primary/40 hover:shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                    :disabled="isLoading"
                    @click="handleGithubSignup"
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

            <!-- Register Form -->
            <form class="flex flex-col gap-4" @submit.prevent="handleRegister">
                <div class="grid grid-cols-2 gap-3">
                    <div class="flex flex-col gap-1.5">
                        <label
                            for="firstName"
                            class="text-xs font-medium text-[var(--text-color)] opacity-70"
                            >First name</label
                        >
                        <div class="relative">
                            <BaseIcon
                                name="user"
                                :size="16"
                                class="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--text-color)] opacity-40"
                            />
                            <input
                                id="firstName"
                                v-model="firstName"
                                type="text"
                                placeholder="John"
                                required
                                autocomplete="given-name"
                                class="w-full pl-9 pr-3 py-2.5 rounded-md border border-[var(--border-color)] bg-[var(--page-bg)] text-[var(--text-color)] text-sm outline-none transition-all duration-200 focus:border-primary focus:ring-1 focus:ring-primary/30 placeholder:text-[var(--placeholder-color)]"
                            />
                        </div>
                    </div>

                    <div class="flex flex-col gap-1.5">
                        <label
                            for="lastName"
                            class="text-xs font-medium text-[var(--text-color)] opacity-70"
                            >Last name</label
                        >
                        <input
                            id="lastName"
                            v-model="lastName"
                            type="text"
                            placeholder="Doe"
                            required
                            autocomplete="family-name"
                            class="w-full px-3 py-2.5 rounded-md border border-[var(--border-color)] bg-[var(--page-bg)] text-[var(--text-color)] text-sm outline-none transition-all duration-200 focus:border-primary focus:ring-1 focus:ring-primary/30 placeholder:text-[var(--placeholder-color)]"
                        />
                    </div>
                </div>

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
                    <label
                        for="password"
                        class="text-xs font-medium text-[var(--text-color)] opacity-70"
                        >Password</label
                    >
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
                            placeholder="At least 8 characters"
                            required
                            minlength="8"
                            autocomplete="new-password"
                            class="w-full pl-9 pr-3 py-2.5 rounded-md border border-[var(--border-color)] bg-[var(--page-bg)] text-[var(--text-color)] text-sm outline-none transition-all duration-200 focus:border-primary focus:ring-1 focus:ring-primary/30 placeholder:text-[var(--placeholder-color)]"
                        />
                    </div>
                </div>

                <div class="flex flex-col gap-1.5">
                    <label
                        for="confirmPassword"
                        class="text-xs font-medium text-[var(--text-color)] opacity-70"
                        >Confirm password</label
                    >
                    <div class="relative">
                        <BaseIcon
                            name="lock"
                            :size="16"
                            class="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--text-color)] opacity-40"
                        />
                        <input
                            id="confirmPassword"
                            v-model="confirmPassword"
                            type="password"
                            placeholder="Confirm your password"
                            required
                            autocomplete="new-password"
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
                    :disabled="isLoading"
                >
                    {{ isLoading ? "Creating account..." : "Create Account" }}
                </BaseButton>
            </form>

            <!-- Footer -->
            <p
                class="text-center mt-8 text-sm text-[var(--text-color)] opacity-60"
            >
                Already have an account?
                <router-link
                    to="/login"
                    class="text-primary no-underline font-medium hover:underline"
                    >Sign in</router-link
                >
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import BaseButton from "@/components/ui/BaseButton.vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import { useTheme } from "@/composables/useTheme";
import { useOAuth } from "@/composables/useOAuth";
import { register } from "@/api/auth";
import logoLight from "@/assets/logo-light.png";
import logoDark from "@/assets/logo-dark.png";
import type { ApiResponse } from "@/api/client";

const router = useRouter();
const { isDarkTheme } = useTheme();
const { errorMessage: oauthError, handleGoogle, handleGithub } = useOAuth();

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const isLoading = ref(false);
const errorMessage = ref("");

async function handleRegister() {
    errorMessage.value = "";

    if (password.value !== confirmPassword.value) {
        errorMessage.value = "Passwords do not match.";
        return;
    }

    if (password.value.length < 8) {
        errorMessage.value = "Password must be at least 8 characters.";
        return;
    }

    isLoading.value = true;

    try {
        await register({
            first_name: firstName.value,
            last_name: lastName.value,
            email: email.value,
            password: password.value,
        });
        router.push("/edit");
    } catch (err: unknown) {
        const apiErr = err as ApiResponse<unknown>;
        errorMessage.value =
            apiErr?.message || "Failed to create account. Please try again.";
    } finally {
        isLoading.value = false;
    }
}

async function handleGoogleSignup() {
    await handleGoogle();
    errorMessage.value = oauthError.value;
}

async function handleGithubSignup() {
    await handleGithub();
    errorMessage.value = oauthError.value;
}
</script>
