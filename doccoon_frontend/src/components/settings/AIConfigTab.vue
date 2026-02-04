<template>
    <div class="space-y-8">
        <!-- Header -->
        <div>
            <h3
                class="text-sm font-semibold tracking-widest uppercase text-primary mb-2"
            >
                AI Configuration
            </h3>
            <p class="text-sm text-[var(--text-color)] opacity-50">
                Add your OpenAI or Gemini API keys to use AI features. Your keys
                are stored securely and never shared.
            </p>
        </div>

        <!-- Saved Keys -->
        <div>
            <div class="flex items-center justify-between mb-4">
                <h4
                    class="text-xs font-medium text-[var(--text-color)] opacity-60 uppercase tracking-wider"
                >
                    Your API Keys
                </h4>
                <button
                    v-if="!showAddForm && keys.length > 0"
                    class="text-xs text-primary bg-transparent border-none cursor-pointer hover:underline p-0"
                    @click="showAddForm = true"
                >
                    + Add Key
                </button>
            </div>

            <!-- Empty State -->
            <div
                v-if="keys.length === 0 && !showAddForm"
                class="border border-dashed border-[var(--border-color)] rounded-lg p-8 text-center"
            >
                <div
                    class="w-10 h-10 mx-auto mb-3 rounded-full bg-[var(--section-alt-bg)] flex items-center justify-center"
                >
                    <BaseIcon
                        name="key"
                        :size="18"
                        class="text-[var(--text-color)] opacity-40"
                    />
                </div>
                <p class="text-sm text-[var(--text-color)] opacity-50 mb-4">
                    No API keys configured yet
                </p>
                <button
                    class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-md border-none cursor-pointer transition-opacity duration-200 hover:opacity-90"
                    @click="showAddForm = true"
                >
                    Add Your First Key
                </button>
            </div>

            <!-- Keys List -->
            <div v-else class="space-y-3">
                <div
                    v-for="key in keys"
                    :key="key.id"
                    class="border rounded-lg overflow-hidden transition-all duration-200"
                    :class="
                        key.is_active
                            ? 'border-emerald-500/40 bg-emerald-500/5'
                            : 'border-[var(--border-color)] bg-[var(--bg-color)]'
                    "
                >
                    <!-- Key Header -->
                    <div class="px-4 py-3 flex items-center gap-3">
                        <!-- Active Indicator -->
                        <button
                            class="w-8 h-8 rounded-full flex items-center justify-center cursor-pointer border-none transition-all duration-200"
                            :class="
                                key.is_active
                                    ? 'bg-emerald-500 text-white'
                                    : 'bg-[var(--section-alt-bg)] text-[var(--text-color)] opacity-40 hover:opacity-70'
                            "
                            :title="
                                key.is_active
                                    ? 'Active key'
                                    : 'Click to activate'
                            "
                            @click="toggleKey(key)"
                        >
                            <BaseIcon
                                :name="key.is_active ? 'check' : 'circle'"
                                :size="14"
                            />
                        </button>

                        <!-- Key Info -->
                        <div class="flex-1 min-w-0">
                            <div class="flex items-center gap-2">
                                <span
                                    class="text-sm font-medium text-[var(--text-color)] truncate"
                                >
                                    {{ key.label || "Unnamed Key" }}
                                </span>
                                <span
                                    class="shrink-0 px-2 py-0.5 text-[10px] font-semibold rounded-full uppercase"
                                    :class="providerBadgeClass(key.provider)"
                                >
                                    {{ key.provider }}
                                </span>
                            </div>
                            <div
                                class="text-xs text-[var(--text-color)] opacity-40 font-mono mt-0.5"
                            >
                                {{ key.masked_key }}
                            </div>
                        </div>

                        <!-- Actions -->
                        <div class="flex items-center gap-1">
                            <button
                                class="w-8 h-8 rounded-md flex items-center justify-center cursor-pointer bg-transparent border-none text-[var(--text-color)] opacity-40 transition-all duration-200 hover:opacity-70 hover:bg-[var(--section-alt-bg)]"
                                title="Edit key"
                                @click="startEditKey(key)"
                            >
                                <BaseIcon name="edit" :size="14" />
                            </button>
                            <button
                                class="w-8 h-8 rounded-md flex items-center justify-center cursor-pointer bg-transparent border-none text-red-500 opacity-50 transition-all duration-200 hover:opacity-100 hover:bg-red-500/10"
                                title="Delete key"
                                @click="handleDeleteKey(key.id)"
                            >
                                <BaseIcon name="trash" :size="14" />
                            </button>
                        </div>
                    </div>

                    <!-- Model Selector -->
                    <div
                        class="px-4 py-2 border-t border-[var(--border-color)]/50 bg-[var(--section-alt-bg)]/30"
                    >
                        <div class="flex items-center gap-3">
                            <span
                                class="text-[10px] font-medium text-[var(--text-color)] opacity-40 uppercase tracking-wider"
                            >
                                Model
                            </span>
                            <select
                                :value="key.model"
                                class="flex-1 px-2 py-1 text-xs bg-[var(--bg-color)] text-[var(--text-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors duration-200 focus:border-primary cursor-pointer"
                                @change="
                                    updateKeyModel(
                                        key,
                                        ($event.target as HTMLSelectElement)
                                            .value,
                                    )
                                "
                            >
                                <option
                                    v-for="m in modelsForProvider(key.provider)"
                                    :key="m.value"
                                    :value="m.value"
                                >
                                    {{ m.label }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Add/Edit Form -->
        <div
            v-if="showAddForm || editingKey"
            class="border border-[var(--border-color)] rounded-lg overflow-hidden"
        >
            <!-- Form Header -->
            <div
                class="px-4 py-3 bg-[var(--section-alt-bg)] border-b border-[var(--border-color)] flex items-center justify-between"
            >
                <h4 class="text-sm font-medium text-[var(--text-color)]">
                    {{ editingKey ? "Edit API Key" : "Add New API Key" }}
                </h4>
                <button
                    class="w-6 h-6 rounded flex items-center justify-center cursor-pointer bg-transparent border-none text-[var(--text-color)] opacity-40 hover:opacity-70"
                    @click="cancelForm"
                >
                    <BaseIcon name="close" :size="14" />
                </button>
            </div>

            <!-- Form Body -->
            <div class="p-4 space-y-4">
                <!-- Provider -->
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label
                            class="block text-[10px] font-medium text-[var(--text-color)] opacity-50 uppercase tracking-wider mb-1.5"
                        >
                            Provider
                        </label>
                        <select
                            v-model="formProvider"
                            class="w-full px-3 py-2 text-sm bg-[var(--bg-color)] text-[var(--text-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors duration-200 focus:border-primary cursor-pointer"
                            :disabled="!!editingKey"
                            @change="onProviderChange"
                        >
                            <option
                                v-for="p in providers"
                                :key="p.value"
                                :value="p.value"
                            >
                                {{ p.label }}
                            </option>
                        </select>
                    </div>
                    <div>
                        <label
                            class="block text-[10px] font-medium text-[var(--text-color)] opacity-50 uppercase tracking-wider mb-1.5"
                        >
                            Model
                        </label>
                        <select
                            v-model="formModel"
                            class="w-full px-3 py-2 text-sm bg-[var(--bg-color)] text-[var(--text-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors duration-200 focus:border-primary cursor-pointer"
                        >
                            <option
                                v-for="m in modelsForProvider(formProvider)"
                                :key="m.value"
                                :value="m.value"
                            >
                                {{ m.label }}
                            </option>
                        </select>
                    </div>
                </div>

                <!-- Label -->
                <div>
                    <label
                        class="block text-[10px] font-medium text-[var(--text-color)] opacity-50 uppercase tracking-wider mb-1.5"
                    >
                        Label
                    </label>
                    <input
                        v-model="formLabel"
                        type="text"
                        class="w-full px-3 py-2 text-sm bg-[var(--bg-color)] text-[var(--text-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors duration-200 focus:border-primary"
                        placeholder="e.g., Personal Key, Work Account"
                    />
                </div>

                <!-- API Key -->
                <div>
                    <label
                        class="block text-[10px] font-medium text-[var(--text-color)] opacity-50 uppercase tracking-wider mb-1.5"
                    >
                        API Key
                        <span v-if="editingKey" class="normal-case opacity-70">
                            (leave empty to keep current)
                        </span>
                    </label>
                    <input
                        v-model="formApiKey"
                        type="password"
                        class="w-full px-3 py-2 text-sm bg-[var(--bg-color)] text-[var(--text-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors duration-200 focus:border-primary font-mono"
                        :placeholder="
                            editingKey
                                ? '••••••••••••'
                                : formProvider === 'gemini'
                                  ? 'AIza...'
                                  : 'sk-...'
                        "
                    />
                </div>

                <!-- Help Text -->
                <p class="text-xs text-[var(--text-color)] opacity-40">
                    <span v-if="formProvider === 'gemini'">
                        Get your API key from
                        <a
                            href="https://aistudio.google.com/app/apikey"
                            target="_blank"
                            rel="noopener"
                            class="text-primary hover:underline"
                        >
                            Google AI Studio
                        </a>
                    </span>
                    <span v-else>
                        Get your API key from
                        <a
                            href="https://platform.openai.com/api-keys"
                            target="_blank"
                            rel="noopener"
                            class="text-primary hover:underline"
                        >
                            OpenAI Platform
                        </a>
                    </span>
                </p>

                <!-- Form Actions -->
                <div class="flex items-center justify-end gap-3 pt-2">
                    <button
                        class="px-4 py-2 text-sm font-medium text-[var(--text-color)] bg-transparent border border-[var(--border-color)] rounded-md cursor-pointer transition-colors duration-200 hover:bg-[var(--section-alt-bg)]"
                        @click="cancelForm"
                    >
                        Cancel
                    </button>
                    <button
                        class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-md border-none cursor-pointer transition-opacity duration-200 hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
                        :disabled="!canSubmitForm || submitting"
                        @click="handleSubmitForm"
                    >
                        {{
                            submitting
                                ? "Saving..."
                                : editingKey
                                  ? "Save Changes"
                                  : "Add Key"
                        }}
                    </button>
                </div>
            </div>
        </div>

        <!-- Info Section -->
        <div
            class="border border-[var(--border-color)] rounded-lg p-4 bg-[var(--section-alt-bg)]/30"
        >
            <h4
                class="text-xs font-medium text-[var(--text-color)] opacity-60 uppercase tracking-wider mb-3"
            >
                How it works
            </h4>
            <ul class="space-y-2 text-xs text-[var(--text-color)] opacity-50">
                <li class="flex items-start gap-2">
                    <span class="text-primary mt-0.5">1.</span>
                    <span>
                        Add your API key from OpenAI or Google (Gemini)
                    </span>
                </li>
                <li class="flex items-start gap-2">
                    <span class="text-primary mt-0.5">2.</span>
                    <span> Select your preferred model for each key </span>
                </li>
                <li class="flex items-start gap-2">
                    <span class="text-primary mt-0.5">3.</span>
                    <span>
                        Activate a key to use it for AI features in the editor
                    </span>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import {
    getAIKeys,
    createAIKey,
    updateAIKey,
    deleteAIKey,
} from "@/api/ai-keys";
import { useToast } from "@/composables/useToast";
import type { AIProviderKey } from "@/types";

const providers = [
    { value: "openai", label: "OpenAI" },
    { value: "gemini", label: "Gemini" },
];

const openaiModels = [
    { value: "gpt-4o-mini", label: "GPT-4o Mini" },
    { value: "gpt-4o", label: "GPT-4o" },
    { value: "gpt-4.1-nano", label: "GPT-4.1 Nano" },
    { value: "gpt-4.1-mini", label: "GPT-4.1 Mini" },
    { value: "gpt-4.1", label: "GPT-4.1" },
];

const geminiModels = [
    { value: "gemini-2.0-flash", label: "Gemini 2.0 Flash" },
    { value: "gemini-2.5-flash", label: "Gemini 2.5 Flash" },
    { value: "gemini-2.5-pro", label: "Gemini 2.5 Pro" },
];

function modelsForProvider(
    provider: string,
): { value: string; label: string }[] {
    return provider === "gemini" ? geminiModels : openaiModels;
}

function defaultModelForProvider(provider: string): string {
    return provider === "gemini" ? "gemini-2.5-flash" : "gpt-4o-mini";
}

const keys = ref<AIProviderKey[]>([]);
const toast = useToast();

// Form state
const showAddForm = ref(false);
const editingKey = ref<AIProviderKey | null>(null);
const formProvider = ref("gemini");
const formModel = ref("gemini-2.5-flash");
const formLabel = ref("");
const formApiKey = ref("");
const submitting = ref(false);

function providerBadgeClass(provider: string): string {
    if (provider === "openai") {
        return "bg-emerald-500/10 text-emerald-600";
    }
    return "bg-blue-500/10 text-blue-600";
}

function onProviderChange() {
    formModel.value = defaultModelForProvider(formProvider.value);
}

const canSubmitForm = computed(() => {
    if (editingKey.value) {
        // When editing, API key is optional (keeps current if empty)
        return formLabel.value.trim().length > 0;
    }
    // When adding, API key is required
    return (
        formLabel.value.trim().length > 0 && formApiKey.value.trim().length > 0
    );
});

function cancelForm() {
    showAddForm.value = false;
    editingKey.value = null;
    formProvider.value = "gemini";
    formModel.value = "gemini-2.5-flash";
    formLabel.value = "";
    formApiKey.value = "";
}

function startEditKey(key: AIProviderKey) {
    editingKey.value = key;
    formProvider.value = key.provider;
    formModel.value = key.model;
    formLabel.value = key.label;
    formApiKey.value = "";
    showAddForm.value = false;
}

async function handleSubmitForm() {
    submitting.value = true;
    try {
        if (editingKey.value) {
            // Update existing key
            const updateData: Record<string, string | boolean> = {
                label: formLabel.value,
                model: formModel.value,
            };
            if (formApiKey.value.trim()) {
                updateData.api_key = formApiKey.value;
            }
            const updated = await updateAIKey(
                editingKey.value.id,
                updateData as never,
            );
            const index = keys.value.findIndex(
                (k) => k.id === editingKey.value!.id,
            );
            if (index !== -1) {
                keys.value[index] = updated;
            }
            toast.success("API key updated successfully.");
        } else {
            // Create new key
            const key = await createAIKey({
                provider: formProvider.value,
                label: formLabel.value,
                api_key: formApiKey.value,
                model: formModel.value,
            });
            keys.value.unshift(key);
            toast.success("API key added successfully.");
        }
        cancelForm();
    } catch {
        toast.error(
            editingKey.value
                ? "Failed to update API key."
                : "Failed to add API key.",
        );
    } finally {
        submitting.value = false;
    }
}

async function updateKeyModel(key: AIProviderKey, model: string) {
    try {
        await updateAIKey(key.id, { model } as never);
        key.model = model;
        toast.success("Model updated.");
    } catch {
        toast.error("Failed to update model.");
    }
}

async function toggleKey(key: AIProviderKey) {
    if (key.is_active) {
        try {
            await updateAIKey(key.id, { is_active: false } as never);
            key.is_active = false;
        } catch {
            toast.error("Failed to update API key.");
        }
    } else {
        try {
            for (const k of keys.value) {
                if (k.is_active) {
                    await updateAIKey(k.id, { is_active: false } as never);
                    k.is_active = false;
                }
            }
            await updateAIKey(key.id, { is_active: true } as never);
            key.is_active = true;
        } catch {
            toast.error("Failed to activate API key.");
        }
    }
}

async function handleDeleteKey(id: number) {
    try {
        await deleteAIKey(id);
        keys.value = keys.value.filter((k) => k.id !== id);
        toast.success("API key deleted.");
    } catch {
        toast.error("Failed to delete API key.");
    }
}

onMounted(async () => {
    try {
        keys.value = await getAIKeys();
    } catch {
        toast.error("Failed to load AI keys.");
    }
});
</script>
