import { ref } from 'vue';

export function useDragDrop() {
  const isDragging = ref(false);
  
  function isImageUrl(url: string): boolean {
    const imageExtensions = /\.(jpg|jpeg|png|gif|bmp|svg|webp|ico)(\?.*)?$/i;
    if (imageExtensions.test(url)) return true;
    
    const imageIndicators = [
      '/images/', '/img/', 'image', 'photo', 'picture',
      '.googleusercontent.com', 'imgur.com', 'flickr.com',
      'unsplash.com', 'pexels.com'
    ];
    
    return imageIndicators.some(indicator => url.toLowerCase().includes(indicator));
  }
  
  function getImageAltText(url: string): string {
    try {
      const urlObj = new URL(url);
      const pathname = urlObj.pathname;
      const filename = pathname.split('/').pop() || '';
      const nameWithoutExt = filename.replace(/\.[^/.]+$/, '');
      return nameWithoutExt || 'image';
    } catch {
      return 'image';
    }
  }
  
  function handleDragOver(e: DragEvent) {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer) {
      e.dataTransfer.dropEffect = 'copy';
    }
    isDragging.value = true;
  }
  
  function handleDragLeave(e: DragEvent) {
    e.preventDefault();
    e.stopPropagation();
    isDragging.value = false;
  }
  
  async function handleDrop(
    e: DragEvent, 
    onInsert: (text: string, cursorPos: number) => void,
    cursorPos: number
  ): Promise<void> {
    e.preventDefault();
    e.stopPropagation();
    isDragging.value = false;
    
    const items = e.dataTransfer?.items;
    const files = e.dataTransfer?.files;
    
    if (!items && !files) return;
    
    // Handle files
    if (files && files.length > 0) {
      for (const file of Array.from(files)) {
        if (file.type.startsWith('image/')) {
          const base64 = await fileToBase64(file);
          const imageName = file.name.replace(/\.[^/.]+$/, '');
          const markdown = `![${imageName}](${base64})`;
          onInsert(markdown, cursorPos);
        } else {
          const markdown = `[${file.name}](file://${file.name})`;
          onInsert(markdown, cursorPos);
        }
      }
      return;
    }
    
    // Handle URLs/HTML
    if (items) {
      let processed = false;
      
      // First try to get HTML content (for image elements)
      for (const item of Array.from(items)) {
        if (item.kind === 'string' && item.type === 'text/html') {
          item.getAsString((html) => {
            const imgMatch = html.match(/<img[^>]+src="([^">]+)"/i);
            if (imgMatch && imgMatch[1]) {
              const imageUrl = imgMatch[1];
              const altMatch = html.match(/<img[^>]+alt="([^">]+)"/i);
              const altText = altMatch ? altMatch[1] : getImageAltText(imageUrl);
              const markdown = `![${altText}](${imageUrl})`;
              onInsert(markdown, cursorPos);
            }
          });
          processed = true;
          break;
        }
      }
      
      // If no HTML, try text/uri-list or text/plain
      if (!processed) {
        for (const item of Array.from(items)) {
          if (item.kind === 'string' && item.type === 'text/uri-list') {
            item.getAsString((url) => {
              url = url.trim();
              const markdown = isImageUrl(url)
                ? `![${getImageAltText(url)}](${url})`
                : `[${url.split('/').pop() || url}](${url})`;
              onInsert(markdown, cursorPos);
            });
            processed = true;
            break;
          } else if (item.kind === 'string' && item.type === 'text/plain') {
            item.getAsString((text) => {
              text = text.trim();
              const urlPattern = /^(https?:\/\/|www\.)/i;
              let markdown = text;
              
              if (urlPattern.test(text)) {
                markdown = isImageUrl(text)
                  ? `![${getImageAltText(text)}](${text})`
                  : `[${text.split('/').pop() || text}](${text})`;
              }
              
              onInsert(markdown, cursorPos);
            });
            processed = true;
            break;
          }
        }
      }
    }
  }
  
  function fileToBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target?.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }
  
  return {
    isDragging,
    handleDragOver,
    handleDragLeave,
    handleDrop
  };
}

