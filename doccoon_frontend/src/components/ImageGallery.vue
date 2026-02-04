<template>
    <BaseModal
        :visible="visible"
        title="Image Gallery"
        size="xl"
        @close="close"
    >
        <div
            v-if="images.length === 0"
            class="flex flex-col items-center justify-center py-16 px-5 text-[var(--text-color)] opacity-60 text-center"
        >
            <BaseIcon
                name="image"
                :size="64"
                :stroke-width="1.5"
                class="mb-4 opacity-40"
            />
            <p class="my-2">No images in this book yet</p>
            <p class="text-sm opacity-70">
                Drag and drop images into the editor or use the "Insert Image"
                button
            </p>
        </div>

        <div
            v-else
            class="grid grid-cols-[repeat(auto-fill,minmax(200px,1fr))] gap-5"
        >
            <div
                v-for="image in images"
                :key="image.id"
                class="flex flex-col gap-2"
            >
                <div
                    class="relative aspect-square rounded-lg overflow-hidden bg-[var(--border-color)] cursor-pointer transition-transform duration-200 hover:scale-[1.02] group"
                    @click="previewImage(image)"
                >
                    <img
                        :src="image.dataUrl"
                        :alt="image.filename"
                        class="w-full h-full object-cover"
                    />
                    <div
                        class="absolute inset-0 bg-black/60 flex items-center justify-center gap-3 opacity-0 transition-opacity duration-200 group-hover:opacity-100"
                    >
                        <button
                            class="bg-white border-none rounded-full w-9 h-9 flex items-center justify-center cursor-pointer transition-transform duration-200 text-gray-700 hover:scale-110"
                            title="Insert into page"
                            @click.stop="insertImage(image)"
                        >
                            <BaseIcon name="plus" :size="16" />
                        </button>
                        <button
                            class="bg-white border-none rounded-full w-9 h-9 flex items-center justify-center cursor-pointer transition-transform duration-200 text-gray-700 hover:scale-110"
                            title="Copy markdown"
                            @click.stop="copyMarkdown(image)"
                        >
                            <BaseIcon name="copy" :size="16" />
                        </button>
                    </div>
                </div>
                <div class="flex flex-col gap-1">
                    <div
                        class="text-[13px] font-medium text-[var(--text-color)] whitespace-nowrap overflow-hidden text-ellipsis"
                        :title="image.filename"
                    >
                        {{ image.filename }}
                    </div>
                    <div
                        class="text-xs text-[var(--text-color)] opacity-60 flex gap-2"
                    >
                        <span>{{ image.width }} x {{ image.height }}</span>
                        <span>{{ formatFileSize(image.size) }}</span>
                    </div>
                    <div
                        v-if="image.usedInPages.length > 0"
                        class="text-[11px] text-primary font-medium"
                    >
                        Used in {{ image.usedInPages.length }} page(s)
                    </div>
                </div>
            </div>
        </div>

        <template #footer>
            <div class="flex items-center justify-between w-full">
                <span class="text-[13px] text-[var(--text-color)] opacity-70">
                    {{ images.length }} image(s) -- {{ totalSize }}
                </span>
                <BaseButton variant="secondary" size="sm" @click="close"
                    >Close</BaseButton
                >
            </div>
        </template>
    </BaseModal>

    <!-- Image Preview Modal -->
    <BaseModal :visible="!!previewImageData" size="full" @close="closePreview">
        <div v-if="previewImageData" class="flex flex-col items-center gap-4">
            <img
                :src="previewImageData.dataUrl"
                :alt="previewImageData.filename"
                class="max-w-full max-h-[calc(90vh-200px)] object-contain rounded"
            />
            <div
                class="bg-white/10 backdrop-blur-lg px-5 py-3 rounded-lg text-center"
            >
                <div class="text-[var(--text-color)] text-sm font-medium mb-1">
                    {{ previewImageData.filename }}
                </div>
                <div class="text-[var(--text-color)] opacity-70 text-xs">
                    {{ previewImageData.width }} x
                    {{ previewImageData.height }} --
                    {{ formatFileSize(previewImageData.size) }}
                </div>
            </div>
        </div>
    </BaseModal>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import type { ImageInfo } from "@/composables/useImage";
import { useImage } from "@/composables/useImage";
import BaseModal from "@/components/ui/BaseModal.vue";
import BaseButton from "@/components/ui/BaseButton.vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import { logger } from "@/utils/logger";

const props = defineProps<{
    visible: boolean;
    images: ImageInfo[];
}>();

const emit = defineEmits<{
    close: [];
    "insert-image": [ImageInfo];
}>();

const { formatFileSize, generateImageMarkdown } = useImage();
const previewImageData = ref<ImageInfo | null>(null);

const totalSize = computed(() => {
    const total = props.images.reduce((sum, img) => sum + img.size, 0);
    return formatFileSize(total);
});

function close() {
    emit("close");
}
function insertImage(image: ImageInfo) {
    emit("insert-image", image);
}

async function copyMarkdown(image: ImageInfo) {
    const markdown = generateImageMarkdown(image);
    try {
        await navigator.clipboard.writeText(markdown);
    } catch (error) {
        logger.error("Failed to copy markdown:", error);
    }
}

function previewImage(image: ImageInfo) {
    previewImageData.value = image;
}
function closePreview() {
    previewImageData.value = null;
}
</script>
