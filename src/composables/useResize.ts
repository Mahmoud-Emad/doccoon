import { ref } from 'vue';

export function useResize() {
  const isResizing = ref(false);
  const startX = ref(0);
  const startLeftWidth = ref(0);
  const startRightWidth = ref(0);
  
  function startResize(e: MouseEvent, leftWidth: number, rightWidth: number) {
    isResizing.value = true;
    startX.value = e.clientX;
    startLeftWidth.value = leftWidth;
    startRightWidth.value = rightWidth;
    
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
  }
  
  function handleResize(
    e: MouseEvent,
    onUpdate: (leftWidth: number, rightWidth: number) => void
  ) {
    if (!isResizing.value) return;
    
    const delta = e.clientX - startX.value;
    const containerWidth = window.innerWidth;
    const deltaFlex = (delta / containerWidth) * 2; // Approximate flex change
    
    let newLeftWidth = Math.max(0.2, startLeftWidth.value + deltaFlex);
    let newRightWidth = Math.max(0.2, startRightWidth.value - deltaFlex);
    
    // Normalize to maintain total
    const total = newLeftWidth + newRightWidth;
    newLeftWidth = newLeftWidth / total;
    newRightWidth = newRightWidth / total;
    
    onUpdate(newLeftWidth, newRightWidth);
  }
  
  function stopResize() {
    isResizing.value = false;
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
  }
  
  return {
    isResizing,
    startResize,
    handleResize,
    stopResize
  };
}

