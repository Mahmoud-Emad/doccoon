<template>
    <BaseModal
        :visible="visible"
        title=""
        size="sm"
        :close-on-overlay="true"
        @close="emit('close')"
    >
        <div class="flex flex-col relative">
            <!-- Close button -->
            <button
                class="absolute -top-2 -right-2 w-8 h-8 flex items-center justify-center rounded-md text-[var(--text-color)] opacity-50 bg-transparent border-none cursor-pointer transition-all duration-150 hover:opacity-100 hover:bg-[var(--section-alt-bg)]"
                @click="emit('close')"
            >
                <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                >
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
            </button>

            <!-- Header -->
            <div class="text-center mb-6">
                <h2
                    class="text-lg font-semibold text-[var(--text-color)] m-0 mb-2"
                >
                    You're in Guest Mode
                </h2>
                <p class="text-sm text-[var(--text-color)] opacity-50 m-0">
                    Some features are limited without an account
                </p>
            </div>

            <!-- Limitations -->
            <div
                class="border border-[var(--border-color)] rounded-lg overflow-hidden mb-6"
            >
                <div
                    class="px-4 py-3 border-b border-[var(--border-color)] last:border-b-0"
                >
                    <p class="text-sm text-[var(--text-color)] m-0">
                        <span class="font-medium">No cloud save</span>
                        <span class="opacity-50">
                            — changes are lost on refresh
                        </span>
                    </p>
                </div>
                <div
                    class="px-4 py-3 border-b border-[var(--border-color)] last:border-b-0"
                >
                    <p class="text-sm text-[var(--text-color)] m-0">
                        <span class="font-medium">No AI tools</span>
                        <span class="opacity-50">
                            — rewrite and refine disabled
                        </span>
                    </p>
                </div>
                <div
                    class="px-4 py-3 border-b border-[var(--border-color)] last:border-b-0"
                >
                    <p class="text-sm text-[var(--text-color)] m-0">
                        <span class="font-medium">No sharing</span>
                        <span class="opacity-50">
                            — publish and share disabled
                        </span>
                    </p>
                </div>
                <div class="px-4 py-3">
                    <p class="text-sm text-[var(--text-color)] m-0">
                        <span class="font-medium">Limited to 2 pages</span>
                        <span class="opacity-50">
                            — per book in guest mode
                        </span>
                    </p>
                </div>
            </div>

            <!-- Actions -->
            <div class="flex flex-col gap-2">
                <router-link
                    to="/register"
                    class="w-full py-2.5 text-sm font-medium text-white bg-primary rounded-lg text-center no-underline transition-opacity duration-200 hover:opacity-90"
                >
                    Create Free Account
                </router-link>
                <router-link
                    to="/login"
                    class="w-full py-2.5 text-sm font-medium text-[var(--text-color)] bg-[var(--section-alt-bg)] border border-[var(--border-color)] rounded-lg text-center no-underline transition-colors duration-200 hover:bg-[var(--border-color)]"
                >
                    Log In
                </router-link>
                <button
                    class="w-full py-2.5 text-sm text-[var(--text-color)] opacity-50 bg-transparent border-none cursor-pointer transition-opacity duration-200 hover:opacity-80"
                    @click="emit('continue')"
                >
                    Continue as Guest
                </button>
            </div>
        </div>
    </BaseModal>
</template>

<script setup lang="ts">
import BaseModal from "@/components/ui/BaseModal.vue";

defineProps<{
    visible: boolean;
}>();

const emit = defineEmits<{
    close: [];
    continue: [];
}>();
</script>
