<template>
    <LoadingScreen :visible="isLoading" />

    <div
        class="flex flex-col h-screen bg-[var(--bg-color)] transition-opacity duration-300"
        :class="{ 'opacity-0': isLoading, 'opacity-100': !isLoading }"
    >
        <!-- Documentation Header -->
        <div
            class="flex items-center justify-between px-6 py-3 bg-[var(--bg-color)] border-b border-[var(--border-color)] min-h-[60px]"
        >
            <BaseButton variant="secondary" size="sm" @click="goHome">
                <BaseIcon name="chevron-left" :size="20" />
                Back to Home
            </BaseButton>

            <div
                class="text-lg font-semibold text-[var(--text-color)] flex-1 text-center"
            >
                Doccoon Documentation
            </div>

            <div class="flex gap-2">
                <BaseButton
                    variant="secondary"
                    size="sm"
                    icon
                    :title="
                        layoutMode === 'book'
                            ? 'Switch to Page View'
                            : 'Switch to Book View'
                    "
                    @click="handleToggleLayoutMode"
                >
                    <BaseIcon
                        :name="
                            layoutMode === 'book' ? 'layout-single' : 'layout'
                        "
                        :size="20"
                    />
                </BaseButton>
            </div>
        </div>

        <BookSpread
            :spread="displaySpread"
            :is-view-mode="true"
            :layout-mode="layoutMode"
            :is-diff-mode="false"
            :render-markdown="renderMarkdown"
            @toggle-layout="handleToggleLayoutMode"
        />

        <!-- Documentation Footer -->
        <div
            class="flex items-center justify-between px-6 py-4 bg-[var(--bg-color)] border-t border-[var(--border-color)] min-h-[70px]"
        >
            <BaseButton
                variant="secondary"
                size="md"
                :disabled="!canGoPrevious"
                @click="goToPrevious"
            >
                <BaseIcon name="chevron-left" :size="20" />
                Previous
            </BaseButton>

            <div
                class="text-sm font-medium text-[var(--text-color)] opacity-70"
            >
                {{ navigationLabel }}
            </div>

            <BaseButton
                variant="secondary"
                size="md"
                :disabled="!canGoNext"
                @click="goToNext"
            >
                Next
                <BaseIcon name="chevron-right" :size="20" />
            </BaseButton>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from "vue";
import { useRouter } from "vue-router";
import LoadingScreen from "@/components/LoadingScreen.vue";
import BookSpread from "@/components/BookSpread.vue";
import BaseButton from "@/components/ui/BaseButton.vue";
import BaseIcon from "@/components/ui/BaseIcon.vue";

import { useTheme } from "@/composables/useTheme";
import { useLayoutMode } from "@/composables/useLayoutMode";
import { useMarkdown } from "@/composables/useMarkdown";
import type { Book } from "@/types";

const router = useRouter();

// Navigation function
function goHome() {
    router.push("/");
}

// Initialize composables
const { isDarkTheme } = useTheme();
const { layoutMode, toggleLayoutMode } = useLayoutMode();
const { renderMarkdown } = useMarkdown(isDarkTheme);

// Loading state
const isLoading = ref(true);

// Navigation indices for both modes
const currentSpreadIndex = ref(0);
const currentPageIndex = ref(0);

// Documentation book structure
const docsBook = ref<Book>({
    filename: "Doccoon Documentation",
    spreads: [],
});

// Build pages array from spreads for page view mode
const pages = computed(() => {
    const result: string[] = [];
    for (const spread of docsBook.value.spreads) {
        if (spread.left) result.push(spread.left);
        if (spread.right) result.push(spread.right);
    }
    return result;
});

// Navigation adapts to layout mode
const totalItems = computed(() =>
    layoutMode.value === "book"
        ? docsBook.value.spreads.length
        : pages.value.length,
);

const currentIndex = computed(() =>
    layoutMode.value === "book"
        ? currentSpreadIndex.value
        : currentPageIndex.value,
);

