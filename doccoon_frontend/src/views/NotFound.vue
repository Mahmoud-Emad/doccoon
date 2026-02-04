<template>
    <div
        class="min-h-screen bg-[var(--bg-color)] text-[var(--text-color)] flex flex-col"
    >
        <!-- Content -->
        <div class="flex-1 flex items-center justify-center px-8 max-md:px-4">
            <div class="max-w-[720px] w-full py-16">
                <div
                    class="flex items-center justify-center gap-5 max-md:flex-col max-md:gap-6 mb-10"
                >
                    <img
                        :src="logo404"
                        alt=""
                        class="w-[180px] max-md:w-[140px] shrink-0"
                    />
                    <div class="max-md:text-center">
                        <h1
                            class="text-[96px] max-md:text-[72px] font-bold m-0 leading-none text-primary"
                        >
                            404
                        </h1>
                    </div>
                </div>

                <div class="text-center mb-10">
                    <h2
                        class="text-xl font-semibold m-0 mb-3 text-[var(--text-color)]"
                    >
                        Page not found
                    </h2>
                    <p
                        class="text-base leading-relaxed m-0 text-[var(--text-color)] opacity-60 max-w-[480px] mx-auto"
                    >
                        The page you're looking for doesn't exist or has been
                        moved. Here are some helpful links to get you back on
                        track.
                    </p>
                </div>

                <div class="flex items-center justify-center gap-3 flex-wrap">
                    <router-link
                        to="/"
                        class="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium text-white bg-primary no-underline rounded-md transition-opacity duration-200 hover:opacity-90"
                    >
                        <BaseIcon name="home" :size="16" />
                        Home
                    </router-link>
                    <router-link
                        to="/edit"
                        class="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium text-[var(--text-color)] bg-transparent no-underline border border-[var(--border-color)] rounded-md transition-colors duration-200 hover:bg-[var(--section-alt-bg)]"
                    >
                        <BaseIcon name="edit" :size="16" />
                        Editor
                    </router-link>
                    <router-link
                        to="/profile"
                        class="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-medium text-[var(--text-color)] bg-transparent no-underline border border-[var(--border-color)] rounded-md transition-colors duration-200 hover:bg-[var(--section-alt-bg)]"
                    >
                        <BaseIcon name="user" :size="16" />
                        Profile
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import BaseIcon from "@/components/ui/BaseIcon.vue";
import logo404 from "@/assets/logo-404.png";
</script>
