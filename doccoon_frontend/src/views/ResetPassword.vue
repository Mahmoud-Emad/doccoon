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
                <p
                    v-if="!resetSuccess && !invalidToken"
                    class="mt-3 text-sm text-[var(--text-color)] opacity-60"
                >
                    Create a new password
                </p>
            </div>

            <!-- Success State -->
            <div v-if="resetSuccess" class="text-center">
                <h2 class="text-lg font-semibold text-[var(--text-color)] mb-2">
                    Password reset successful
                </h2>
                <p class="text-sm text-[var(--text-color)] opacity-60 mb-6">
                    Your password has been updated. You can now sign in with
                    your new password.
                </p>
                <router-link
                    to="/login"
                    class="inline-block px-6 py-2.5 text-sm font-medium text-white bg-primary rounded-md no-underline transition-opacity duration-200 hover:opacity-90"
                >
                    Sign in
                </router-link>
            </div>

            <!-- Invalid Token State -->
            <div v-else-if="invalidToken" class="text-center">
                <div
                    class="w-16 h-16 mx-auto mb-6 rounded-full bg-danger/10 flex items-center justify-center"
                >
                    <BaseIcon name="x" :size="32" class="text-danger" />
                </div>
                <h2 class="text-lg font-semibold text-[var(--text-color)] mb-2">
                    Invalid or expired link
                </h2>
                <p class="text-sm text-[var(--text-color)] opacity-60 mb-6">
                    This password reset link is invalid or has expired. Please
                    request a new one.
                </p>
                <router-link
                    to="/forgot-password"
                    class="inline-block px-6 py-2.5 text-sm font-medium text-white bg-primary rounded-md no-underline transition-opacity duration-200 hover:opacity-90"
                >
                    Request new link
                </router-link>
            </div>

            <!-- Form State -->
            <template v-else>
                <form
                    class="flex flex-col gap-4"
                    @submit.prevent="handleSubmit"
                >
                    <div class="flex flex-col gap-1.5">
                        <label
                            for="password"
                            class="text-xs font-medium text-[var(--text-color)] opacity-70"
                            >New Password</label
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
                                placeholder="Enter new password"
                                required
                                autocomplete="new-password"
                                class="w-full pl-9 pr-3 py-2.5 rounded-md border border-[var(--border-color)] bg-[var(--page-bg)] text-[var(--text-color)] text-sm outline-none transition-all duration-200 focus:border-primary focus:ring-1 focus:ring-primary/30 placeholder:text-[var(--placeholder-color)]"
                            />
                        </div>
                    </div>

                    <div class="flex flex-col gap-1.5">
                        <label
                            for="confirmPassword"
                            class="text-xs font-medium text-[var(--text-color)] opacity-70"
                            >Confirm Password</label
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
                                placeholder="Confirm new password"
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
                        {{ isLoading ? "Resetting..." : "Reset Password" }}
                    </BaseButton>
                </form>
            </template>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import BaseButton from "@/components/ui/BaseButton.vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import { useTheme } from "@/composables/useTheme";
import { api, type ApiResponse } from "@/api/client";
import logoLight from "@/assets/logo-light.png";
import logoDark from "@/assets/logo-dark.png";

const route = useRoute();
const { isDarkTheme } = useTheme();

const password = ref("");
const confirmPassword = ref("");
const isLoading = ref(false);
const errorMessage = ref("");
const resetSuccess = ref(false);
const invalidToken = ref(false);

const token = ref("");
const uid = ref("");

onMounted(() => {
    token.value = (route.query.token as string) || "";
    uid.value = (route.query.uid as string) || "";

    if (!token.value || !uid.value) {
        invalidToken.value = true;
    }
});

async function handleSubmit() {
    errorMessage.value = "";

    if (password.value.length < 8) {
        errorMessage.value = "Password must be at least 8 characters";
        return;
    }

    if (password.value !== confirmPassword.value) {
        errorMessage.value = "Passwords do not match";
        return;
    }

    isLoading.value = true;

    try {
        await api.post("/auth/password-reset/confirm/", {
            token: token.value,
            uid: uid.value,
            new_password: password.value,
        });
        resetSuccess.value = true;
    } catch (err) {
        const apiErr = err as ApiResponse<unknown>;
        if (
            apiErr?.message?.includes("Invalid") ||
            apiErr?.message?.includes("expired")
        ) {
            invalidToken.value = true;
        } else {
            errorMessage.value =
                apiErr?.message ||
                "Failed to reset password. Please try again.";
        }
    } finally {
        isLoading.value = false;
    }
}
</script>
