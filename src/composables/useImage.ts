import { ref } from 'vue';
import { logger } from '@/utils/logger';

export interface ImageInfo {
  id: string;
  dataUrl: string;
  filename: string;
  format: string;
  size: number; // in bytes
  width: number;
  height: number;
  uploadedAt: number;
  usedInPages: number[]; // spread indices where this image is used
}

export interface ImageValidationResult {
  valid: boolean;
  error?: string;
}

// Supported image formats
const SUPPORTED_FORMATS = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/svg+xml', 'image/webp'];
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const COMPRESSION_QUALITY = 0.85; // JPEG compression quality
const MAX_DIMENSION = 2000; // Max width/height before compression

export function useImage() {
  const isProcessing = ref(false);
  const uploadProgress = ref(0);

  /**
   * Validate image file
   */
  function validateImage(file: File): ImageValidationResult {
    // Check file type
    if (!SUPPORTED_FORMATS.includes(file.type)) {
      return {
        valid: false,
        error: `Unsupported format. Supported formats: PNG, JPG, JPEG, GIF, SVG, WebP`
      };
    }

    // Check file size
    if (file.size > MAX_FILE_SIZE) {
      const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
      const maxSizeMB = (MAX_FILE_SIZE / (1024 * 1024)).toFixed(0);
      return {
        valid: false,
        error: `File too large (${sizeMB}MB). Maximum size: ${maxSizeMB}MB`
      };
    }

    return { valid: true };
  }

  /**
   * Read file as data URL
   */
  function readFileAsDataURL(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target?.result) {
          resolve(e.target.result as string);
        } else {
          reject(new Error('Failed to read file'));
        }
      };
      reader.onerror = () => reject(new Error('Failed to read file'));
      reader.readAsDataURL(file);
    });
  }

  /**
   * Get image dimensions
   */
  function getImageDimensions(dataUrl: string): Promise<{ width: number; height: number }> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => {
        resolve({ width: img.width, height: img.height });
      };
      img.onerror = () => reject(new Error('Failed to load image'));
      img.src = dataUrl;
    });
  }

  /**
   * Compress image if needed
   */
  async function compressImage(dataUrl: string, format: string): Promise<string> {
    // Skip compression for SVG and GIF
    if (format === 'image/svg+xml' || format === 'image/gif') {
      return dataUrl;
    }

    const dimensions = await getImageDimensions(dataUrl);
    
    // Check if compression is needed
    const needsResize = dimensions.width > MAX_DIMENSION || dimensions.height > MAX_DIMENSION;
    const needsCompression = format === 'image/jpeg' || format === 'image/jpg' || format === 'image/png';

    if (!needsResize && !needsCompression) {
      return dataUrl;
    }

    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        let { width, height } = dimensions;

        // Resize if needed
        if (needsResize) {
          const ratio = Math.min(MAX_DIMENSION / width, MAX_DIMENSION / height);
          width = Math.floor(width * ratio);
          height = Math.floor(height * ratio);
        }

        canvas.width = width;
        canvas.height = height;

        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.drawImage(img, 0, 0, width, height);
          
          // Convert to JPEG for better compression (except for PNG with transparency)
          const outputFormat = format === 'image/png' ? 'image/png' : 'image/jpeg';
          const compressed = canvas.toDataURL(outputFormat, COMPRESSION_QUALITY);
          resolve(compressed);
        } else {
          resolve(dataUrl);
        }
      };
      img.src = dataUrl;
    });
  }

  /**
   * Process and upload image
   */
  async function processImage(file: File): Promise<ImageInfo> {
    isProcessing.value = true;
    uploadProgress.value = 0;

    try {
      // Validate
      const validation = validateImage(file);
      if (!validation.valid) {
        throw new Error(validation.error);
      }

      uploadProgress.value = 20;

      // Read file
      const dataUrl = await readFileAsDataURL(file);
      uploadProgress.value = 40;

      // Get dimensions
      const dimensions = await getImageDimensions(dataUrl);
      uploadProgress.value = 60;

      // Compress if needed
      const compressedDataUrl = await compressImage(dataUrl, file.type);
      uploadProgress.value = 80;

      // Create image info
      const imageInfo: ImageInfo = {
        id: `img_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        dataUrl: compressedDataUrl,
        filename: file.name,
        format: file.type,
        size: file.size,
        width: dimensions.width,
        height: dimensions.height,
        uploadedAt: Date.now(),
        usedInPages: []
      };

      uploadProgress.value = 100;
      return imageInfo;
    } catch (error) {
      logger.error('Failed to process image:', error);
      throw error;
    } finally {
      isProcessing.value = false;
      setTimeout(() => {
        uploadProgress.value = 0;
      }, 500);
    }
  }

  /**
   * Generate markdown for image
   */
  function generateImageMarkdown(imageInfo: ImageInfo, options?: {
    alt?: string;
    width?: string;
    height?: string;
    align?: 'left' | 'center' | 'right';
  }): string {
    const alt = options?.alt || imageInfo.filename.replace(/\.[^/.]+$/, '');
    
    // If no sizing or alignment, use simple markdown
    if (!options?.width && !options?.height && !options?.align) {
      return `![${alt}](${imageInfo.dataUrl})`;
    }

    // Use HTML img tag for advanced options
    const attrs: string[] = [`src="${imageInfo.dataUrl}"`, `alt="${alt}"`];
    
    if (options?.width) {
      attrs.push(`width="${options.width}"`);
    }
    if (options?.height) {
      attrs.push(`height="${options.height}"`);
    }

    let imgTag = `<img ${attrs.join(' ')} />`;

    // Wrap in div for alignment
    if (options?.align) {
      const alignStyle = options.align === 'center' 
        ? 'text-align: center;' 
        : options.align === 'right' 
        ? 'text-align: right;' 
        : 'text-align: left;';
      imgTag = `<div style="${alignStyle}">\n${imgTag}\n</div>`;
    }

    return imgTag;
  }

  /**
   * Extract images from markdown content
   */
  function extractImagesFromMarkdown(markdown: string): string[] {
    const images: string[] = [];
    
    // Match markdown images: ![alt](data:image/...)
    const markdownImageRegex = /!\[([^\]]*)\]\((data:image\/[^)]+)\)/g;
    let match;
    while ((match = markdownImageRegex.exec(markdown)) !== null) {
      if (match[2]) {
        images.push(match[2]);
      }
    }

    // Match HTML img tags: <img src="data:image/..." />
    const htmlImageRegex = /<img[^>]+src=["'](data:image\/[^"']+)["'][^>]*>/g;
    while ((match = htmlImageRegex.exec(markdown)) !== null) {
      if (match[1] && !images.includes(match[1])) {
        images.push(match[1]);
      }
    }

    return images;
  }

  /**
   * Format file size for display
   */
  function formatFileSize(bytes: number): string {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  }

  /**
   * Get image info from data URL
   */
  async function getImageInfoFromDataUrl(dataUrl: string, filename?: string): Promise<Partial<ImageInfo>> {
    try {
      const dimensions = await getImageDimensions(dataUrl);
      
      // Extract format from data URL
      const formatMatch = dataUrl.match(/^data:(image\/[^;]+);/);
      const format = formatMatch ? formatMatch[1] : 'image/png';
      
      // Estimate size from base64 length
      const base64Length = dataUrl.split(',')[1]?.length || 0;
      const estimatedSize = Math.floor((base64Length * 3) / 4);

      return {
        dataUrl,
        filename: filename || 'image',
        format,
        size: estimatedSize,
        width: dimensions.width,
        height: dimensions.height
      };
    } catch (error) {
      logger.error('Failed to get image info:', error);
      throw error;
    }
  }

  return {
    isProcessing,
    uploadProgress,
    validateImage,
    processImage,
    generateImageMarkdown,
    extractImagesFromMarkdown,
    formatFileSize,
    getImageInfoFromDataUrl
  };
}

