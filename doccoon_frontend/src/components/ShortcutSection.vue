<template>
    <div class="flex flex-col">
        <!-- Section Header -->
        <div class="flex items-center gap-2 mb-3">
            <div
                class="w-7 h-7 rounded-lg bg-[var(--section-alt-bg)] flex items-center justify-center"
            >
                <BaseIcon
                    :name="icon"
                    :size="14"
                    class="text-[var(--text-color)] opacity-60"
                />
            </div>
            <h3
                class="text-sm font-semibold text-[var(--text-color)] m-0 uppercase tracking-wide opacity-70"
            >
                {{ title }}
            </h3>
        </div>

        <!-- Shortcuts List -->
        <div
            class="bg-[var(--section-alt-bg)] rounded-xl border border-[var(--border-color)] overflow-hidden"
        >
            <div
                v-for="(shortcut, index) in shortcuts"
                :key="shortcut.description"
                class="flex items-center justify-between px-4 py-3 transition-colors duration-150 hover:bg-[var(--bg-color)]"
                :class="{
                    'border-t border-[var(--border-color)]': index > 0,
                }"
            >
                <span class="text-sm text-[var(--text-color)]">
                    {{ shortcut.description }}
                </span>
                <div class="flex items-center gap-1">
                    <template v-if="shortcut.ctrl">
                        <kbd class="shortcut-key">{{ isMac ? '⌘' : 'Ctrl' }}</kbd>
                        <span class="text-[var(--text-color)] opacity-30 text-xs">+</span>
                    </template>
                    <template v-if="shortcut.alt">
                        <kbd class="shortcut-key">{{ isMac ? '⌥' : 'Alt' }}</kbd>
                        <span class="text-[var(--text-color)] opacity-30 text-xs">+</span>
                    </template>
                    <template v-if="shortcut.shift">
                        <kbd class="shortcut-key">{{ isMac ? '⇧' : 'Shift' }}</kbd>
                        <span class="text-[var(--text-color)] opacity-30 text-xs">+</span>
                    </template>
                    <kbd class="shortcut-key">{{ formatKey(shortcut.key) }}</kbd>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import type { KeyboardShortcut } from "@/composables/useKeyboardShortcuts";

defineProps<{
    title: string;
    icon: string;
    shortcuts: KeyboardShortcut[];
}>();

const isMac = computed(() =>
    typeof navigator !== "undefined" &&
    navigator.platform.toUpperCase().indexOf("MAC") >= 0
);

function formatKey(key: string): string {
    const keyMap: Record<string, string> = {
        "ArrowLeft": "←",
        "ArrowRight": "→",
        "ArrowUp": "↑",
        "ArrowDown": "↓",
        "Escape": "Esc",
        "Enter": "↵",
        " ": "Space",
        "`": "`",
        "'": "'",
    };
    return keyMap[key] || key.toUpperCase();
}
</script>

<style scoped>
.shortcut-key {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 1.75rem;
    height: 1.75rem;
    padding: 0 0.5rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.75rem;
    font-weight: 500;
    background: var(--bg-color);
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    color: var(--text-color);
    box-shadow:
        0 1px 0 1px rgba(0, 0, 0, 0.04),
        0 2px 4px rgba(0, 0, 0, 0.08);
}

/* Keyboard key press effect on hover */
.shortcut-key:hover {
    transform: translateY(1px);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
}
</style>
