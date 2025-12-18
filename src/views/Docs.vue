<template>
  <LoadingScreen :visible="isLoading" />

  <div class="container" :class="{ loaded: !isLoading }">
    <!-- Documentation Header -->
    <div class="docs-header">
      <button class="back-button" @click="goHome">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 4L6 10L12 16" stroke="currentColor" stroke-width="2" stroke-linecap="round"
            stroke-linejoin="round" />
        </svg>
        Back to Home
      </button>

      <div class="docs-title">📖 Open Book Documentation</div>

      <div class="header-controls">
        <button class="control-button" @click="handleToggleLayoutMode" :title="layoutMode === 'book' ? 'Switch to Page View' : 'Switch to Book View'">
          <svg v-if="layoutMode === 'book'" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="14" height="14" rx="1" stroke="currentColor" stroke-width="1.5" fill="none" />
          </svg>
          <svg v-else width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="2" y="3" width="6" height="14" rx="1" stroke="currentColor" stroke-width="1.5" fill="none" />
            <rect x="12" y="3" width="6" height="14" rx="1" stroke="currentColor" stroke-width="1.5" fill="none" />
          </svg>
        </button>

        <button class="control-button" @click="toggleTheme" title="Toggle theme">
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
    </div>

    <BookSpread :spread="displaySpread" :is-view-mode="true" :layout-mode="layoutMode" :is-diff-mode="false"
      :render-markdown="renderMarkdown" @toggle-layout="handleToggleLayoutMode" />

    <!-- Documentation Footer -->
    <div class="docs-footer">
      <button class="nav-button" :disabled="!canGoPrevious" @click="goToPrevious">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 4L6 10L12 16" stroke="currentColor" stroke-width="2" stroke-linecap="round"
            stroke-linejoin="round" />
        </svg>
        Previous
      </button>

      <div class="page-info">
        Spread {{ currentSpreadIndex + 1 }} of {{ totalSpreads }}
      </div>

      <button class="nav-button" :disabled="!canGoNext" @click="goToNext">
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
import { ref, computed, onMounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import LoadingScreen from '@/components/LoadingScreen.vue';
import BookSpread from '@/components/BookSpread.vue';

import { useTheme } from '@/composables/useTheme';
import { useLayoutMode } from '@/composables/useLayoutMode';
import { useMarkdown } from '@/composables/useMarkdown';
import type { Book } from '@/types';

const router = useRouter();

// Navigation function
function goHome() {
  router.push('/');
}

// Initialize composables
const { isDarkTheme, toggleTheme } = useTheme();
const { layoutMode, toggleLayoutMode } = useLayoutMode();
const { renderMarkdown } = useMarkdown(isDarkTheme);

// Loading state
const isLoading = ref(true);

// Current spread index for navigation
const currentSpreadIndex = ref(0);

// Documentation book structure
const docsBook = ref<Book>({
  filename: 'Open Book Documentation',
  spreads: []
});

// Computed values for navigation
const totalSpreads = computed(() => docsBook.value.spreads.length);
const canGoPrevious = computed(() => currentSpreadIndex.value > 0);
const canGoNext = computed(() => currentSpreadIndex.value < totalSpreads.value - 1);

// Current spread to display
const displaySpread = computed(() => {
  const spread = docsBook.value.spreads[currentSpreadIndex.value];
  if (!spread) {
    return {
      left: '',
      right: '',
      leftWidth: '1',
      rightWidth: '1'
    };
  }

  if (layoutMode.value === 'page') {
    // In page view mode, show only the left page
    return spread;
  }
  // In book view mode, show both pages normally
  return spread;
});

// Navigation functions
function goToPrevious() {
  if (canGoPrevious.value) {
    currentSpreadIndex.value--;
  }
}

function goToNext() {
  if (canGoNext.value) {
    currentSpreadIndex.value++;
  }
}

function handleToggleLayoutMode() {
  toggleLayoutMode();
}

// Initialize documentation content
function initializeDocumentation() {
  docsBook.value.spreads = [
    // Spread 1: Welcome & Introduction
    {
      left: `# Welcome to Open Book

Open Book is a modern, fully static markdown-based book editor with a beautiful two-page spread interface. Write, edit, and organize your content with powerful features—all running entirely in your browser.

## What is Open Book?

Open Book combines the elegance of traditional book reading with the power of modern markdown editing. It provides:

- **Book-like Interface**: Natural two-page spread layout
- **Rich Content**: Markdown, diagrams, math, and code
- **Fully Static**: No backend required, runs in browser
- **Auto-Save**: Never lose your work
- **Beautiful Themes**: Dark and light modes`,
      right: `## Why Open Book?

### Perfect for Writers
Whether you're writing a novel, documentation, or notes, Open Book provides a distraction-free environment with powerful formatting capabilities.

### Perfect for Developers
Document your code with syntax highlighting, create technical diagrams with Mermaid, and write mathematical formulas with LaTeX.

### Perfect for Educators
Create beautiful course materials, lecture notes, and educational content with rich formatting and visual elements.

### Perfect for Everyone
Simple enough for beginners, powerful enough for professionals.`,
      leftWidth: '1',
      rightWidth: '1'
    },
    // Spread 2: Key Features
    {
      left: `# Key Features

## 📝 Markdown Support

Open Book supports **GitHub Flavored Markdown** with all the features you expect:

- **Headers** (H1-H6)
- **Bold**, *italic*, and ~~strikethrough~~
- Lists (ordered and unordered)
- [Links](https://example.com)
- Images
- Tables
- Task lists
- Blockquotes
- Horizontal rules
- And more!`,
      right: `## 🎨 Rich Content

### Mermaid Diagrams
Create flowcharts, sequence diagrams, class diagrams, and more:

\`\`\`mermaid
graph LR
    A[Write] --> B[Preview]
    B --> C[Publish]
\`\`\`

### Math Expressions
Beautiful mathematical notation with KaTeX:

Inline: $E = mc^2$

Display:
$$
\\int_a^b f(x) dx = F(b) - F(a)
$$`,
      leftWidth: '1',
      rightWidth: '1'
    },
    // Spread 3: More Features
    {
      left: `## 💻 Syntax Highlighting

Code blocks with beautiful syntax highlighting for 100+ languages:

\`\`\`typescript
interface Book {
  title: string;
  author: string;
  pages: number;
}

function createBook(title: string): Book {
  return { title, author: '', pages: 0 };
}
\`\`\`

One-click copy buttons make it easy to share code snippets.`,
      right: `## 📖 Two-Page Spread

Experience the natural flow of reading and writing with our book-like interface:

- **Book View**: See two pages side-by-side
- **Page View**: Focus on one page at a time
- **Adjustable Width**: Resize pages to your preference
- **Smooth Navigation**: Arrow keys and buttons

## 🔄 Diff Checker

Compare left and right pages with visual diff highlighting:

- **Added Lines**: Green highlighting
- **Removed Lines**: Red highlighting
- **Unchanged**: Normal display`,
      leftWidth: '1',
      rightWidth: '1'
    },
    // Spread 4: Getting Started
    {
      left: `# Getting Started

## Creating Your First Book

1. Click **"Start Writing"** on the home page
2. You'll be taken to the editor in edit mode
3. Start typing in either the left or right page
4. Your work is automatically saved to browser storage

## Editor Modes

### Edit Mode
- Type directly in the text areas
- See line numbers on the left
- Drag and drop images
- Use markdown syntax`,
      right: `### View Mode
- See your rendered markdown
- Beautiful typography
- Rendered diagrams and math
- Syntax-highlighted code blocks

## Switching Modes

Click the **eye icon** in the toolbar to toggle between edit and view modes, or use the keyboard shortcut.

## Navigation

- **Next/Previous buttons**: Navigate between spreads
- **Arrow keys**: Quick navigation
- **Page counter**: Shows current position`,
      leftWidth: '1',
      rightWidth: '1'
    },
    // Spread 5: Using the Editor
    {
      left: `# Using the Editor

## Writing Markdown

Open Book uses standard markdown syntax. Here are some examples:

### Headers
\`\`\`markdown
# H1 Header
## H2 Header
### H3 Header
\`\`\`

### Text Formatting
\`\`\`markdown
**bold text**
*italic text*
~~strikethrough~~
\`\`\``,
      right: `### Lists
\`\`\`markdown
- Unordered item 1
- Unordered item 2

1. Ordered item 1
2. Ordered item 2
\`\`\`

### Task Lists
\`\`\`markdown
- [ ] Incomplete task
- [x] Completed task
\`\`\`

### Links and Images
\`\`\`markdown
[Link text](https://example.com)
![Alt text](image-url.jpg)
\`\`\``,
      leftWidth: '1',
      rightWidth: '1'
    },
    // Spread 6: Advanced Features
    {
      left: `# Advanced Features

## Creating Diagrams

### Flowcharts
\`\`\`mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
\`\`\`

### Sequence Diagrams
\`\`\`mermaid
sequenceDiagram
    Alice->>Bob: Hello Bob!
    Bob-->>Alice: Hi Alice!
\`\`\``,
      right: `### Class Diagrams
\`\`\`mermaid
classDiagram
    class Book {
        +String title
        +String author
        +publish()
    }
    class Chapter {
        +String name
        +int pages
    }
    Book "1" --> "*" Chapter
\`\`\`

Visit [Mermaid documentation](https://mermaid.js.org/) for more diagram types and syntax.`,
      leftWidth: '1',
      rightWidth: '1'
    },
    // Spread 7: Math & Tables
    {
      left: `## Writing Math

### Inline Math
Use single dollar signs for inline math:
\`$E = mc^2$\` renders as: $E = mc^2$

### Display Math
Use double dollar signs for display equations:

\`\`\`
$$
f(x) = \\int_{-\\infty}^{\\infty} e^{-x^2} dx
$$
\`\`\`

Renders as:
$$
f(x) = \\int_{-\\infty}^{\\infty} e^{-x^2} dx
$$`,
      right: `## Creating Tables

Use pipes and dashes to create tables:

\`\`\`markdown
| Feature | Supported |
|---------|-----------|
| Markdown | ✓ |
| Diagrams | ✓ |
| Math | ✓ |
| Code | ✓ |
\`\`\`

Renders as:

| Feature | Supported |
|---------|-----------|
| Markdown | ✓ |
| Diagrams | ✓ |
| Math | ✓ |
| Code | ✓ |`,
      leftWidth: '1',
      rightWidth: '1'
    },
    // Spread 8: Technical Architecture
    {
      left: `# Technical Architecture

## Technology Stack

### Frontend Framework
- **Vue 3**: Modern reactive framework
- **TypeScript**: Type-safe development
- **Vite**: Fast build tooling

### Markdown Processing
- **Marked.js**: Markdown parsing
- **KaTeX**: Math rendering
- **Mermaid**: Diagram generation
- **Highlight.js**: Syntax highlighting`,
      right: `## Architecture Principles

### Fully Static
- No backend server required
- Runs entirely in browser
- Deploy anywhere (GitHub Pages, Netlify, etc.)

### Local Storage
- Auto-save to browser storage
- No data sent to servers
- Privacy-focused design

### Component-Based
- Modular Vue components
- Reusable composables
- Clean separation of concerns`,
      leftWidth: '1',
      rightWidth: '1'
    },
    // Spread 9: Setup & Installation
    {
      left: `# Setup & Installation

## Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Modern web browser
- Git (for cloning)

## Installation Steps

1. **Clone the repository**
\`\`\`bash
git clone https://github.com/Mahmoud-Emad/openbook.git
cd openbook
\`\`\`

2. **Install dependencies**
\`\`\`bash
npm install
\`\`\``,
      right: `3. **Run development server**
\`\`\`bash
npm run dev
\`\`\`

4. **Build for production**
\`\`\`bash
npm run build
\`\`\`

5. **Preview production build**
\`\`\`bash
npm run preview
\`\`\`

## Docker Deployment

\`\`\`bash
docker build -t openbook .
docker run -p 80:80 openbook
\`\`\``,
      leftWidth: '1',
      rightWidth: '1'
    },
    // Spread 10: Themes & Customization
    {
      left: `# Themes & Customization

## Available Themes

### Light Theme
- Clean, bright interface
- Easy on the eyes in daylight
- Professional appearance
- High contrast for readability

### Dark Theme
- Reduced eye strain in low light
- Modern aesthetic
- OLED-friendly
- Syntax highlighting optimized`,
      right: `## Switching Themes

Click the **sun/moon icon** in the navigation bar to toggle between light and dark themes.

Your theme preference is saved automatically and persists across sessions.

## Customization Options

### Page Width
Drag the bookmark separator between pages to adjust the width ratio of left and right pages.

### Layout Modes
- **Book View**: Two-page spread
- **Page View**: Single page focus`,
      leftWidth: '1',
      rightWidth: '1'
    },
    // Spread 11: Tips & Tricks
    {
      left: `# Tips & Tricks

## Productivity Tips

### Keyboard Shortcuts
- Use arrow keys to navigate between spreads
- Tab for indentation in lists
- Shift+Enter for line breaks

### Drag & Drop
- Drag images directly into the editor
- Drop files to insert them
- Works in edit mode

### Auto-Save
Your work is automatically saved every few seconds. No need to manually save!`,
      right: `## Best Practices

### Organize Content
- Use one spread per topic
- Keep related content on facing pages
- Use headers for structure

### Use Rich Features
- Add diagrams for visual explanation
- Include code examples with syntax highlighting
- Use math for formulas and equations

### Preview Often
Toggle to view mode frequently to see how your content looks rendered.`,
      leftWidth: '1',
      rightWidth: '1'
    },
    // Spread 12: FAQ & Support
    {
      left: `# FAQ & Support

## Frequently Asked Questions

### Where is my data stored?
All data is stored locally in your browser's localStorage. Nothing is sent to any server.

### Can I export my books?
Currently, books are stored in browser storage. You can copy the content manually.

### Does it work offline?
Yes! Once loaded, Open Book works completely offline.`,
      right: `### Can I use custom fonts?
The app uses system fonts for optimal performance and compatibility.

### Is my data private?
Absolutely! All data stays in your browser. We don't collect or transmit any information.

## Getting Help

- Check this documentation
- Visit the GitHub repository
- Report issues on GitHub
- Contribute to the project

**Happy writing! 📖✨**`,
      leftWidth: '1',
      rightWidth: '1'
    }
  ];
}

// Initialize on mount
onMounted(async () => {
  initializeDocumentation();

  // Wait a bit to show loading screen
  await new Promise(resolve => setTimeout(resolve, 500));

  // Hide loading screen
  isLoading.value = false;

  // Render current spread
  await nextTick();
});
</script>

<style scoped>
.container {
  opacity: 0;
  transition: opacity 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-color);
}

.container.loaded {
  opacity: 1;
}

/* Documentation Header */
.docs-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: var(--bg-color);
  border-bottom: 1px solid var(--border-color);
  min-height: 60px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-color);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-button:hover {
  background: var(--page-bg);
  border-color: #007ACC;
  color: #007ACC;
}

.docs-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  flex: 1;
  text-align: center;
}

.header-controls {
  display: flex;
  gap: 8px;
}

.control-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-color);
  cursor: pointer;
  transition: all 0.2s ease;
}

.control-button:hover {
  background: var(--page-bg);
  border-color: #007ACC;
  color: #007ACC;
}

/* Documentation Footer */
.docs-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: var(--bg-color);
  border-top: 1px solid var(--border-color);
  min-height: 70px;
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-color);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-button:hover:not(:disabled) {
  background: var(--page-bg);
  border-color: #007ACC;
  color: #007ACC;
}

.nav-button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
  opacity: 0.7;
}
</style>

