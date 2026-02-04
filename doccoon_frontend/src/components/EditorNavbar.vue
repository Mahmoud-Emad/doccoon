<template>
    <nav
        ref="navRef"
        class="h-[50px] bg-[var(--page-bg)] border-b border-[var(--border-color)] flex items-center justify-between px-3 text-[13px] relative z-[100]"
    >
        <div class="flex items-center gap-1">
            <!-- Home Link -->
            <router-link
                to="/"
                class="flex items-center gap-1.5 px-2 py-1 cursor-pointer text-[var(--text-color)] rounded transition-colors duration-150 no-underline select-none font-medium hover:bg-[var(--border-color)]"
                title="Go to Home"
            >
                <BaseIcon name="home" :size="16" />
                <span class="max-md:hidden">Doccoon</span>
            </router-link>

            <!-- File Menu -->
            <div
                class="flex items-center gap-1.5 px-2 py-1 cursor-pointer text-[var(--text-color)] rounded transition-colors duration-150 select-none relative"
                :class="{
                    'bg-[var(--border-color)]': activeDropdown === 'file',
                }"
                @click="toggleDropdown('file')"
            >
                <span>File</span>
                <div
                    v-if="activeDropdown === 'file'"
                    class="absolute top-full left-0 mt-0.5 bg-[var(--page-bg)] border border-[var(--border-color)] rounded shadow-[0_4px_12px_rgba(0,0,0,0.15)] min-w-[160px] md:min-w-[200px] max-h-[80vh] overflow-y-auto p-1 z-[1000]"
                    @click.stop
                >
                    <button
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center gap-2 text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)]"
                        @click="handleNew"
                    >
                        <BaseIcon name="file" :size="14" />
                        New Book
                    </button>
                    <button
                        v-if="loggedIn"
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center gap-2 text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)]"
                        @click="handleShareBook"
                    >
                        <BaseIcon name="share" :size="14" />
                        Share Book
                    </button>
                    <button
                        v-if="loggedIn"
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center gap-2 text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)]"
                        @click="handlePublishBook"
                    >
                        <BaseIcon name="eye" :size="14" />
                        {{
                            bookStatus === "Published"
                                ? "Unpublish Book"
                                : "Publish Book"
                        }}
                    </button>
                    <div
                        v-if="loggedIn"
                        class="h-px bg-[var(--border-color)] my-1"
                    />
                    <button
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center gap-2 text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)]"
                        @click="handleDeleteBook"
                    >
                        <BaseIcon name="trash" :size="14" />
                        Delete Book
                    </button>
                </div>
            </div>

            <!-- Edit Menu -->
            <div
                class="flex items-center gap-1.5 px-2 py-1 cursor-pointer text-[var(--text-color)] rounded transition-colors duration-150 select-none relative"
                :class="{
                    'bg-[var(--border-color)]': activeDropdown === 'edit',
                }"
                @click="toggleDropdown('edit')"
            >
                <span>Edit</span>
                <div
                    v-if="activeDropdown === 'edit'"
                    class="absolute top-full left-0 mt-0.5 bg-[var(--page-bg)] border border-[var(--border-color)] rounded shadow-[0_4px_12px_rgba(0,0,0,0.15)] min-w-[160px] md:min-w-[200px] max-h-[80vh] overflow-y-auto p-1 z-[1000]"
                    @click.stop
                >
                    <button
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center gap-2 text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)]"
                        @click="handleAddPage"
                    >
                        <BaseIcon name="plus" :size="14" />
                        Add Page Spread
                    </button>
                    <button
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center gap-2 text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)]"
                        @click="handleDeletePage"
                    >
                        <BaseIcon name="x" :size="14" />
                        Delete Page Spread
                    </button>
                </div>
            </div>

            <!-- View Menu -->
            <div
                class="flex items-center gap-1.5 px-2 py-1 cursor-pointer text-[var(--text-color)] rounded transition-colors duration-150 select-none relative"
                :class="{
                    'bg-[var(--border-color)]': activeDropdown === 'view',
                }"
                @click="toggleDropdown('view')"
            >
                <span>View</span>
                <div
                    v-if="activeDropdown === 'view'"
                    class="absolute top-full left-0 mt-0.5 bg-[var(--page-bg)] border border-[var(--border-color)] rounded shadow-[0_4px_12px_rgba(0,0,0,0.15)] min-w-[160px] md:min-w-[200px] max-h-[80vh] overflow-y-auto p-1 z-[1000]"
                    @click.stop
                >
                    <button
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center gap-2 text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)]"
                        :class="{
                            'opacity-40 pointer-events-none': livePreview,
                        }"
                        @click="handleToggleView"
                    >
                        <BaseIcon name="eye" :size="14" />
                        {{ isViewMode ? "Edit Mode" : "View Mode" }}
                    </button>
                    <button
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center gap-2 text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)]"
                        :class="{
                            'opacity-40 pointer-events-none': livePreview,
                        }"
                        @click="handleToggleLayout"
                    >
                        <BaseIcon name="layout" :size="14" />
                        {{ layoutMode === "book" ? "Page View" : "Book View" }}
                    </button>
                    <button
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center gap-2 text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)]"
                        @click="handleTogglePreview"
                    >
                        <BaseIcon name="columns" :size="14" />
                        Live Preview
                        <span v-if="livePreview" class="ml-auto text-primary"
                            >&#10003;</span
                        >
                    </button>
                    <button
                        v-if="isViewMode && layoutMode === 'book'"
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center gap-2 text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)]"
                        @click="handleToggleDiff"
                    >
                        <BaseIcon name="diff" :size="14" />
                        {{ isDiffMode ? "Hide Diff" : "Show Diff" }}
                    </button>
                    <div class="h-px bg-[var(--border-color)] my-1" />
                    <button
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center gap-2 text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)]"
                        @click="handleShowImageGallery"
                    >
                        <BaseIcon name="image" :size="14" />
                        Image Gallery
                    </button>
                </div>
            </div>

            <!-- Help Menu -->
            <div
                class="flex items-center gap-1.5 px-2 py-1 cursor-pointer text-[var(--text-color)] rounded transition-colors duration-150 select-none relative"
                :class="{
                    'bg-[var(--border-color)]': activeDropdown === 'help',
                }"
                @click="toggleDropdown('help')"
            >
                <span>Help</span>
                <div
                    v-if="activeDropdown === 'help'"
                    class="absolute top-full left-0 mt-0.5 bg-[var(--page-bg)] border border-[var(--border-color)] rounded shadow-[0_4px_12px_rgba(0,0,0,0.15)] min-w-[160px] md:min-w-[200px] max-h-[80vh] overflow-y-auto p-1 z-[1000]"
                    @click.stop
                >
                    <button
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center justify-between text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)]"
                        @click="handleShowShortcuts"
                    >
                        <span class="flex items-center gap-2">
                            <BaseIcon name="keyboard" :size="14" />
                            Keyboard Shortcuts
                        </span>
                        <span class="text-[11px] opacity-50">Ctrl+?</span>
                    </button>
                    <div class="h-px bg-[var(--border-color)] my-1" />
                    <a
                        href="/docs"
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center gap-2 text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)] no-underline"
                        @click="closeDropdown"
                    >
                        <BaseIcon name="book-open" :size="14" />
                        Documentation
                    </a>
                    <a
                        href="https://github.com/doccoon/doccoon"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="w-full py-1.5 px-2 bg-transparent border-none text-[var(--text-color)] cursor-pointer flex items-center gap-2 text-[13px] rounded transition-colors duration-150 text-left hover:bg-[var(--border-color)] no-underline"
                        @click="closeDropdown"
                    >
                        <BaseIcon name="github" :size="14" />
                        GitHub
                    </a>
                </div>
            </div>
        </div>

        <div class="flex items-center gap-3">
            <div class="text-[var(--text-color)] opacity-70 text-xs italic">
                {{ filename }}
            </div>
            <button
                class="flex items-center justify-center w-7 h-7 bg-transparent border-none text-[var(--text-color)] cursor-pointer rounded transition-colors duration-150 hover:bg-[var(--border-color)]"
                :title="
                    isFullscreen ? 'Exit Fullscreen (F11)' : 'Fullscreen (F11)'
                "
                @click="toggleFullscreen"
            >
                <BaseIcon
                    :name="isFullscreen ? 'minimize' : 'maximize'"
                    :size="16"
                />
            </button>
            <template v-if="loggedIn">
                <NotificationDropdown />
                <UserProfileDropdown />
            </template>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import UserProfileDropdown from "@/components/UserProfileDropdown.vue";
