<template>
    <div class="space-y-6">
        <!-- Change Password -->
        <div>
            <h3 class="text-sm font-semibold text-[var(--text-color)] mb-1">
                {{ hasPassword ? "Change Password" : "Set Password" }}
            </h3>
            <p
                v-if="!hasPassword"
                class="text-xs text-[var(--text-color)] opacity-60 mb-3"
            >
                You signed up with a social account. Set a password to also sign
                in with email.
            </p>

            <div class="space-y-3">
                <div v-if="hasPassword">
                    <BaseTooltip
                        text="Enter your current password for verification"
                        position="right"
                    >
                        <label
                            class="block text-xs font-medium text-[var(--text-color)] mb-1"
                            >Current Password</label
                        >
                    </BaseTooltip>
                    <input
                        v-model="currentPassword"
                        type="password"
                        class="w-full px-3 py-2 text-sm bg-[var(--bg-color)] text-[var(--text-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors duration-200 focus:border-primary"
                        placeholder="Current password"
                    />
                </div>

                <div>
                    <BaseTooltip
                        text="Choose a strong password with at least 8 characters"
                        position="right"
                    >
                        <label
                            class="block text-xs font-medium text-[var(--text-color)] mb-1"
                            >{{
                                hasPassword ? "New Password" : "Password"
                            }}</label
                        >
                    </BaseTooltip>
                    <input
                        v-model="newPassword"
                        type="password"
                        class="w-full px-3 py-2 text-sm bg-[var(--bg-color)] text-[var(--text-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors duration-200 focus:border-primary"
                        :placeholder="
                            hasPassword ? 'New password' : 'Enter password'
                        "
                    />
                </div>

                <div>
                    <BaseTooltip
                        text="Re-enter your new password to confirm"
                        position="right"
                    >
                        <label
                            class="block text-xs font-medium text-[var(--text-color)] mb-1"
                            >Confirm Password</label
                        >
                    </BaseTooltip>
                    <input
                        v-model="confirmPassword"
                        type="password"
                        class="w-full px-3 py-2 text-sm bg-[var(--bg-color)] text-[var(--text-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors duration-200 focus:border-primary"
                        placeholder="Confirm password"
                    />
                </div>

                <div class="flex items-center gap-3">
                    <button
                        class="px-4 py-2 text-sm font-medium text-primary bg-transparent border border-[var(--border-color)] rounded-md cursor-pointer transition-colors duration-200 hover:border-primary hover:bg-primary/5 disabled:opacity-50 disabled:cursor-not-allowed"
                        :disabled="savingPassword"
                        @click="handleChangePassword"
                    >
                        {{
                            savingPassword
                                ? "Saving..."
                                : hasPassword
                                  ? "Update"
                                  : "Set Password"
                        }}
                    </button>
                    <span
                        v-if="passwordMessage"
                        class="text-sm"
                        :class="
                            passwordError ? 'text-red-500' : 'text-green-600'
                        "
                    >
                        {{ passwordMessage }}
                    </span>
                </div>
            </div>
        </div>

        <div class="h-px bg-[var(--border-color)]" />

        <!-- Profile Visibility -->
        <div class="flex items-center justify-between">
            <div>
                <BaseTooltip
                    text="Control whether other users can see your profile"
                    position="right"
                >
                    <span class="text-sm font-medium text-[var(--text-color)]"
                        >Profile Visibility</span
                    >
                </BaseTooltip>
                <p class="text-xs text-[var(--text-color)] opacity-60 mt-0.5">
                    {{
                        profileVisible
                            ? "Your profile is public"
                            : "Your profile is private"
                    }}
                </p>
            </div>
            <button
                class="flex items-center justify-center w-9 h-9 bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md cursor-pointer transition-colors duration-200 hover:bg-[var(--page-bg)]"
                :class="
                    profileVisible
                        ? 'text-primary'
                        : 'text-[var(--text-color)] opacity-50'
                "
                @click="toggleVisibility"
            >
                <BaseIcon
                    :name="profileVisible ? 'eye' : 'eye-off'"
                    :size="18"
                />
            </button>
        </div>

        <div class="h-px bg-[var(--border-color)]" />

        <!-- Delete Account -->
        <div class="flex items-center justify-between">
            <div>
                <span class="text-sm font-medium text-[var(--text-color)]"
                    >Delete Account</span
                >
                <p class="text-xs text-[var(--text-color)] opacity-60 mt-0.5">
                    Permanently delete your account and all data
                </p>
            </div>
            <button
                class="px-4 py-2 text-sm font-medium text-danger bg-transparent border border-[var(--border-color)] rounded-md cursor-pointer transition-colors duration-200 hover:border-danger hover:bg-danger/5"
                @click="showDeleteConfirmation = true"
            >
                Delete
            </button>
        </div>

        <!-- Delete Confirmation Modal -->
        <BaseModal
            :visible="showDeleteConfirmation"
            title=""
            size="sm"
            :close-on-overlay="true"
            @close="showDeleteConfirmation = false"
        >
            <div class="flex flex-col">
                <!-- Header -->
                <div class="text-center mb-6">
                    <h2
                        class="text-lg font-semibold text-[var(--text-color)] m-0 mb-2"
                    >
                        Delete your account?
                    </h2>
                    <p class="text-sm text-[var(--text-color)] opacity-50 m-0">
                        This action is permanent and cannot be undone
                    </p>
                </div>

                <!-- What will be deleted -->
                <div
                    class="border border-[var(--border-color)] rounded-lg overflow-hidden mb-6"
                >
                    <div
                        class="px-4 py-3 border-b border-[var(--border-color)]"
                    >
                        <p class="text-sm text-[var(--text-color)] m-0">
                            <span class="font-medium">All your books</span>
                            <span class="opacity-50">
                                — will be permanently deleted
                            </span>
                        </p>
                    </div>
                    <div
                        class="px-4 py-3 border-b border-[var(--border-color)]"
                    >
                        <p class="text-sm text-[var(--text-color)] m-0">
                            <span class="font-medium">All your pages</span>
                            <span class="opacity-50">
                                — content cannot be recovered
                            </span>
                        </p>
                    </div>
                    <div class="px-4 py-3">
                        <p class="text-sm text-[var(--text-color)] m-0">
                            <span class="font-medium">Your settings</span>
                            <span class="opacity-50">
                                — preferences and API keys
                            </span>
                        </p>
                    </div>
                </div>

                <!-- Actions -->
                <div class="flex flex-col gap-2">
                    <button
                        class="w-full py-2.5 text-sm font-medium text-white bg-danger rounded-lg cursor-pointer border-none transition-opacity duration-200 hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
                        :disabled="deletingAccount"
                        @click="handleDeleteAccount"
                    >
                        {{
                            deletingAccount
                                ? "Deleting..."
                                : "Delete My Account"
                        }}
                    </button>
                    <button
                        class="w-full py-2.5 text-sm text-[var(--text-color)] opacity-50 bg-transparent border-none cursor-pointer transition-opacity duration-200 hover:opacity-80"
                        @click="showDeleteConfirmation = false"
                    >
                        Cancel
                    </button>
                </div>
            </div>
        </BaseModal>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import BaseTooltip from "@/components/ui/BaseTooltip.vue";
