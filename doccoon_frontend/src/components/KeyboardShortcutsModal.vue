<template>
    <BaseModal :visible="visible" title="" size="lg" @close="emit('close')">
        <div class="flex flex-col">
            <!-- Header -->
            <div class="flex items-center gap-3 mb-6">
                <div
                    class="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center"
                >
                    <BaseIcon name="command" :size="24" class="text-primary" />
                </div>
                <div>
                    <h2
                        class="text-xl font-semibold text-[var(--text-color)] m-0"
                    >
                        Keyboard Shortcuts
                    </h2>
                    <p
                        class="text-sm text-[var(--text-color)] opacity-60 m-0 mt-0.5"
                    >
                        Speed up your workflow with these shortcuts
                    </p>
                </div>
            </div>

            <!-- Search (optional future feature placeholder) -->
            <div class="relative mb-5">
                <BaseIcon
                    name="search"
                    :size="16"
                    class="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--text-color)] opacity-40"
                />
                <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="Search shortcuts..."
                    class="w-full pl-10 pr-4 py-2.5 text-sm bg-[var(--section-alt-bg)] text-[var(--text-color)] border border-[var(--border-color)] rounded-lg outline-none transition-all duration-200 focus:border-primary focus:ring-2 focus:ring-primary/20"
                />
            </div>

            <!-- Shortcuts Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- General Shortcuts -->
                <ShortcutSection
                    v-if="filteredGeneralShortcuts.length > 0"
                    title="General"
                    icon="settings"
                    :shortcuts="filteredGeneralShortcuts"
                />

                <!-- Navigation Shortcuts -->
                <ShortcutSection
                    v-if="filteredNavigationShortcuts.length > 0"
                    title="Navigation"
                    icon="navigation"
                    :shortcuts="filteredNavigationShortcuts"
                />

                <!-- View Shortcuts -->
                <ShortcutSection
                    v-if="filteredViewShortcuts.length > 0"
                    title="View"
                    icon="eye"
                    :shortcuts="filteredViewShortcuts"
                />

                <!-- Editing Shortcuts -->
                <ShortcutSection
                    v-if="filteredEditingShortcuts.length > 0"
                    title="Text Formatting"
                    icon="type"
                    :shortcuts="filteredEditingShortcuts"
                />
            </div>

            <!-- Empty State -->
            <div
                v-if="noResults"
                class="flex flex-col items-center justify-center py-12"
            >
                <BaseIcon
                    name="search"
                    :size="40"
                    class="text-[var(--text-color)] opacity-20 mb-3"
                />
                <p class="text-sm text-[var(--text-color)] opacity-60 m-0">
                    No shortcuts found for "{{ searchQuery }}"
                </p>
            </div>

            <!-- Platform Tip -->
            <div
                class="flex items-center gap-3 mt-6 p-4 bg-gradient-to-r from-primary/5 to-primary/10 border border-primary/20 rounded-xl"
            >
                <div
                    class="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center shrink-0"
                >
                    <BaseIcon name="info" :size="20" class="text-primary" />
                </div>
                <div class="flex-1">
                    <p class="text-sm font-medium text-[var(--text-color)] m-0">
                        Platform Shortcuts
                    </p>
                    <p
                        class="text-xs text-[var(--text-color)] opacity-70 m-0 mt-0.5"
                    >
                        On macOS, use
                        <kbd class="shortcut-key">⌘</kbd>
                        instead of
                        <kbd class="shortcut-key">Ctrl</kbd>
                        for all shortcuts
                    </p>
                </div>
            </div>
        </div>

        <template #footer>
            <div class="flex items-center justify-between w-full">
                <p class="text-xs text-[var(--text-color)] opacity-50 m-0">
                    Press <kbd class="shortcut-key">Ctrl</kbd> +
                    <kbd class="shortcut-key">?</kbd> anytime to open this
                </p>
                <button
                    class="px-5 py-2 text-sm font-medium text-white bg-primary rounded-lg cursor-pointer border-none transition-all duration-200 hover:opacity-90 hover:shadow-[0_4px_12px_rgba(0,122,204,0.3)]"
                    @click="emit('close')"
                >
                    Got it
                </button>
            </div>
        </template>
    </BaseModal>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import BaseModal from "@/components/ui/BaseModal.vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import ShortcutSection from "@/components/ShortcutSection.vue";
import type { KeyboardShortcut } from "@/composables/useKeyboardShortcuts";

const props = defineProps<{
    visible: boolean;
    shortcuts: KeyboardShortcut[];
}>();

const emit = defineEmits<{
    close: [];
}>();

const searchQuery = ref("");

function filterBySearch(shortcuts: KeyboardShortcut[]) {
    if (!searchQuery.value.trim()) return shortcuts;
    const query = searchQuery.value.toLowerCase();
    return shortcuts.filter(
        (s) =>
            s.description.toLowerCase().includes(query) ||
            s.key.toLowerCase().includes(query),
    );
}

const filteredGeneralShortcuts = computed(() =>
    filterBySearch(props.shortcuts.filter((s) => s.category === "general")),
);

const filteredEditingShortcuts = computed(() =>
    filterBySearch(props.shortcuts.filter((s) => s.category === "editing")),
);

const filteredNavigationShortcuts = computed(() =>
    filterBySearch(props.shortcuts.filter((s) => s.category === "navigation")),
);

const filteredViewShortcuts = computed(() =>
    filterBySearch(props.shortcuts.filter((s) => s.category === "view")),
);

const noResults = computed(
    () =>
        searchQuery.value.trim() &&
        filteredGeneralShortcuts.value.length === 0 &&
        filteredEditingShortcuts.value.length === 0 &&
        filteredNavigationShortcuts.value.length === 0 &&
        filteredViewShortcuts.value.length === 0,
);
</script>

<style scoped>
.shortcut-key {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 1.5rem;
    padding: 0.125rem 0.375rem;
    font-family:
        ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.6875rem;
    font-weight: 500;
    background: var(--section-alt-bg);
    border: 1px solid var(--border-color);
    border-radius: 0.25rem;
    color: var(--text-color);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
</style>
