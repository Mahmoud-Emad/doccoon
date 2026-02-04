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
                    Reset your password
                </p>
            </div>

            <!-- Success State -->
            <div v-if="emailSent" class="text-center">
                <h2 class="text-lg font-semibold text-[var(--text-color)] mb-2">
                    Check your email
                </h2>
                <p class="text-sm text-[var(--text-color)] opacity-60 mb-6">
                    If an account exists for {{ email }}, you will receive a
                    password reset link shortly.
                </p>

                <!-- Resend button with countdown -->
                <div class="mb-6">
                    <button
                        v-if="resendCountdown > 0"
                        disabled
                        class="text-sm text-[var(--text-color)] opacity-40 cursor-not-allowed"
                    >
                        Resend email in {{ resendCountdown }}s
                    </button>
                    <button
                        v-else
                        class="text-sm text-primary font-medium cursor-pointer bg-transparent border-none hover:underline disabled:opacity-50"
                        :disabled="isLoading"
                        @click="handleResend"
                    >
                        {{ isLoading ? "Sending..." : "Resend email" }}
                    </button>
                </div>

                <div class="flex items-center justify-center gap-4">
                    <router-link
                        to="/login"
                        class="text-primary text-sm font-medium no-underline hover:underline"
                    >
                        Back to login
                    </router-link>
                    <span class="text-[var(--text-color)] opacity-30">|</span>
                    <router-link
                        to="/"
                        class="text-[var(--text-color)] opacity-60 text-sm no-underline hover:opacity-80"
                    >
                        Back to home
                    </router-link>
                </div>
            </div>

            <!-- Form State -->
            <template v-else>
                <p class="text-sm text-[var(--text-color)] opacity-60 mb-6">
                    Enter your email address and we'll send you a link to reset
                    your password.
                </p>

                <form
                    class="flex flex-col gap-4"
                    @submit.prevent="handleSubmit"
                >
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
                        {{ isLoading ? "Sending..." : "Send Reset Link" }}
                    </BaseButton>
                </form>

                <!-- Footer -->
                <div
                    class="flex items-center justify-center gap-4 mt-8 text-sm"
                >
                    <span class="text-[var(--text-color)] opacity-60">
                        Remember your password?
                        <router-link
                            to="/login"
                            class="text-primary no-underline font-medium hover:underline"
                            >Sign in</router-link
                        >
                    </span>
                    <span class="text-[var(--text-color)] opacity-30">|</span>
                    <router-link
                        to="/"
                        class="text-[var(--text-color)] opacity-60 no-underline hover:opacity-80"
                        >Back to home</router-link
                    >
                </div>
            </template>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from "vue";
import BaseButton from "@/components/ui/BaseButton.vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import { useTheme } from "@/composables/useTheme";
import { api, type ApiResponse } from "@/api/client";
import logoLight from "@/assets/logo-light.png";
import logoDark from "@/assets/logo-dark.png";

const { isDarkTheme } = useTheme();

const email = ref("");
const isLoading = ref(false);
const errorMessage = ref("");
const emailSent = ref(false);
const resendCountdown = ref(0);

let countdownInterval: ReturnType<typeof setInterval> | null = null;

function startCountdown() {
    resendCountdown.value = 60;
    countdownInterval = setInterval(() => {
        resendCountdown.value--;
        if (resendCountdown.value <= 0 && countdownInterval) {
            clearInterval(countdownInterval);
            countdownInterval = null;
        }
    }, 1000);
}

onUnmounted(() => {
    if (countdownInterval) {
        clearInterval(countdownInterval);
    }
});

async function handleSubmit() {
    errorMessage.value = "";
    isLoading.value = true;

    try {
        await api.post("/auth/password-reset/", { email: email.value });
        emailSent.value = true;
        startCountdown();
    } catch (err) {
        const apiErr = err as ApiResponse<unknown>;
        errorMessage.value =
            apiErr?.message || "Failed to send reset email. Please try again.";
    } finally {
        isLoading.value = false;
    }
}

async function handleResend() {
    isLoading.value = true;

    try {
        await api.post("/auth/password-reset/", { email: email.value });
        startCountdown();
    } catch {
        // Silently fail on resend
    } finally {
        isLoading.value = false;
    }
}
</script>