import BaseModal from "@/components/ui/BaseModal.vue";
import { api, type ApiResponse } from "@/api/client";
import { getSettings, updateSettings, getUserProfile } from "@/api/settings";
import { deleteAccount } from "@/api/auth";

const router = useRouter();

const hasPassword = ref(true);
const currentPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const savingPassword = ref(false);
const passwordMessage = ref("");
const passwordError = ref(false);

const profileVisible = ref(true);

const showDeleteConfirmation = ref(false);
const deletingAccount = ref(false);

onMounted(async () => {
    try {
        const [settings, profile] = await Promise.all([
            getSettings(),
            getUserProfile(),
        ]);
        profileVisible.value = settings.profile_visible;
        hasPassword.value = profile.has_password;
    } catch {
        // load failed
    }
});

async function handleChangePassword() {
    passwordMessage.value = "";
    passwordError.value = false;

    if (newPassword.value.length < 8) {
        passwordError.value = true;
        passwordMessage.value = "Password must be at least 8 characters";
        return;
    }

    if (newPassword.value !== confirmPassword.value) {
        passwordError.value = true;
        passwordMessage.value = "Passwords do not match";
        return;
    }

    savingPassword.value = true;
    try {
        await api.put("/auth/change-password/", {
            old_password: currentPassword.value,
            new_password: newPassword.value,
        });
        passwordMessage.value = hasPassword.value
            ? "Password updated successfully"
            : "Password set successfully";
        hasPassword.value = true; // User now has a password
        currentPassword.value = "";
        newPassword.value = "";
        confirmPassword.value = "";
    } catch (err) {
        passwordError.value = true;
        const apiErr = err as ApiResponse<unknown>;
        passwordMessage.value = apiErr?.message || "Failed to update password.";
    } finally {
        savingPassword.value = false;
    }
}

async function toggleVisibility() {
    profileVisible.value = !profileVisible.value;
    try {
        await updateSettings({ profile_visible: profileVisible.value });
    } catch {
        profileVisible.value = !profileVisible.value;
    }
}

async function handleDeleteAccount() {
    deletingAccount.value = true;
    try {
        await deleteAccount();
        router.push("/login");
    } catch {
        // Error handled silently, user stays on page
    } finally {
        deletingAccount.value = false;
        showDeleteConfirmation.value = false;
    }
}
</script>
