import { computed, type Ref } from "vue";
import type { Book } from "@/types";
import type { ImageInfo } from "./useImage";
import { useImage } from "./useImage";
import { logger } from "@/utils/logger";
import { escapeRegExp } from "@/utils/html";
import { MAX_IMAGE_STORAGE_SIZE } from "@/config/constants";

export function useBookImages(book: Ref<Book>) {
  const { extractImagesFromMarkdown, getImageInfoFromDataUrl } = useImage();

  /**
   * Extract all images from the book (async version with full metadata)
   */
  const allImages = computed(async (): Promise<ImageInfo[]> => {
    const imageUsage = new Map<string, number[]>();

    for (
      let spreadIndex = 0;
      spreadIndex < book.value.spreads.length;
      spreadIndex++
    ) {
      const spread = book.value.spreads[spreadIndex];
      if (!spread) continue;

      const leftImages = extractImagesFromMarkdown(spread.left);
      for (const dataUrl of leftImages) {
        if (!imageUsage.has(dataUrl)) {
          imageUsage.set(dataUrl, []);
        }
        imageUsage.get(dataUrl)!.push(spreadIndex);
      }

      const rightImages = extractImagesFromMarkdown(spread.right);
      for (const dataUrl of rightImages) {
        if (!imageUsage.has(dataUrl)) {
          imageUsage.set(dataUrl, []);
        }
        imageUsage.get(dataUrl)!.push(spreadIndex);
      }
    }

    const images: ImageInfo[] = [];
    let index = 0;
    for (const [dataUrl, usedInPages] of imageUsage.entries()) {
      try {
        const info = await getImageInfoFromDataUrl(dataUrl, `image-${index++}`);
        images.push({
          id: `img_${Date.now()}_${index}`,
          dataUrl,
          filename: info.filename || `image-${index}`,
          format: info.format || "image/png",
          size: info.size || 0,
          width: info.width || 0,
          height: info.height || 0,
          uploadedAt: Date.now(),
          usedInPages: Array.from(new Set(usedInPages)).sort(),
        });
      } catch (error) {
        logger.error("Failed to get image info:", error);
      }
    }

    return images;
  });

  /**
   * Get images synchronously (for immediate use, without full metadata)
   */
  function getImagesSync(): ImageInfo[] {
    const imageMap = new Map<string, Set<number>>();

    for (
      let spreadIndex = 0;
      spreadIndex < book.value.spreads.length;
      spreadIndex++
    ) {
      const spread = book.value.spreads[spreadIndex];
      if (!spread) continue;

      const leftImages = extractImagesFromMarkdown(spread.left);
      const rightImages = extractImagesFromMarkdown(spread.right);
      const allPageImages = [...leftImages, ...rightImages];

      for (const dataUrl of allPageImages) {
        if (!imageMap.has(dataUrl)) {
          imageMap.set(dataUrl, new Set());
        }
        imageMap.get(dataUrl)!.add(spreadIndex);
      }
    }

    const images: ImageInfo[] = [];
    let index = 0;
    for (const [dataUrl, usedInPages] of imageMap.entries()) {
      const formatMatch = dataUrl.match(/^data:(image\/[^;]+);/);
      const format = formatMatch ? formatMatch[1] : "image/png";

      const base64Length = dataUrl.split(",")[1]?.length || 0;
      const estimatedSize = Math.floor((base64Length * 3) / 4);

      images.push({
        id: `img_sync_${index++}`,
        dataUrl,
        filename: `image-${index}`,
        format: format || "image/png",
        size: estimatedSize,
        width: 0,
        height: 0,
        uploadedAt: Date.now(),
        usedInPages: Array.from(usedInPages).sort(),
      });
    }

    return images;
  }

  /**
   * Check if an image is used in the book
   */
  function isImageUsed(dataUrl: string): boolean {
    for (const spread of book.value.spreads) {
      if (spread.left.includes(dataUrl) || spread.right.includes(dataUrl)) {
        return true;
      }
    }
    return false;
  }

  /**
   * Get pages where an image is used
   */
  function getImageUsage(dataUrl: string): number[] {
    const pages: number[] = [];
    for (let i = 0; i < book.value.spreads.length; i++) {
      const spread = book.value.spreads[i];
      if (!spread) continue;
      if (spread.left.includes(dataUrl) || spread.right.includes(dataUrl)) {
        pages.push(i);
      }
    }
    return pages;
  }

  /**
   * Remove unused images from content
   */
  function removeUnusedImages(content: string, usedImages: string[]): string {
    let cleanedContent = content;

    const allImages = extractImagesFromMarkdown(content);

    for (const imageUrl of allImages) {
      if (!usedImages.includes(imageUrl)) {
        const markdownPattern = new RegExp(
          `!\\[[^\\]]*\\]\\(${escapeRegExp(imageUrl)}\\)`,
          "g",
        );
        cleanedContent = cleanedContent.replace(markdownPattern, "");

        const htmlPattern = new RegExp(
          `<img[^>]+src=["']${escapeRegExp(imageUrl)}["'][^>]*>`,
          "g",
        );
        cleanedContent = cleanedContent.replace(htmlPattern, "");
      }
    }

    return cleanedContent;
  }

  /**
   * Get total size of all images in the book
   */
  function getTotalImageSize(): number {
    const images = getImagesSync();
    return images.reduce((total, img) => total + img.size, 0);
  }

  /**
   * Check if adding a new image would exceed storage limits
   */
  function canAddImage(imageSize: number): {
    canAdd: boolean;
    reason?: string;
  } {
    const currentSize = getTotalImageSize();
    const totalSize = currentSize + imageSize;

    if (totalSize > MAX_IMAGE_STORAGE_SIZE) {
      const currentMB = (currentSize / (1024 * 1024)).toFixed(2);
      const maxMB = (MAX_IMAGE_STORAGE_SIZE / (1024 * 1024)).toFixed(0);
      return {
        canAdd: false,
        reason: `Storage limit exceeded. Current: ${currentMB}MB, Max: ${maxMB}MB`,
      };
    }

    return { canAdd: true };
  }

  return {
    allImages,
    getImagesSync,
    isImageUsed,
    getImageUsage,
    removeUnusedImages,
    getTotalImageSize,
    canAddImage,
  };
}