import NotificationDropdown from "@/components/NotificationDropdown.vue";
import { isAuthenticated } from "@/api/auth";
import { useClickOutside } from "@/composables/useClickOutside";

const loggedIn = ref(isAuthenticated());
const isFullscreen = ref(false);

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

function handleFullscreenChange() {
    isFullscreen.value = !!document.fullscreenElement;
}

onMounted(() => {
    document.addEventListener("fullscreenchange", handleFullscreenChange);
});

onUnmounted(() => {
    document.removeEventListener("fullscreenchange", handleFullscreenChange);
});

defineProps<{
    filename: string;
    isViewMode: boolean;
    layoutMode: "book" | "page";
    isDiffMode?: boolean;
    livePreview?: boolean;
    bookStatus?: string;
}>();

const emit = defineEmits<{
    new: [];
    "publish-book": [];
    "delete-book": [];
    "share-book": [];
    "add-page": [];
    "delete-page": [];
    "toggle-view": [];
    "toggle-layout": [];
    "toggle-preview": [];
    "toggle-diff": [];
    "show-image-gallery": [];
    "show-shortcuts": [];
}>();

const navRef = ref<HTMLElement | null>(null);
const activeDropdown = ref<string | null>(null);

useClickOutside(navRef, () => {
    closeDropdown();
});

function toggleDropdown(menu: string) {
    activeDropdown.value = activeDropdown.value === menu ? null : menu;
}

function closeDropdown() {
    activeDropdown.value = null;
}

function handleNew() {
    emit("new");
    closeDropdown();
}
function handlePublishBook() {
    emit("publish-book");
    closeDropdown();
}
function handleDeleteBook() {
    emit("delete-book");
    closeDropdown();
}
function handleShareBook() {
    emit("share-book");
    closeDropdown();
}
function handleAddPage() {
    emit("add-page");
    closeDropdown();
}
function handleDeletePage() {
    emit("delete-page");
    closeDropdown();
}
function handleToggleView() {
    emit("toggle-view");
    closeDropdown();
}
function handleToggleLayout() {
    emit("toggle-layout");
    closeDropdown();
}
function handleTogglePreview() {
    emit("toggle-preview");
    closeDropdown();
}
function handleToggleDiff() {
    emit("toggle-diff");
    closeDropdown();
}
function handleShowImageGallery() {
    emit("show-image-gallery");
    closeDropdown();
}

function handleShowShortcuts() {
    emit("show-shortcuts");
    closeDropdown();
}
</script>