const canGoPrevious = computed(() => currentIndex.value > 0);
const canGoNext = computed(() => currentIndex.value < totalItems.value - 1);

// Current spread to display
const displaySpread = computed(() => {
    if (layoutMode.value === "book") {
        const spread = docsBook.value.spreads[currentSpreadIndex.value];
        if (!spread) {
            return { left: "", right: "", leftWidth: "1", rightWidth: "1" };
        }
        return spread;
    }

    // Page view: show single page in a spread
    const pageContent = pages.value[currentPageIndex.value] ?? "";
    return {
        left: pageContent,
        right: "",
        leftWidth: "1",
        rightWidth: "1",
    };
});

// Navigation label adapts to layout mode
const navigationLabel = computed(() => {
    if (layoutMode.value === "book") {
        return `Spread ${currentSpreadIndex.value + 1} of ${docsBook.value.spreads.length}`;
    }
    return `Page ${currentPageIndex.value + 1} of ${pages.value.length}`;
});

// Navigation functions
function goToPrevious() {
    if (!canGoPrevious.value) return;
    if (layoutMode.value === "book") {
        currentSpreadIndex.value--;
    } else {
        currentPageIndex.value--;
    }
}

function goToNext() {
    if (!canGoNext.value) return;
    if (layoutMode.value === "book") {
        currentSpreadIndex.value++;
    } else {
        currentPageIndex.value++;
    }
}

function handleToggleLayoutMode() {
    toggleLayoutMode();
}

// Sync indices when switching layout modes
watch(layoutMode, (newMode, oldMode) => {
    if (newMode === "page" && oldMode === "book") {
        // Switching to page view: jump to the first page of the current spread
        currentPageIndex.value = currentSpreadIndex.value * 2;
    } else if (newMode === "book" && oldMode === "page") {
        // Switching to book view: jump to the spread containing the current page
        currentSpreadIndex.value = Math.floor(currentPageIndex.value / 2);
    }
});

