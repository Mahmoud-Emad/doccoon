<template>
    <BaseModal
        :visible="visible"
        title="Select a Book"
        size="md"
        @close="handleClose"
    >
        <div class="flex flex-col gap-4">
            <!-- Loading State -->
            <div v-if="loading" class="flex items-center justify-center py-12">
                <div class="flex flex-col items-center gap-3">
                    <div
                        class="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin"
                    />
                    <span class="text-sm text-[var(--text-color)] opacity-60">
                        Loading your books...
                    </span>
                </div>
            </div>

            <!-- Empty State -->
            <div
                v-else-if="books.length === 0"
                class="flex flex-col items-center justify-center py-12 gap-4"
            >
                <div
                    class="w-16 h-16 rounded-full bg-[var(--section-alt-bg)] flex items-center justify-center"
                >
                    <BaseIcon
                        name="book-open"
                        :size="32"
                        class="text-[var(--text-color)] opacity-40"
                    />
                </div>
                <div class="text-center">
                    <p
                        class="text-sm font-medium text-[var(--text-color)] mb-1"
                    >
                        No books yet
                    </p>
                    <p class="text-xs text-[var(--text-color)] opacity-60">
                        Create your first book to get started
                    </p>
                </div>
                <button
                    class="flex items-center gap-2 px-4 py-2 bg-primary text-white text-sm font-medium rounded-md border-none cursor-pointer transition-all duration-200 hover:opacity-90 hover:translate-y-[-1px] shadow-[0_4px_12px_rgba(0,122,204,0.3)]"
                    @click="handleCreateNew"
                >
                    <BaseIcon name="plus" :size="16" />
                    Create New Book
                </button>
            </div>

            <!-- Books List -->
            <template v-else>
                <!-- Create New Button -->
                <button
                    class="w-full flex items-center gap-3 p-4 bg-[var(--section-alt-bg)] border border-dashed border-[var(--border-color)] rounded-lg cursor-pointer transition-all duration-200 hover:border-primary hover:bg-primary/5"
                    @click="handleCreateNew"
                >
                    <div
                        class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center shrink-0"
                    >
                        <BaseIcon name="plus" :size="20" class="text-primary" />
                    </div>
                    <div class="text-left">
                        <span
                            class="block text-sm font-medium text-[var(--text-color)]"
                        >
                            Create New Book
                        </span>
                        <span
                            class="block text-xs text-[var(--text-color)] opacity-60"
                        >
                            Start fresh with a blank book
                        </span>
                    </div>
                </button>

                <!-- Divider -->
                <div class="flex items-center gap-3">
                    <div class="flex-1 h-px bg-[var(--border-color)]" />
                    <span class="text-xs text-[var(--text-color)] opacity-50">
                        or continue editing
                    </span>
                    <div class="flex-1 h-px bg-[var(--border-color)]" />
                </div>

                <!-- Books Grid -->
                <div class="flex flex-col gap-2 max-h-[320px] overflow-y-auto">
                    <button
                        v-for="book in books"
                        :key="book.id"
                        class="w-full flex items-center gap-3 p-4 bg-[var(--section-alt-bg)] border border-[var(--border-color)] rounded-lg cursor-pointer transition-all duration-200 hover:border-primary/30 hover:shadow-md text-left"
                        @click="handleSelectBook(book)"
                    >
                        <!-- Book Icon -->
                        <div
                            class="w-10 h-10 rounded-lg bg-[var(--bg-color)] border border-[var(--border-color)] flex items-center justify-center shrink-0"
                        >
                            <BaseIcon
                                name="book"
                                :size="20"
                                class="text-[var(--text-color)] opacity-60"
                            />
                        </div>

                        <!-- Book Info -->
                        <div class="flex-1 min-w-0">
                            <div class="flex items-center gap-2 mb-0.5">
                                <span
                                    class="text-sm font-medium text-[var(--text-color)] truncate"
                                >
                                    {{ book.title }}
                                </span>
                                <span
                                    :class="[
                                        'shrink-0 px-2 py-0.5 text-[10px] font-medium rounded-full',
                                        book.status === 'Published'
                                            ? 'bg-green-500/10 text-green-500'
                                            : 'bg-primary/10 text-primary',
                                    ]"
                                >
                                    {{ book.status }}
                                </span>
                            </div>
                            <div
                                class="flex items-center gap-3 text-xs text-[var(--text-color)] opacity-50"
                            >
                                <span>{{ book.page_count }} pages</span>
                                <span>{{ formatDate(book.modified_at) }}</span>
                            </div>
                        </div>

                        <!-- Arrow Icon -->
                        <BaseIcon
                            name="chevron-right"
                            :size="16"
                            class="text-[var(--text-color)] opacity-30 shrink-0"
                        />
                    </button>
                </div>
            </template>
        </div>

        <template #footer>
            <button
                class="px-4 py-2 text-sm font-medium text-[var(--text-color)] bg-transparent border border-[var(--border-color)] rounded-md cursor-pointer transition-colors duration-200 hover:bg-[var(--section-alt-bg)]"
                @click="handleClose"
            >
                Cancel
            </button>
        </template>
    </BaseModal>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import BaseModal from "@/components/ui/BaseModal.vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import { getBooks } from "@/api/books";
import type { BookSummary } from "@/types";

const props = defineProps<{
    visible: boolean;
}>();

const emit = defineEmits<{
    "update:visible": [value: boolean];
    select: [book: BookSummary];
    create: [];
    close: [];
}>();

const books = ref<BookSummary[]>([]);
const loading = ref(false);

async function fetchBooks() {
    loading.value = true;
    try {
        books.value = await getBooks();
    } catch {
        books.value = [];
    } finally {
        loading.value = false;
    }
}

function formatDate(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
        return "Today";
    } else if (diffDays === 1) {
        return "Yesterday";
    } else if (diffDays < 7) {
        return `${diffDays} days ago`;
    } else {
        return date.toLocaleDateString("en-US", {
            month: "short",
            day: "numeric",
            year: date.getFullYear() !== now.getFullYear() ? "numeric" : undefined,
        });
    }
}

function handleSelectBook(book: BookSummary) {
    emit("select", book);
    emit("update:visible", false);
}

function handleCreateNew() {
    emit("create");
    emit("update:visible", false);
}

function handleClose() {
    emit("close");
    emit("update:visible", false);
}

// Fetch books when dialog opens
watch(
    () => props.visible,
    (visible) => {
        if (visible) {
            fetchBooks();
        }
    },
);
</script>
