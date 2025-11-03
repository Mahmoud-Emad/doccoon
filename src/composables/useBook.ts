import { ref, computed } from 'vue';
import type { Book, Spread } from '@/types';

export function useBook() {
  const book = ref<Book>({
    filename: '',
    spreads: [{ left: '', right: '', leftWidth: '1', rightWidth: '1' }]
  });
  
  const currentSpreadIndex = ref(0);
  
  const currentSpread = computed(() => 
    book.value.spreads[currentSpreadIndex.value]
  );
  
  const totalSpreads = computed(() => 
    book.value.spreads.length
  );
  
  const canGoPrevious = computed(() => 
    currentSpreadIndex.value > 0
  );
  
  const canGoNext = computed(() => 
    currentSpreadIndex.value < book.value.spreads.length - 1
  );
  
  function addSpread() {
    book.value.spreads.push({ 
      left: '', 
      right: '', 
      leftWidth: '1', 
      rightWidth: '1' 
    });
    currentSpreadIndex.value = book.value.spreads.length - 1;
  }
  
  function deleteSpread(index: number): boolean {
    if (book.value.spreads.length === 1) {
      return false; // Can't delete last spread
    }
    
    book.value.spreads.splice(index, 1);
    
    if (currentSpreadIndex.value >= book.value.spreads.length) {
      currentSpreadIndex.value = book.value.spreads.length - 1;
    }
    
    return true;
  }
  
  function updateSpread(index: number, data: Partial<Spread>) {
    Object.assign(book.value.spreads[index], data);
  }
  
  function goToNext() {
    if (canGoNext.value) {
      currentSpreadIndex.value++;
    }
  }
  
  function goToPrevious() {
    if (canGoPrevious.value) {
      currentSpreadIndex.value--;
    }
  }
  
  function generateFilename(): string {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    return `book-${year}${month}${day}-${hours}${minutes}`;
  }
  
  function createNewBook() {
    book.value = {
      filename: generateFilename(),
      spreads: [{ left: '', right: '', leftWidth: '1', rightWidth: '1' }]
    };
    currentSpreadIndex.value = 0;
  }
  
  return {
    book,
    currentSpreadIndex,
    currentSpread,
    totalSpreads,
    canGoPrevious,
    canGoNext,
    addSpread,
    deleteSpread,
    updateSpread,
    goToNext,
    goToPrevious,
    generateFilename,
    createNewBook
  };
}

