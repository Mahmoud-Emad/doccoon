<template>
    <div class="space-y-6">
        <!-- Theme -->
        <div class="flex items-center justify-between">
            <div>
                <BaseTooltip
                    text="Choose between light and dark appearance"
                    position="right"
                >
                    <span class="text-sm font-medium text-[var(--text-color)]"
                        >Theme</span
                    >
                </BaseTooltip>
                <p class="text-xs text-[var(--text-color)] opacity-60 mt-0.5">
                    {{ settings.theme === "dark" ? "Dark mode" : "Light mode" }}
                </p>
            </div>
            <button
                class="flex items-center justify-center w-9 h-9 bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md cursor-pointer text-[var(--text-color)] transition-colors duration-200 hover:bg-[var(--page-bg)]"
                @click="toggleTheme"
            >
                <BaseIcon
                    :name="settings.theme === 'dark' ? 'moon' : 'sun'"
                    :size="18"
                />
            </button>
        </div>

        <div class="h-px bg-[var(--border-color)]" />

        <!-- Auto Save -->
        <div class="flex items-center justify-between">
            <div>
                <BaseTooltip
                    text="Automatically save your work at regular intervals"
                    position="right"
                >
                    <span class="text-sm font-medium text-[var(--text-color)]"
                        >Auto Save</span
                    >
                </BaseTooltip>
                <p class="text-xs text-[var(--text-color)] opacity-60 mt-0.5">
                    Save your work automatically
                </p>
            </div>
            <button
                class="flex items-center justify-center w-9 h-9 bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md cursor-pointer transition-colors duration-200 hover:bg-[var(--page-bg)]"
                :class="
                    settings.auto_save_enabled
                        ? 'text-primary'
                        : 'text-[var(--text-color)] opacity-50'
                "
                @click="toggleAutoSave"
            >
                <BaseIcon
                    :name="
                        settings.auto_save_enabled
                            ? 'toggle-right'
                            : 'toggle-left'
                    "
                    :size="22"
                />
            </button>
        </div>

        <!-- Auto Save Interval -->
        <div v-if="settings.auto_save_enabled">
            <BaseTooltip
                text="Time in seconds between automatic saves"
                position="right"
            >
                <label
                    class="block text-sm font-medium text-[var(--text-color)] mb-2"
                >
                    Auto Save Interval: {{ settings.auto_save_interval }}s
                </label>
            </BaseTooltip>
            <input
                type="range"
                :value="settings.auto_save_interval"
                min="2"
                max="120"
                step="1"
                class="w-full accent-primary"
                @input="
                    updateInterval(($event.target as HTMLInputElement).value)
                "
            />
            <div
                class="flex justify-between text-[10px] text-[var(--text-color)] opacity-40 mt-1"
            >
                <span>2s</span>
                <span>120s</span>
            </div>
        </div>

        <div class="h-px bg-[var(--border-color)]" />

        <!-- Notifications -->
        <div class="flex items-center justify-between">
            <div>
                <BaseTooltip
                    text="Enable or disable in-app notifications"
                    position="right"
                >
                    <span class="text-sm font-medium text-[var(--text-color)]"
                        >Notifications</span
                    >
                </BaseTooltip>
                <p class="text-xs text-[var(--text-color)] opacity-60 mt-0.5">
                    Receive in-app notifications
                </p>
            </div>
            <button
                class="flex items-center justify-center w-9 h-9 bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md cursor-pointer transition-colors duration-200 hover:bg-[var(--page-bg)]"
                :class="
                    settings.notification_enabled
                        ? 'text-primary'
                        : 'text-[var(--text-color)] opacity-50'
                "
                @click="toggleNotifications"
            >
                <BaseIcon
                    :name="
                        settings.notification_enabled
                            ? 'toggle-right'
                            : 'toggle-left'
                    "
                    :size="22"
                />
            </button>
        </div>

        <span
            v-if="message"
            class="block text-sm mt-2"
            :class="error ? 'text-red-500' : 'text-green-600'"
        >
            {{ message }}
        </span>
    </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import BaseTooltip from "@/components/ui/BaseTooltip.vue";
import { getSettings, updateSettings } from "@/api/settings";
import { useTheme } from "@/composables/useTheme";

const { isDarkTheme, toggleTheme: toggleAppTheme } = useTheme();

const settings = reactive({
    auto_save_enabled: true,
    auto_save_interval: 2,
    notification_enabled: true,
    theme: isDarkTheme.value ? ("dark" as const) : ("light" as const),
    profile_visible: true,
});

const message = ref("");
const error = ref(false);

onMounted(async () => {
    try {
        const s = await getSettings();
        Object.assign(settings, s);
    } catch {
        // settings load failed
    }
});

async function save() {
    message.value = "";
    error.value = false;
    try {
        await updateSettings({ ...settings });
    } catch {
        error.value = true;
        message.value = "Failed to save preferences";
    }
}

function toggleTheme() {
    settings.theme = settings.theme === "dark" ? "light" : "dark";
    toggleAppTheme();
    save();
}

function toggleAutoSave() {
    settings.auto_save_enabled = !settings.auto_save_enabled;
    save();
}

function updateInterval(val: string) {
    settings.auto_save_interval = parseInt(val, 10);
    save();
}

function toggleNotifications() {
    settings.notification_enabled = !settings.notification_enabled;
    save();
}
</script>