// Initialize documentation content
function initializeDocumentation() {
    docsBook.value.spreads = [
        // Spread 1: Welcome & Introduction
        {
            left: `# Welcome to Doccoon

Doccoon is a modern markdown-based book editor with a beautiful two-page spread interface. Write, edit, and organize your content with powerful features — synced to the cloud and enhanced with AI.

## What is Doccoon?

Doccoon combines the elegance of traditional book reading with the power of modern markdown editing. It provides:

- **Book-like Interface**: Natural two-page spread layout
- **Rich Content**: Markdown, diagrams, math, and code
- **Cloud Sync**: Auto-save with configurable intervals
- **AI Refinement**: OpenAI and Gemini integration
- **Sharing**: Versioned page snapshots with social sharing
- **Accounts**: Sign in with Google, GitHub, or email
- **Beautiful Themes**: Dark and light modes`,
            right: `## Why Doccoon?

### Perfect for Writers
Whether you're writing a novel, documentation, or notes, Doccoon provides a distraction-free environment with powerful formatting and AI-assisted refinement.

### Perfect for Developers
Document your code with syntax highlighting for 100+ languages, create technical diagrams with Mermaid, and write mathematical formulas with KaTeX.

### Perfect for Educators
Create beautiful course materials, lecture notes, and educational content with rich formatting and visual elements. Share pages with students via secure links.

### Perfect for Teams
Share versioned snapshots of your pages via WhatsApp, Facebook, Telegram, or direct links. Recipients see exactly what you shared, even if you keep editing.`,
            leftWidth: "1",
            rightWidth: "1",
        },
        // Spread 2: Key Features
        {
            left: `# Key Features

## Markdown Support

Doccoon supports **GitHub Flavored Markdown** with all the features you expect:

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
            right: `## Rich Content

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
            leftWidth: "1",
            rightWidth: "1",
        },
        // Spread 3: More Features
        {
            left: `## Syntax Highlighting

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
            right: `## Two-Page Spread

Experience the natural flow of reading and writing with our book-like interface:

- **Book View**: See two pages side-by-side
- **Page View**: Focus on one page at a time
- **Adjustable Width**: Resize pages to your preference
- **Smooth Navigation**: Arrow keys and buttons

## Diff Checker

Compare left and right pages with visual diff highlighting:

- **Added Lines**: Green highlighting
- **Removed Lines**: Red highlighting
- **Unchanged**: Normal display`,
            leftWidth: "1",
            rightWidth: "1",
        },
        // Spread 4: Getting Started
        {
            left: `# Getting Started

## Sign In

1. Click **Sign in** or **Sign up** in the navigation bar
2. Choose Google, GitHub, or email/password
3. Your books, settings, and AI keys are tied to your account

## Creating Your First Book

1. Click **"Start Writing"** on the home page or go to \`/edit\`
2. If you have no books, you'll be prompted to create one
3. Start typing in either the left or right page
4. Your work auto-saves to the cloud (configurable interval)

You can also create books from your **Profile** page.`,
            right: `## Editor Toolbar

Each page has action buttons at the top:

- **Copy Content** — copy page text to clipboard
- **Insert Image** — upload and embed images inline
- **Clear Content** — clear the page
- **Page View / Book View** — toggle layout mode
- **AI** — refine or rewrite content with AI
- **Share** — generate a shareable link

## Editor Modes

### Edit Mode
- Type directly with line numbers
- Drag and drop images
- Full markdown syntax

### View Mode
- Rendered markdown with diagrams, math, and code
- Beautiful typography`,
            leftWidth: "1",
            rightWidth: "1",
        },
        // Spread 5: Using the Editor
        {
            left: `# Using the Editor

## Writing Markdown

Doccoon uses standard markdown syntax. Here are some examples:

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
            leftWidth: "1",
            rightWidth: "1",
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
            leftWidth: "1",
            rightWidth: "1",
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
            leftWidth: "1",
            rightWidth: "1",
        },
        // Spread 8: Themes & Customization
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

Click the **sun/moon icon** in the navigation bar to toggle between light and dark themes. Your preference persists across sessions.

## Settings & Preferences

Access settings from your profile dropdown. Available options:

### Preferences Tab
- **Auto-save interval**: Configure from 2 to 120 seconds
- Theme and layout preferences

### AI Configuration Tab
- **Add API keys**: Enter your OpenAI or Gemini API key
- **Select model**: Choose a model per key (e.g. GPT-4o, Gemini 2.5 Flash)
- **Manage keys**: View, update, or remove saved keys

### Page Width
Drag the bookmark separator between pages to adjust the width ratio of left and right pages.`,
            leftWidth: "1",
            rightWidth: "1",
        },
        // Spread 9: AI Features
        {
            left: `# AI Features

## Setup

1. Go to **Settings** > **AI Configuration**
2. Click **Add Key** and choose a provider (OpenAI or Gemini)
3. Paste your API key and select a model
4. Save — your key is stored securely on the server

## Using AI in the Editor

Click the **AI** button on any page to see options:

- **Refine** — improve grammar, tone, and clarity
- **Rewrite** — regenerate the content entirely

The AI output streams in with a typewriter effect. The textarea is disabled during processing.

## Supported Models

**OpenAI**: GPT-4o Mini, GPT-4o, GPT-4.1 Nano/Mini/Full

**Gemini**: Gemini 2.0 Flash, Gemini 2.5 Flash, Gemini 2.5 Pro`,
            right: `# Getting API Keys

To use AI features, you need an API key from OpenAI or Google. Here's how to get one:

## Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated key (starts with AIza...)
5. In Doccoon, go to **Settings** > **AI Configuration**
6. Click **Add Key**, select **Gemini**, paste your key
7. Choose a model (e.g., Gemini 2.5 Flash)

**Note**: Gemini offers a free tier with generous limits.`,
            leftWidth: "1",
            rightWidth: "1",
        },
        // Spread 10: OpenAI API Key & Troubleshooting
        {
            left: `## OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an OpenAI account
3. Click **"Create new secret key"**
4. Give it a name (e.g., "Doccoon")
5. Copy the key (starts with sk-...)
6. In Doccoon, go to **Settings** > **AI Configuration**
7. Click **Add Key**, select **OpenAI**, paste your key
8. Choose a model (e.g., GPT-4o)

**Note**: OpenAI requires a paid account with credits. New accounts may receive free trial credits.

## API Key Security

- Your API keys are stored securely on our servers
- Keys are never exposed in the browser
- You can remove keys anytime from Settings
- We recommend using dedicated keys for Doccoon`,
            right: `## Troubleshooting

### "API rate limit or quota exceeded"
- Your API key has exceeded its usage limits
- Check your usage at the provider's dashboard
- Wait for limits to reset or upgrade your plan

### "Invalid API key"
- Double-check that you copied the full key
- Ensure you selected the correct provider
- Try generating a new key

### "AI service unavailable"
- The AI provider may be experiencing issues
- Try again in a few minutes
- Check the provider's status page

## Tips

- Start with Gemini's free tier to try AI features
- Monitor your API usage to avoid unexpected charges
- Use GPT-4o Mini or Gemini Flash for faster, cheaper responses
- Use GPT-4o or Gemini Pro for higher quality output`,
            leftWidth: "1",
            rightWidth: "1",
        },
        // Spread 11: Sharing
        {
            left: `# Sharing

## Sharing a Page

1. Click the **Share** button on any page
2. A shareable link is generated with a **content snapshot**
3. Share via WhatsApp, Facebook, Telegram, or copy the link

## Content Versioning

When you share a page, the current content is captured as a snapshot. The recipient sees that exact version — even if you continue editing the original page.

Re-sharing the same page updates the snapshot to the latest content.

## Managing Shares

- **Revoke**: Delete the share to deactivate the link
- **Re-share**: Share again to update the snapshot
- Shared pages are view-only with rendered markdown

## Tips

- Save your page before sharing (content must be on the server)
- Sign in is required to share
- Empty pages cannot be shared`,
            right: `## Share Link Format

Shared pages are accessible at URLs like:

**your-domain.com/shared/abc123**

Recipients can view the content without signing in.

## Social Sharing

Click any social button to share directly:

- **WhatsApp**: Opens WhatsApp with pre-filled message
- **Facebook**: Opens Facebook share dialog
- **Telegram**: Opens Telegram share dialog
- **Copy Link**: Copies URL to clipboard

## Privacy

- Only the page content is shared, not your entire book
- You control when to revoke access
- Share links do not expire unless revoked`,
            leftWidth: "1",
            rightWidth: "1",
        },
        // Spread 12: FAQ & Support
        {
            left: `# FAQ & Support

## Frequently Asked Questions

### Where is my data stored?
When signed in, your books and pages are stored securely on our servers and synced automatically. Your AI provider keys are also stored server-side.

### Can I export my books?
You can copy page content from the editor and share pages via public links. Full export features are planned for a future release.

### Does it work offline?
The editor loads offline for viewing cached content, but saving, AI features, and sharing require an internet connection.

### Is my data private?
Yes. Only you can access your books unless you explicitly share them. We do not track usage or collect telemetry.`,
            right: `### Can I use my own AI provider?
Yes. Add your OpenAI or Google Gemini API key in Settings > AI Configuration. Choose your preferred model per key.

### What happens when I share a page?
A snapshot of the page content is captured at share time. The recipient sees that version. If you edit the page later, the shared link still shows the original snapshot until you re-share.

### Can I use custom fonts?
The app uses system fonts for optimal performance and compatibility.

## Getting Help

- Check this documentation
- Contact support at support@doccoon.com
- Visit our Help Center for more resources

**Happy writing!**`,
            leftWidth: "1",
            rightWidth: "1",
        },
    ];
}

// Initialize on mount
onMounted(async () => {
    initializeDocumentation();

    // Wait a bit to show loading screen
    await new Promise((resolve) => setTimeout(resolve, 500));

    // Hide loading screen
    isLoading.value = false;

    // Render current spread
    await nextTick();
});
</script>
