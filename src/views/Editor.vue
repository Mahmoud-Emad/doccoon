<template>
  <LoadingScreen :visible="isLoading" />

  <div class="container" :class="{ loaded: !isLoading }">
    <!-- Editor Navbar -->
    <EditorNavbar :filename="book.filename" :is-view-mode="isViewMode" :is-dark-theme="isDarkTheme"
      :layout-mode="layoutMode" :is-diff-mode="isDiffMode" @new="handleNewBook" @delete-book="handleDeleteBook"
      @add-page="addSpread" @delete-page="handleDeletePage" @toggle-view="handleToggleView"
      @toggle-layout="handleToggleLayoutMode" @toggle-diff="toggleDiffMode" @toggle-theme="toggleTheme" />

    <BookSpread :spread="displaySpread" :is-view-mode="isViewMode" :layout-mode="layoutMode" :is-diff-mode="isDiffMode"
      :left-diff-content="leftDiffContent" :right-diff-content="rightDiffContent" :render-markdown="renderMarkdown"
      @update:spread="updateCurrentSpread" @open-page-view="handleOpenPageView"
      @toggle-layout="handleToggleLayoutMode" />

    <FooterControls :current-index="currentSpreadIndex" :total-pages="totalSpreads" :can-go-previous="canGoPrevious"
      :can-go-next="canGoNext" :filename="book.filename" :status="saveStatus" :is-view-mode="isViewMode"
      :is-dark-theme="isDarkTheme" :layout-mode="layoutMode" @prev="goToPrevious" @next="goToNext" @add="addSpread"
      @update:filename="updateFilename" @new="handleNewBook" @delete-page="handleDeletePage"
      @delete-book="handleDeleteBook" @toggle-layout="handleToggleLayoutMode" @toggle-view="handleToggleView"
      @toggle-theme="toggleTheme" />
  </div>

  <Modal :visible="modalState.visible" :title="modalState.title" :message="modalState.message"
    :is-danger="modalState.isDanger" @confirm="confirm" @cancel="cancel" />

  <PageSelectionModal :visible="pageSelectionModalVisible" title="Select Page to View"
    message="Which page would you like to view in Page View mode?" @select-left="handleSelectLeftPage"
    @select-right="handleSelectRightPage" @cancel="handleCancelPageSelection" />
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import LoadingScreen from '@/components/LoadingScreen.vue';
import EditorNavbar from '@/components/EditorNavbar.vue';
import BookSpread from '@/components/BookSpread.vue';
import FooterControls from '@/components/Footer/FooterControls.vue';
import Modal from '@/components/Modal.vue';
import PageSelectionModal from '@/components/PageSelectionModal.vue';

import { useBook } from '@/composables/useBook';
import { useTheme } from '@/composables/useTheme';
import { useViewMode } from '@/composables/useViewMode';
import { useLayoutMode } from '@/composables/useLayoutMode';
import { useStorage } from '@/composables/useStorage';
import { useMarkdown } from '@/composables/useMarkdown';
import { useModal } from '@/composables/useModal';
import { useDiff } from '@/composables/useDiff';
import { logger } from '@/utils/logger';

import type { Spread } from '@/types';

const route = useRoute();
const router = useRouter();

// Track if we're viewing an example (don't auto-save examples)
const isViewingExample = ref(false);

// Initialize composables
const {
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
} = useBook();

const { isDarkTheme, toggleTheme } = useTheme();
const { isViewMode, setViewMode } = useViewMode();
const { layoutMode, toggleLayoutMode, setLayoutMode } = useLayoutMode();
const { saveStatus, loadBook, deleteBook } = useStorage(book, isViewingExample);
const { renderMarkdown } = useMarkdown(isDarkTheme);
const { modalState, showModal, confirm, cancel } = useModal();
const { isDiffMode, toggleDiffMode, computeDiff, renderDiffToHtml } = useDiff();

// Loading state
const isLoading = ref(true);

// Track which page to show in page view mode ('left' or 'right')
const pageViewSide = ref<'left' | 'right'>('left');

// Page selection modal state
const pageSelectionModalVisible = ref(false);

// Computed spread to display based on layout mode and selected page
const displaySpread = computed(() => {
  const spread = currentSpread.value;
  if (!spread) {
    return {
      left: '',
      right: '',
      leftWidth: '50%',
      rightWidth: '50%'
    };
  }

  if (layoutMode.value === 'page') {
    // In page view mode, show only the selected page
    if (pageViewSide.value === 'left') {
      return spread;
    } else {
      // Show right page content in the left position
      return {
        ...spread,
        left: spread.right,
        right: ''
      };
    }
  }
  // In book view mode, show both pages normally
  return spread;
});

// Computed diff content for left and right pages
const leftDiffContent = computed(() => {
  if (!isDiffMode.value || !isViewMode.value || layoutMode.value !== 'book') {
    return undefined;
  }
  const spread = currentSpread.value;
  if (!spread) return undefined;

  const diff = computeDiff(spread.left, spread.right);
  // Show removed lines on left (content in left but not in right)
  return renderDiffToHtml(diff.left);
});

