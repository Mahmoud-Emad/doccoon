<template>
    <div class="py-24 px-8 max-md:py-16 max-md:px-5 bg-[var(--section-alt-bg)]">
        <div class="max-w-[1000px] mx-auto">
            <p
                class="text-center text-sm font-semibold tracking-widest uppercase text-primary mb-3"
            >
                About Doccoon
            </p>
            <h2
                class="text-center text-[32px] max-md:text-2xl font-bold mb-4 text-[var(--text-color)] leading-tight"
            >
                Writing tools built for the way you think
            </h2>
            <p
                class="text-center text-base max-md:text-[15px] leading-relaxed text-[var(--text-color)] opacity-60 max-w-[640px] mx-auto mb-16"
            >
                Doccoon is a modern document editor that combines the elegance
                of a book layout with the power of markdown, diagrams, math, and
                AI. Cloud-synced, privacy-respecting, and built on open
                standards &mdash; your content stays yours.
            </p>

            <div class="grid grid-cols-3 max-md:grid-cols-1 gap-10">
                <div
                    v-for="pillar in pillars"
                    :key="pillar.title"
                    class="text-center"
                >
                    <div
                        class="w-12 h-12 mx-auto mb-4 rounded-lg bg-primary/10 flex items-center justify-center"
                        v-html="pillar.icon"
                    ></div>
                    <h3
                        class="text-base font-semibold mb-2 text-[var(--text-color)]"
                    >
                        {{ pillar.title }}
                    </h3>
                    <p
                        class="text-sm leading-relaxed text-[var(--text-color)] opacity-60 m-0"
                    >
                        {{ pillar.description }}
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
const pillars = [
    {
        title: "Your Data, Your Control",
        description:
            "Your data is stored securely on our servers when signed in. You choose what to share and with whom. No tracking, no telemetry.",
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#007ACC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    },
    {
        title: "Write Anywhere",
        description:
            "Access your books from any device. Sign in and your content syncs automatically. Works great in any modern browser.",
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#007ACC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    },
    {
        title: "Open & Extensible",
        description:
            "Built on open standards like Markdown, Mermaid, and KaTeX. Bring your own AI provider. Your content is portable and never locked in.",
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#007ACC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
    },
];
</script>
