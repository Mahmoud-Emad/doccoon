<template>
    <div class="relative" ref="dropdownRef">
        <button
            class="flex items-center gap-2 px-2 py-1 rounded-md cursor-pointer bg-transparent border border-[var(--border-color)] text-[var(--text-color)] transition-colors duration-200 hover:bg-[var(--page-bg)] text-sm"
            :aria-expanded="isOpen"
            aria-haspopup="menu"
            aria-label="User menu"
            @click="isOpen = !isOpen"
        >
            <span
                class="flex items-center justify-center w-6 h-6 rounded-full bg-primary text-white text-xs font-semibold shrink-0"
            >
                {{ initials }}
            </span>
            <span class="max-w-[120px] truncate max-md:hidden">{{
                userName
            }}</span>
            <BaseIcon name="chevron-down" :size="14" />
        </button>

        <Transition
            enter-active-class="transition ease-out duration-150"
            enter-from-class="opacity-0 scale-95"
            enter-to-class="opacity-100 scale-100"
            leave-active-class="transition ease-in duration-100"
            leave-from-class="opacity-100 scale-100"
            leave-to-class="opacity-0 scale-95"
        >
            <div
                v-if="isOpen"
                role="menu"
                class="absolute right-0 top-full mt-1 w-52 bg-[var(--page-bg)] border border-[var(--border-color)] rounded-lg shadow-[0_4px_12px_rgba(0,0,0,0.15)] z-[1000] p-1"
            >
                <div
                    class="px-3 py-2 border-b border-[var(--border-color)] mb-1"
                >
                    <div
                        class="text-sm font-medium text-[var(--text-color)] truncate"
                    >
                        {{ userName }}
                    </div>
                    <div
                        class="text-xs text-[var(--text-color)] opacity-60 truncate"
                    >
                        {{ userEmail }}
                    </div>
                </div>

                <router-link
                    to="/profile"
                    class="w-full flex items-center gap-2.5 px-3 py-2 text-sm text-[var(--text-color)] no-underline bg-transparent border-none rounded cursor-pointer transition-colors duration-150 hover:bg-[var(--border-color)]"
                    @click="isOpen = false"
                >
                    <BaseIcon name="user" :size="16" />
                    Profile
                </router-link>

                <button
                    class="w-full flex items-center gap-2.5 px-3 py-2 text-sm text-[var(--text-color)] bg-transparent border-none rounded cursor-pointer transition-colors duration-150 hover:bg-[var(--border-color)] text-left"
                    @click="openSettings"
                >
                    <BaseIcon name="settings" :size="16" />
                    Settings
                </button>

                <div class="h-px bg-[var(--border-color)] my-1" />

                <button
                    class="w-full flex items-center gap-2.5 px-3 py-2 text-sm text-red-500 bg-transparent border-none rounded cursor-pointer transition-colors duration-150 hover:bg-[var(--border-color)] text-left"
                    @click="handleLogout"
                >
                    <BaseIcon name="log-out" :size="16" />
                    Log out
                </button>
            </div>
        </Transition>

        <SettingsDialog v-model:visible="showSettings" />
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import SettingsDialog from "@/components/settings/SettingsDialog.vue";
import { logout } from "@/api/auth";
import { getProfile } from "@/api/profile";
import { useClickOutside } from "@/composables/useClickOutside";

interface UserProfile {
    id: number;
    email: string;
    full_name: string;
    first_name: string;
    last_name: string;
}

const isOpen = ref(false);
const showSettings = ref(false);
const dropdownRef = ref<HTMLElement | null>(null);
const user = ref<UserProfile | null>(null);

const userName = computed(() => user.value?.full_name || "User");
const userEmail = computed(() => user.value?.email || "");
const initials = computed(() => {
    const u = user.value;
    if (!u) return "?";
    const first = u.first_name?.[0] || "";
    const last = u.last_name?.[0] || "";
    return (first + last).toUpperCase() || u.email?.[0]?.toUpperCase() || "?";
});

function openSettings() {
    isOpen.value = false;
    showSettings.value = true;
}

function handleLogout() {
    isOpen.value = false;
    logout();
}

useClickOutside(dropdownRef, () => {
    isOpen.value = false;
});

function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Escape" && isOpen.value) {
        isOpen.value = false;
    }
}

async function fetchUserProfile() {
    try {
        const profile = await getProfile();
        user.value = profile;
    } catch {
        // Profile fetch failed, use defaults
    }
}

onMounted(() => {
    document.addEventListener("keydown", handleKeydown);
    fetchUserProfile();
});
onUnmounted(() => document.removeEventListener("keydown", handleKeydown));
</script>