const rightDiffContent = computed(() => {
  if (!isDiffMode.value || !isViewMode.value || layoutMode.value !== 'book') {
    return undefined;
  }
  const spread = currentSpread.value;
  if (!spread) return undefined;

  const diff = computeDiff(spread.left, spread.right);
  // Show added lines on right (content in right but not in left)
  return renderDiffToHtml(diff.right);
});

// Update current spread
function updateCurrentSpread(data: Partial<Spread>) {
  // If in page view mode showing the right page, map the left content to right
  if (layoutMode.value === 'page' && pageViewSide.value === 'right' && data.left !== undefined) {
    updateSpread(currentSpreadIndex.value, { right: data.left });
  } else {
    updateSpread(currentSpreadIndex.value, data);
  }
}

// Handle opening a page in page view mode
function handleOpenPageView(side: 'left' | 'right') {
  pageViewSide.value = side;
  setLayoutMode('page');
}

// Handle layout mode toggle with page selection
function handleToggleLayoutMode() {
  // If currently in book view and switching to page view, show selection modal
  if (layoutMode.value === 'book') {
    pageSelectionModalVisible.value = true;
  } else {
    // If currently in page view, just toggle back to book view
    toggleLayoutMode();
  }
}

// Handle page selection modal - Left page
function handleSelectLeftPage() {
  pageViewSide.value = 'left';
  pageSelectionModalVisible.value = false;
  setLayoutMode('page');
}

// Handle page selection modal - Right page
function handleSelectRightPage() {
  pageViewSide.value = 'right';
  pageSelectionModalVisible.value = false;
  setLayoutMode('page');
}

// Handle page selection modal - Cancel
function handleCancelPageSelection() {
  pageSelectionModalVisible.value = false;
}

// Update filename
function updateFilename(newFilename: string) {
  book.value.filename = newFilename;
}

// Handle new book
async function handleNewBook() {
  const confirmed = await showModal({
    title: 'Create New Book',
    message: 'Are you sure you want to create a new book? All current content will be lost.',
    isDanger: true
  });

  if (confirmed) {
    createNewBook();
  }
}

// Handle delete page
async function handleDeletePage() {
  if (totalSpreads.value === 1) {
    await showModal({
      title: 'Cannot Delete',
      message: 'You cannot delete the last page spread.',
      isDanger: false
    });
    return;
  }

  const confirmed = await showModal({
    title: 'Delete Page Spread',
    message: 'Are you sure you want to delete this page spread?',
    isDanger: true
  });

  if (confirmed) {
    deleteSpread(currentSpreadIndex.value);
  }
}

// Handle delete book
async function handleDeleteBook() {
  const confirmed = await showModal({
    title: 'Delete Book',
    message: 'Are you sure you want to delete the entire book? This action cannot be undone.',
    isDanger: true
  });

  if (confirmed) {
    deleteBook();
    createNewBook();
  }
}

// Initialize app
async function init() {
  // Check if we have an example in the URL query parameter
  const exampleData = route.query.example as string | undefined;

  if (exampleData) {
    // Load example data from URL without saving to localStorage
    try {
      const decodedData = decodeURIComponent(atob(exampleData));
      const exampleBook = JSON.parse(decodedData);
      book.value = exampleBook;
      isViewingExample.value = true;
      // Don't save to localStorage - this is just a temporary example
      // Show loading screen briefly
      await new Promise(resolve => setTimeout(resolve, 500));
      isLoading.value = false;
      return;
    } catch (error) {
      logger.error('Failed to load example data:', error);
      // Fall through to load saved book
    }
  }

  isViewingExample.value = false;

  // Load saved book
  const savedBook = loadBook();
  if (savedBook) {
    book.value = savedBook;
  } else {
    // Generate filename for new book
    book.value.filename = generateFilename();
  }

  // Wait a bit to show loading screen
  await new Promise(resolve => setTimeout(resolve, 500));

  // Hide loading screen
  isLoading.value = false;

  // Render current spread if in view mode
  if (isViewMode.value) {
    await nextTick();
    // The BookPage components will handle rendering
  }
}

// Handle toggle view - change route instead of just toggling state
function handleToggleView() {
  if (isViewMode.value) {
    // Currently in view mode, switch to edit mode
    router.push('/edit');
  } else {
    // Currently in edit mode, switch to view mode
    router.push('/view');
  }
}

// Apply view mode based on route
function applyRouteViewMode() {
  const defaultViewMode = route.meta.defaultViewMode as boolean | undefined;

  if (defaultViewMode !== undefined) {
    // Set view mode based on route meta using the composable
    setViewMode(defaultViewMode);
  } else {
    // For /edit route, check localStorage
    const saved = localStorage.getItem('openbook_viewmode');
    if (saved) {
      setViewMode(saved === 'true');
    } else {
      // Default to edit mode if no saved preference
      setViewMode(false);
    }
  }
}

// Watch for route changes
watch(() => route.path, () => {
  applyRouteViewMode();
});

onMounted(() => {
  // Apply view mode based on route
  applyRouteViewMode();

  init();
});
</script>
