<template>
    <div class="py-24 px-8 max-md:py-16 max-md:px-5 bg-[var(--section-alt-bg)]">
        <div class="max-w-[640px] mx-auto text-center">
            <h2
                class="text-[28px] max-md:text-2xl font-bold mb-4 text-[var(--text-color)]"
            >
                Ready to start writing?
            </h2>
            <p
                class="text-base leading-relaxed text-[var(--text-color)] opacity-60 mb-8"
            >
                No sign-up required. Open the editor and start creating
                beautiful documents in seconds. Sign in with Google, GitHub, or
                email to unlock sharing, AI refinement, and cloud sync.
            </p>
            <div class="flex items-center justify-center gap-3 flex-wrap">
                <button
                    class="inline-flex items-center gap-2 px-6 py-3 text-[15px] font-medium text-white bg-primary border-none rounded-md cursor-pointer transition-opacity duration-200 hover:opacity-90 active:opacity-80"
                    @click="$emit('start-writing')"
                >
                    Open the Editor
                </button>
                <router-link
                    to="/docs"
                    class="inline-flex items-center gap-2 px-6 py-3 text-[15px] font-medium text-[var(--text-color)] bg-transparent border border-[var(--border-color)] rounded-md no-underline transition-colors duration-200 hover:bg-[var(--border-color)]"
                >
                    Read the Docs
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
defineEmits<{
    (e: "start-writing"): void;
}>();
</script>
