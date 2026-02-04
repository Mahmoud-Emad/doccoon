<template>
    <div class="space-y-5">
        <div>
            <BaseTooltip
                text="Your first name as displayed across the app"
                position="right"
            >
                <label
                    class="block text-sm font-medium text-[var(--text-color)] mb-1.5"
                    >First Name</label
                >
            </BaseTooltip>
            <input
                v-model="firstName"
                type="text"
                class="w-full px-3 py-2 text-sm bg-[var(--bg-color)] text-[var(--text-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors duration-200 focus:border-primary"
                placeholder="First name"
            />
        </div>

        <div>
            <BaseTooltip
                text="Your last name as displayed across the app"
                position="right"
            >
                <label
                    class="block text-sm font-medium text-[var(--text-color)] mb-1.5"
                    >Last Name</label
                >
            </BaseTooltip>
            <input
                v-model="lastName"
                type="text"
                class="w-full px-3 py-2 text-sm bg-[var(--bg-color)] text-[var(--text-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors duration-200 focus:border-primary"
                placeholder="Last name"
            />
        </div>

        <div>
            <BaseTooltip
                text="Your email address (cannot be changed)"
                position="right"
            >
                <label
                    class="block text-sm font-medium text-[var(--text-color)] mb-1.5"
                    >Email</label
                >
            </BaseTooltip>
            <input
                :value="email"
                type="email"
                disabled
                class="w-full px-3 py-2 text-sm bg-[var(--bg-color)] text-[var(--text-color)] border border-[var(--border-color)] rounded-md opacity-60 cursor-not-allowed"
            />
        </div>

        <div class="flex items-center gap-3 pt-2">
            <button
                class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-md cursor-pointer border-none transition-opacity duration-200 hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="saving"
                @click="handleSave"
            >
                {{ saving ? "Saving..." : "Save Changes" }}
            </button>
            <span
                v-if="message"
                class="text-sm"
                :class="error ? 'text-red-500' : 'text-green-600'"
            >
                {{ message }}
            </span>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import BaseTooltip from "@/components/ui/BaseTooltip.vue";
import { getProfile, updateProfile } from "@/api/profile";

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const saving = ref(false);
const message = ref("");
const error = ref(false);

onMounted(async () => {
    try {
        const profile = await getProfile();
        firstName.value = profile.first_name;
        lastName.value = profile.last_name;
        email.value = profile.email;
    } catch {
        // profile load failed
    }
});

async function handleSave() {
    saving.value = true;
    message.value = "";
    error.value = false;
    try {
        await updateProfile({
            first_name: firstName.value,
            last_name: lastName.value,
        });
        // Profile data is fetched from API when needed, no localStorage caching
        message.value = "Profile updated successfully";
    } catch {
        error.value = true;
        message.value = "Failed to update profile";
    } finally {
        saving.value = false;
    }
}
</script>
