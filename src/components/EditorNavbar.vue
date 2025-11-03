<template>
  <nav class="editor-navbar">
    <div class="navbar-left">
      <!-- Home Link -->
      <router-link to="/" class="navbar-item navbar-home" title="Go to Home">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
        <span>Home</span>
      </router-link>

      <!-- File Menu -->
      <div class="navbar-item navbar-dropdown" @click="toggleDropdown('file')"
        :class="{ active: activeDropdown === 'file' }">
        <span>File</span>
        <div v-if="activeDropdown === 'file'" class="dropdown-menu" @click.stop>
          <button class="dropdown-item" @click="handleNew">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
            New Book
          </button>
          <button class="dropdown-item" @click="handleDeleteBook">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
            Delete Book
          </button>
        </div>
      </div>

      <!-- Edit Menu -->
      <div class="navbar-item navbar-dropdown" @click="toggleDropdown('edit')"
        :class="{ active: activeDropdown === 'edit' }">
        <span>Edit</span>
        <div v-if="activeDropdown === 'edit'" class="dropdown-menu" @click.stop>
          <button class="dropdown-item" @click="handleAddPage">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            Add Page Spread
          </button>
          <button class="dropdown-item" @click="handleDeletePage">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
            Delete Page Spread
          </button>
        </div>
      </div>

      <!-- View Menu -->
      <div class="navbar-item navbar-dropdown" @click="toggleDropdown('view')"
        :class="{ active: activeDropdown === 'view' }">
        <span>View</span>
        <div v-if="activeDropdown === 'view'" class="dropdown-menu" @click.stop>
          <button class="dropdown-item" @click="handleToggleView">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
            {{ isViewMode ? 'Edit Mode' : 'View Mode' }}
          </button>
          <button class="dropdown-item" @click="handleToggleLayout">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="12" y1="3" x2="12" y2="21"></line>
            </svg>
            {{ layoutMode === 'book' ? 'Page View' : 'Book View' }}
          </button>
          <button v-if="isViewMode && layoutMode === 'book'" class="dropdown-item" @click="handleToggleDiff">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M16 3h5v5M4 20L21 3M21 16v5h-5M15 15l6 6M4 4l5 5"></path>
            </svg>
            {{ isDiffMode ? 'Hide Diff' : 'Show Diff' }}
          </button>
          <div class="dropdown-divider"></div>
          <button class="dropdown-item" @click="handleToggleTheme">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
            {{ isDarkTheme ? 'Light Theme' : 'Dark Theme' }}
          </button>
        </div>
      </div>
    </div>

    <div class="navbar-right">
      <!-- Filename Display -->
      <div class="navbar-filename">
        {{ filename }}
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps<{
  filename: string;
  isViewMode: boolean;
  isDarkTheme: boolean;
  layoutMode: 'book' | 'page';
  isDiffMode?: boolean;
}>();

const emit = defineEmits<{
  'new': [];
  'delete-book': [];
  'add-page': [];
  'delete-page': [];
  'toggle-view': [];
  'toggle-layout': [];
  'toggle-theme': [];
  'toggle-diff': [];
}>();

const activeDropdown = ref<string | null>(null);

function toggleDropdown(menu: string) {
  if (activeDropdown.value === menu) {
    activeDropdown.value = null;
  } else {
    activeDropdown.value = menu;
  }
}

function closeDropdown() {
  activeDropdown.value = null;
}

function handleNew() {
  emit('new');
  closeDropdown();
}

function handleDeleteBook() {
  emit('delete-book');
  closeDropdown();
}

function handleAddPage() {
  emit('add-page');
  closeDropdown();
}

function handleDeletePage() {
  emit('delete-page');
  closeDropdown();
}

function handleToggleView() {
  emit('toggle-view');
  closeDropdown();
}

function handleToggleLayout() {
  emit('toggle-layout');
  closeDropdown();
}

function handleToggleDiff() {
  emit('toggle-diff');
  closeDropdown();
}

function handleToggleTheme() {
  emit('toggle-theme');
  closeDropdown();
}

// Close dropdown when clicking outside
function handleClickOutside(e: MouseEvent) {
  const target = e.target as HTMLElement;
  if (!target.closest('.navbar-dropdown')) {
    closeDropdown();
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.editor-navbar {
  height: 35px;
  background: var(--page-bg);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12px;
  font-size: 13px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
  position: relative;
  z-index: 100;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 4px;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.navbar-item {
  padding: 4px 8px;
  cursor: pointer;
  color: var(--text-color);
  transition: background 0.15s ease;
  border-radius: 3px;
  display: flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  user-select: none;
  position: relative;
}

.navbar-item:hover {
  background: var(--border-color);
}

.navbar-item.active {
  background: var(--border-color);
}

.navbar-home {
  font-weight: 500;
}

.navbar-home svg {
  display: block;
}

.navbar-dropdown {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 2px;
  background: var(--page-bg);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  padding: 4px;
  z-index: 1000;
}

.dropdown-item {
  width: 100%;
  padding: 6px 8px;
  background: transparent;
  border: none;
  color: var(--text-color);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  border-radius: 3px;
  transition: background 0.15s ease;
  text-align: left;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
}

.dropdown-item:hover {
  background: var(--border-color);
}

.dropdown-item svg {
  display: block;
  flex-shrink: 0;
}

.dropdown-divider {
  height: 1px;
  background: var(--border-color);
  margin: 4px 0;
}

.navbar-filename {
  color: var(--text-color);
  opacity: 0.7;
  font-size: 12px;
  font-style: italic;
}

/* Dark theme adjustments */
body.dark-theme .dropdown-menu {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}
</style>
