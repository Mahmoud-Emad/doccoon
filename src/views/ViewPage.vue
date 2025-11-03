<template>
  <div class="view-page-container">
    <!-- Header -->
    <div class="view-header">
      <button class="back-button" @click="goHome">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 4L6 10L12 16" stroke="currentColor" stroke-width="2" stroke-linecap="round"
            stroke-linejoin="round" />
        </svg>
        Back to Home
      </button>

      <div class="view-title">{{ book.filename || 'Untitled Book' }}</div>

      <button class="theme-toggle" @click="toggleTheme">
        <svg v-if="!isDarkTheme" width="20" height="20" viewBox="0 0 20 20" fill="none"
          xmlns="http://www.w3.org/2000/svg">
          <circle cx="10" cy="10" r="4" fill="currentColor" />
          <path d="M10 2V4M10 16V18M18 10H16M4 10H2M15.5 4.5L14 6M6 14L4.5 15.5M15.5 15.5L14 14M6 6L4.5 4.5"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" />
        </svg>
        <svg v-else width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M17 10.5C16.1 13.5 13.4 15.5 10.5 15.5C6.9 15.5 4 12.6 4 9C4 6.1 6 3.4 9 2.5C5.9 3.4 3.5 6.4 3.5 10C3.5 14.1 6.9 17.5 11 17.5C14.6 17.5 17.6 15.1 18.5 12C18.2 11.2 17.7 10.8 17 10.5Z"
            fill="currentColor" />
        </svg>
      </button>
    </div>

    <!-- Page Content -->
    <div class="view-content">
      <div v-if="!pageExists" class="error-message">
        <h2>Page Not Found</h2>
        <p>The requested page does not exist in this book.</p>
        <button class="cta-button" @click="goToPage(1)">Go to First Page</button>
      </div>

      <div v-else class="page-viewer">
        <div class="page-display" ref="pageRef"></div>
      </div>
    </div>

    <!-- Navigation Footer -->
    <div class="view-footer">
      <button class="nav-button" :disabled="currentPage <= 1" @click="previousPage">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 4L6 10L12 16" stroke="currentColor" stroke-width="2" stroke-linecap="round"
            stroke-linejoin="round" />
        </svg>
        Previous
      </button>

      <div class="page-info">
        Page {{ currentPage }} of {{ totalPages }}
      </div>

      <button class="nav-button" :disabled="currentPage >= totalPages" @click="nextPage">
        Next
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M8 4L14 10L8 16" stroke="currentColor" stroke-width="2" stroke-linecap="round"
            stroke-linejoin="round" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useBook } from '@/composables/useBook';
import { useTheme } from '@/composables/useTheme';
import { useStorage } from '@/composables/useStorage';
import { useMarkdown } from '@/composables/useMarkdown';

const route = useRoute();
const router = useRouter();

// Initialize composables
const { book } = useBook();
const { isDarkTheme, toggleTheme } = useTheme();
const { loadBook } = useStorage(book);
const { renderMarkdown } = useMarkdown(isDarkTheme);

// Page reference
const pageRef = ref<HTMLElement>();

// Get current page from query parameter
const currentPage = computed(() => {
  const page = parseInt(route.query.page as string || '1');
  return isNaN(page) || page < 1 ? 1 : page;
});

// Calculate total pages (each spread has 2 pages)
const totalPages = computed(() => {
  return book.value.spreads.length * 2;
});

// Check if page exists
const pageExists = computed(() => {
  return currentPage.value <= totalPages.value;
});

// Get page content
const pageContent = computed(() => {
  if (!pageExists.value) return '';

  const spreadIndex = Math.floor((currentPage.value - 1) / 2);
  const isLeftPage = (currentPage.value - 1) % 2 === 0;

  const spread = book.value.spreads[spreadIndex];
  if (!spread) return '';

  return isLeftPage ? spread.left : spread.right;
});

// Navigation functions
function goHome() {
  router.push('/');
}

function goToPage(page: number) {
  router.push({ path: '/view', query: { page: page.toString() } });
}

function previousPage() {
  if (currentPage.value > 1) {
    goToPage(currentPage.value - 1);
  }
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    goToPage(currentPage.value + 1);
  }
}

// Render markdown when page changes
async function renderPage() {
  if (pageRef.value && pageExists.value) {
    await nextTick();
    await renderMarkdown(pageContent.value, pageRef.value);
  }
}

// Watch for page changes
watch([currentPage, pageContent], () => {
  renderPage();
});

// Initialize
onMounted(() => {
  // Load saved book
  const savedBook = loadBook();
  if (savedBook) {
    book.value = savedBook;
  }

  // Render initial page
  renderPage();
});
</script>

<style scoped>
.view-page-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-color);
  color: var(--text-color);
}

/* Header */
.view-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: #007ACC;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

.view-title {
  font-size: 18px;
  font-weight: 600;
}

.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-toggle:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Content */
.view-content {
  flex: 1;
  overflow-y: auto;
  padding: 40px 20px;
}

.error-message {
  max-width: 600px;
  margin: 100px auto;
  text-align: center;
}

.error-message h2 {
  font-size: 32px;
  margin: 0 0 16px;
  color: var(--text-color);
}

.error-message p {
  font-size: 18px;
  margin: 0 0 32px;
  color: var(--text-color);
  opacity: 0.7;
}

.page-viewer {
  max-width: 800px;
  margin: 0 auto;
}

.page-display {
  background: var(--page-bg);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 40px;
  min-height: 400px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-color);
}

/* Footer */
.view-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: #007ACC;
  color: #ffffff;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.2);
}

.nav-button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  font-weight: 500;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
  background: linear-gradient(135deg, #007ACC 0%, #005a9e 100%);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 122, 204, 0.3);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 122, 204, 0.4);
}
</style>
