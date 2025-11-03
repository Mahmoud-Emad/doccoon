import { computed, type Ref } from 'vue';
import type { Book } from '@/types';
import type { ImageInfo } from './useImage';
import { useImage } from './useImage';

export function useBookImages(book: Ref<Book>) {
  const { extractImagesFromMarkdown, getImageInfoFromDataUrl } = useImage();

  /**
   * Extract all images from the book
   */
  const allImages = computed(async (): Promise<ImageInfo[]> => {
    const imageUsage = new Map<string, number[]>();

    // Iterate through all spreads
    for (let spreadIndex = 0; spreadIndex < book.value.spreads.length; spreadIndex++) {
      const spread = book.value.spreads[spreadIndex];
      if (!spread) continue;

      // Extract images from left page
      const leftImages = extractImagesFromMarkdown(spread.left);
      for (const dataUrl of leftImages) {
        if (!imageUsage.has(dataUrl)) {
          imageUsage.set(dataUrl, []);
        }
        imageUsage.get(dataUrl)!.push(spreadIndex);
      }

      // Extract images from right page
      const rightImages = extractImagesFromMarkdown(spread.right);
      for (const dataUrl of rightImages) {
        if (!imageUsage.has(dataUrl)) {
          imageUsage.set(dataUrl, []);
        }
        imageUsage.get(dataUrl)!.push(spreadIndex);
      }
    }

    // Create ImageInfo objects for unique images
    const images: ImageInfo[] = [];
    let index = 0;
    for (const [dataUrl, usedInPages] of imageUsage.entries()) {
      try {
        const info = await getImageInfoFromDataUrl(dataUrl, `image-${index++}`);
        images.push({
          id: `img_${Date.now()}_${index}`,
          dataUrl,
          filename: info.filename || `image-${index}`,
          format: info.format || 'image/png',
          size: info.size || 0,
          width: info.width || 0,
          height: info.height || 0,
          uploadedAt: Date.now(),
          usedInPages: Array.from(new Set(usedInPages)).sort()
        });
      } catch (error) {
        console.error('Failed to get image info:', error);
      }
    }

    return images;
  });

  /**
   * Get images synchronously (for immediate use)
   */
  function getImagesSync(): ImageInfo[] {
    const imageMap = new Map<string, Set<number>>();

    // Iterate through all spreads
    for (let spreadIndex = 0; spreadIndex < book.value.spreads.length; spreadIndex++) {
      const spread = book.value.spreads[spreadIndex];
      if (!spread) continue;

      // Extract images from both pages
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

    // Create simplified ImageInfo objects
    const images: ImageInfo[] = [];
    let index = 0;
    for (const [dataUrl, usedInPages] of imageMap.entries()) {
      // Extract basic info from data URL
      const formatMatch = dataUrl.match(/^data:(image\/[^;]+);/);
      const format = formatMatch ? formatMatch[1] : 'image/png';

      // Estimate size from base64 length
      const base64Length = dataUrl.split(',')[1]?.length || 0;
      const estimatedSize = Math.floor((base64Length * 3) / 4);

      images.push({
        id: `img_sync_${index++}`,
        dataUrl,
        filename: `image-${index}`,
        format: format || 'image/png',
        size: estimatedSize,
        width: 0, // Will be loaded asynchronously if needed
        height: 0,
        uploadedAt: Date.now(),
        usedInPages: Array.from(usedInPages).sort()
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
   * This is a utility function that can be called to clean up
   */
  function removeUnusedImages(content: string, usedImages: string[]): string {
    let cleanedContent = content;

    // Extract all images from content
    const allImages = extractImagesFromMarkdown(content);

    // Remove images that are not in the usedImages list
    for (const imageUrl of allImages) {
      if (!usedImages.includes(imageUrl)) {
        // Remove markdown image syntax
        const markdownPattern = new RegExp(`!\\[[^\\]]*\\]\\(${escapeRegExp(imageUrl)}\\)`, 'g');
        cleanedContent = cleanedContent.replace(markdownPattern, '');

        // Remove HTML img tags
        const htmlPattern = new RegExp(`<img[^>]+src=["']${escapeRegExp(imageUrl)}["'][^>]*>`, 'g');
        cleanedContent = cleanedContent.replace(htmlPattern, '');
      }
    }

    return cleanedContent;
  }

  /**
   * Escape special regex characters
   */
  function escapeRegExp(string: string): string {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
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
  function canAddImage(imageSize: number): { canAdd: boolean; reason?: string } {
    const currentSize = getTotalImageSize();
    const totalSize = currentSize + imageSize;

    // LocalStorage limit is typically 5-10MB
    // We'll use 8MB as a safe limit
    const MAX_STORAGE = 8 * 1024 * 1024; // 8MB

    if (totalSize > MAX_STORAGE) {
      const currentMB = (currentSize / (1024 * 1024)).toFixed(2);
      const maxMB = (MAX_STORAGE / (1024 * 1024)).toFixed(0);
      return {
        canAdd: false,
        reason: `Storage limit exceeded. Current: ${currentMB}MB, Max: ${maxMB}MB`
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
    canAddImage
  };
}

