<template>
  <div class="home">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-left">
          <router-link to="/" class="navbar-logo">
            Open Book
          </router-link>

          <div class="navbar-links">
            <router-link to="/edit" class="navbar-link">Editor</router-link>
            <router-link to="/view" class="navbar-link">View</router-link>
          </div>
        </div>

        <div class="navbar-right">
          <button class="theme-toggle-btn" @click="toggleTheme" title="Toggle theme">
            <svg v-if="!isDarkTheme" width="20" height="20" viewBox="0 0 20 20" fill="none"
              xmlns="http://www.w3.org/2000/svg">
              <circle cx="10" cy="10" r="4" fill="currentColor" />
              <path d="M10 2V4M10 16V18M18 10H16M4 10H2M15.5 4.5L14 6M6 14L4.5 15.5M15.5 15.5L14 14M6 6L4.5 4.5"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            </svg>
            <svg v-else width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"
              style="transform: rotate(-25deg);">
              <path
                d="M17 10.5C16.1 13.5 13.4 15.5 10.5 15.5C6.9 15.5 4 12.6 4 9C4 6.1 6 3.4 9 2.5C5.9 3.4 3.5 6.4 3.5 10C3.5 14.1 6.9 17.5 11 17.5C14.6 17.5 17.6 15.1 18.5 12C18.2 11.2 17.7 10.8 17 10.5Z"
                fill="currentColor" />
            </svg>
          </button>

          <!-- <a href="#" class="navbar-link">Sign In</a> -->
          <!-- <a href="#" class="navbar-signup-btn">Sign Up</a> -->
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="hero">
      <div class="hero-content">
        <h1 class="hero-title">Open Book</h1>
        <p class="hero-subtitle">A Modern Markdown-Based Book Editor</p>

        <p class="hero-description">
          Write, edit, and organize your content with a beautiful two-page spread interface.
          Perfect for books, documentation, notes, and creative writing.
        </p>

        <button class="cta-button" @click="startWriting">
          Start Writing
        </button>
      </div>
    </div>

    <!-- Mermaid Examples Section -->
    <div class="mermaid-section">
      <div class="mermaid-content">
        <h2 class="section-title">Powerful Diagram Support</h2>
        <p class="section-description">
          Create beautiful diagrams directly in your markdown using Mermaid syntax.
          Perfect for flowcharts, class diagrams, entity relationships, and more.
        </p>

        <div class="mermaid-examples">
          <div class="mermaid-example" data-index="0">
            <div class="mermaid-header">
              <h3>Flowchart</h3>
              <div class="mermaid-actions">
                <button class="action-btn copy-btn" @click="copyMermaidCode(0)" title="Copy code">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="5" y="5" width="9" height="9" rx="1" stroke="currentColor" stroke-width="1.5"
                      fill="none" />
                    <path d="M3 11V3C3 2.4 3.4 2 4 2H10" stroke="currentColor" stroke-width="1.5" fill="none" />
                  </svg>
                  <span v-if="copiedIndex === 0" class="copy-tooltip">Copied!</span>
                </button>
                <button class="action-btn try-btn" @click="tryMermaidCode(0)" title="Try it">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 3L11 8L5 13V3Z" fill="currentColor" />
                  </svg>
                </button>
              </div>
            </div>
            <div class="mermaid-preview">
              <pre class="mermaid-code">graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E</pre>
            </div>
          </div>

          <div class="mermaid-example" data-index="1">
            <div class="mermaid-header">
              <h3>Class Diagram</h3>
              <div class="mermaid-actions">
                <button class="action-btn copy-btn" @click="copyMermaidCode(1)" title="Copy code">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="5" y="5" width="9" height="9" rx="1" stroke="currentColor" stroke-width="1.5"
                      fill="none" />
                    <path d="M3 11V3C3 2.4 3.4 2 4 2H10" stroke="currentColor" stroke-width="1.5" fill="none" />
                  </svg>
                  <span v-if="copiedIndex === 1" class="copy-tooltip">Copied!</span>
                </button>
                <button class="action-btn try-btn" @click="tryMermaidCode(1)" title="Try it">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 3L11 8L5 13V3Z" fill="currentColor" />
                  </svg>
                </button>
              </div>
            </div>
            <div class="mermaid-preview">
              <pre class="mermaid-code">classDiagram
    class Book {
        +String title
        +String author
        +publish()
    }
    class Chapter {
        +String name
        +int pages
    }
    Book "1" --> "*" Chapter</pre>
            </div>
          </div>

          <div class="mermaid-example" data-index="2">
            <div class="mermaid-header">
              <h3>Entity Relationship</h3>
              <div class="mermaid-actions">
                <button class="action-btn copy-btn" @click="copyMermaidCode(2)" title="Copy code">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="5" y="5" width="9" height="9" rx="1" stroke="currentColor" stroke-width="1.5"
                      fill="none" />
                    <path d="M3 11V3C3 2.4 3.4 2 4 2H10" stroke="currentColor" stroke-width="1.5" fill="none" />
                  </svg>
                  <span v-if="copiedIndex === 2" class="copy-tooltip">Copied!</span>
                </button>
                <button class="action-btn try-btn" @click="tryMermaidCode(2)" title="Try it">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 3L11 8L5 13V3Z" fill="currentColor" />
                  </svg>
                </button>
              </div>
            </div>
            <div class="mermaid-preview">
              <pre class="mermaid-code">erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ITEM : contains
    USER {
        string name
        string email
    }</pre>
            </div>
          </div>
        </div>

        <div class="mermaid-footer">
          <a href="https://github.com/mermaid-js/mermaid" target="_blank" rel="noopener noreferrer"
            class="see-more-link">
            See more diagram types
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 3L11 8L6 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                stroke-linejoin="round" />
            </svg>
          </a>
        </div>
      </div>
    </div>

    <!-- Code Syntax Highlighting Section -->
    <div class="code-section">
      <div class="code-content">
        <h2 class="section-title">Beautiful Code Blocks</h2>
        <p class="section-description">
          Syntax highlighting for 100+ programming languages with automatic language detection.
          Write clean, readable code examples with beautiful color schemes.
        </p>

        <div class="code-examples">
          <div class="code-example" data-index="0">
            <div class="code-header">
              <h3>TypeScript</h3>
              <div class="code-actions">
                <button class="action-btn copy-btn" @click="copyCodeExample(0)" title="Copy code">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="5" y="5" width="9" height="9" rx="1" stroke="currentColor" stroke-width="1.5"
                      fill="none" />
                    <path d="M3 11V3C3 2.4 3.4 2 4 2H10" stroke="currentColor" stroke-width="1.5" fill="none" />
                  </svg>
                  <span v-if="copiedCodeIndex === 0" class="copy-tooltip">Copied!</span>
                </button>
                <button class="action-btn try-btn" @click="tryCodeExample(0)" title="Try it">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 3L11 8L5 13V3Z" fill="currentColor" />
                  </svg>
                </button>
              </div>
            </div>
            <div class="code-preview">
              <pre><code class="language-typescript" v-html="highlightedCode[0]"></code></pre>
            </div>
          </div>

          <div class="code-example" data-index="1">
            <div class="code-header">
              <h3>Python</h3>
              <div class="code-actions">
                <button class="action-btn copy-btn" @click="copyCodeExample(1)" title="Copy code">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="5" y="5" width="9" height="9" rx="1" stroke="currentColor" stroke-width="1.5"
                      fill="none" />
                    <path d="M3 11V3C3 2.4 3.4 2 4 2H10" stroke="currentColor" stroke-width="1.5" fill="none" />
                  </svg>
                  <span v-if="copiedCodeIndex === 1" class="copy-tooltip">Copied!</span>
                </button>
                <button class="action-btn try-btn" @click="tryCodeExample(1)" title="Try it">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 3L11 8L5 13V3Z" fill="currentColor" />
                  </svg>
                </button>
              </div>
            </div>
            <div class="code-preview">
              <pre><code class="language-python" v-html="highlightedCode[1]"></code></pre>
            </div>
          </div>
        </div>

        <div class="code-footer">
          <a href="https://highlightjs.org/static/demo/" target="_blank" rel="noopener noreferrer"
            class="see-more-link">
            See all supported languages
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 3L11 8L6 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                stroke-linejoin="round" />
            </svg>
          </a>
        </div>
      </div>
    </div>

    <!-- Mathematical Expressions Section -->
    <div class="math-section">
      <div class="math-content">
        <h2 class="section-title">Mathematical Expressions</h2>
        <p class="section-description">
          Write beautiful mathematical notation using LaTeX syntax.
          Support for inline math, display equations, matrices, and advanced mathematical symbols.
        </p>

        <div class="math-examples">
          <div class="math-example" data-index="0">
            <div class="math-header">
              <h3>Basic Equations</h3>
              <div class="math-actions">
                <button class="action-btn copy-btn" @click="copyMathCode(0)" title="Copy code">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="5" y="5" width="9" height="9" rx="1" stroke="currentColor" stroke-width="1.5"
                      fill="none" />
                    <path d="M3 11V3C3 2.4 3.4 2 4 2H10" stroke="currentColor" stroke-width="1.5" fill="none" />
                  </svg>
                  <span v-if="copiedMathIndex === 0" class="copy-tooltip">Copied!</span>
                </button>
                <button class="action-btn try-btn" @click="tryMathCode(0)" title="Try it">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 3L11 8L5 13V3Z" fill="currentColor" />
                  </svg>
                </button>
              </div>
            </div>
            <div class="math-preview">
              <pre class="math-code">Einstein's equation: $E = mc^2$

Pythagorean theorem:

$$
a^2 + b^2 = c^2
$$

The golden ratio: $\phi = \frac{1 + \sqrt{5}}{2}$</pre>
            </div>
          </div>

          <div class="math-example" data-index="1">
            <div class="math-header">
              <h3>Calculus</h3>
              <div class="math-actions">
                <button class="action-btn copy-btn" @click="copyMathCode(1)" title="Copy code">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="5" y="5" width="9" height="9" rx="1" stroke="currentColor" stroke-width="1.5"
                      fill="none" />
                    <path d="M3 11V3C3 2.4 3.4 2 4 2H10" stroke="currentColor" stroke-width="1.5" fill="none" />
                  </svg>
                  <span v-if="copiedMathIndex === 1" class="copy-tooltip">Copied!</span>
                </button>
                <button class="action-btn try-btn" @click="tryMathCode(1)" title="Try it">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 3L11 8L5 13V3Z" fill="currentColor" />
                  </svg>
                </button>
              </div>
            </div>
            <div class="math-preview">
              <pre class="math-code">Derivative definition:

$$
f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
$$

Fundamental theorem of calculus:

$$
\int_a^b f(x) dx = F(b) - F(a)
$$

Sum notation: $\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$</pre>
            </div>
          </div>

          <div class="math-example" data-index="2">
            <div class="math-header">
              <h3>Advanced Math</h3>
              <div class="math-actions">
                <button class="action-btn copy-btn" @click="copyMathCode(2)" title="Copy code">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="5" y="5" width="9" height="9" rx="1" stroke="currentColor" stroke-width="1.5"
                      fill="none" />
                    <path d="M3 11V3C3 2.4 3.4 2 4 2H10" stroke="currentColor" stroke-width="1.5" fill="none" />
                  </svg>
                  <span v-if="copiedMathIndex === 2" class="copy-tooltip">Copied!</span>
                </button>
                <button class="action-btn try-btn" @click="tryMathCode(2)" title="Try it">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 3L11 8L5 13V3Z" fill="currentColor" />
                  </svg>
                </button>
              </div>
            </div>
            <div class="math-preview">
              <pre class="math-code">Normal distribution:

$$
f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}
$$

Matrix:

$$
A = \begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
$$

Binomial theorem: $\binom{n}{k} = \frac{n!}{k!(n-k)!}$</pre>
            </div>
          </div>
        </div>

        <div class="math-footer">
          <a href="https://katex.org/docs/supported.html" target="_blank" rel="noopener noreferrer"
            class="see-more-link">
            See supported LaTeX functions
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 3L11 8L6 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                stroke-linejoin="round" />
            </svg>
          </a>
        </div>
      </div>
    </div>

    <!-- Diff Checker Section -->
    <div class="diff-section">
      <div class="diff-content">
        <h2 class="section-title">Side-by-Side Diff Checker</h2>
        <p class="section-description">
          Compare left and right pages in book view mode with visual diff highlighting.
          Perfect for tracking changes, comparing versions, or reviewing edits.
        </p>

        <div class="diff-example">
          <div class="diff-example-header">
            <h3>Compare Two Versions</h3>
            <p>See additions, deletions, and unchanged content at a glance</p>
          </div>

          <div class="diff-example-content">
            <div class="diff-pane">
              <div class="diff-pane-header">Left Page (Original)</div>
              <div class="diff-pane-body">
                <div class="diff-line diff-line-unchanged"><span class="diff-symbol">&nbsp;</span>- **Markdown Support**
                </div>
                <div class="diff-line diff-line-removed"><span class="diff-symbol">-</span>- **Mermaid Diagrams**</div>
                <div class="diff-line diff-line-unchanged"><span class="diff-symbol">&nbsp;</span>- **Math Expressions**
                </div>
                <div class="diff-line diff-line-unchanged"><span class="diff-symbol">&nbsp;</span>- **Syntax
                  Highlighting**</div>
                <div class="diff-line diff-line-unchanged"><span class="diff-symbol">&nbsp;</span>- **Dark & Light
                  Themes**</div>
                <div class="diff-line diff-line-placeholder"><span class="diff-symbol">&nbsp;</span>&nbsp;</div>
              </div>
            </div>

            <div class="diff-pane">
              <div class="diff-pane-header">Right Page (Modified)</div>
              <div class="diff-pane-body">
                <div class="diff-line diff-line-unchanged"><span class="diff-symbol">&nbsp;</span>- **Markdown Support**
                </div>
                <div class="diff-line diff-line-placeholder"><span class="diff-symbol">&nbsp;</span>&nbsp;</div>
                <div class="diff-line diff-line-unchanged"><span class="diff-symbol">&nbsp;</span>- **Math Expressions**
                </div>
                <div class="diff-line diff-line-unchanged"><span class="diff-symbol">&nbsp;</span>- **Syntax
                  Highlighting**</div>
                <div class="diff-line diff-line-unchanged"><span class="diff-symbol">&nbsp;</span>- **Dark & Light
                  Themes**</div>
                <div class="diff-line diff-line-added"><span class="diff-symbol">+</span>- **Diff Checker**</div>
              </div>
            </div>
          </div>

          <div class="diff-legend">
            <div class="diff-legend-item">
              <span class="diff-legend-box diff-legend-added"></span>
              <span>Added lines (green)</span>
            </div>
            <div class="diff-legend-item">
              <span class="diff-legend-box diff-legend-removed"></span>
              <span>Removed lines (red)</span>
            </div>
            <div class="diff-legend-item">
              <span class="diff-legend-box diff-legend-placeholder"></span>
              <span>Placeholder (gray)</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="features">
      <h2 class="features-title">Features</h2>

      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 10H32M8 20H32M8 30H24" stroke="#007ACC" stroke-width="3" stroke-linecap="round" />
            </svg>
          </div>
          <h3>Markdown Support</h3>
          <p>Full GitHub Flavored Markdown with live preview, task lists, tables, and more.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="5" y="10" width="10" height="20" stroke="#007ACC" stroke-width="2" fill="none" />
              <rect x="25" y="10" width="10" height="20" stroke="#007ACC" stroke-width="2" fill="none" />
              <path d="M15 20H25M20 15V25" stroke="#007ACC" stroke-width="2" />
            </svg>
          </div>
          <h3>Mermaid Diagrams</h3>
          <p>Create flowcharts, sequence diagrams, and other visualizations directly in your text.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <text x="8" y="28" font-size="24" font-weight="bold" fill="#007ACC">∑x²</text>
            </svg>
          </div>
          <h3>Math Expressions</h3>
          <p>Beautiful mathematical notation with KaTeX support for inline and display equations.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="5" y="5" width="30" height="30" rx="2" stroke="#007ACC" stroke-width="2" fill="none" />
              <path d="M10 15L15 10M25 10L30 15M10 25L15 30M25 30L30 25" stroke="#007ACC" stroke-width="2" />
            </svg>
          </div>
          <h3>Syntax Highlighting</h3>
          <p>Code blocks with syntax highlighting for 100+ languages and one-click copy buttons.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="5" y="10" width="12" height="20" stroke="#007ACC" stroke-width="2" fill="none" />
              <rect x="23" y="10" width="12" height="20" stroke="#007ACC" stroke-width="2" fill="none" />
              <rect x="5" y="10" width="2" height="20" fill="#007ACC" />
            </svg>
          </div>
          <h3>Two-Page Spread</h3>
          <p>Edit and view content in a natural book-like layout with left and right pages.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="20" cy="20" r="6" fill="#007ACC" />
              <path d="M20 5V10M20 30V35M35 20H30M10 20H5M30 10L26 14M14 26L10 30M30 30L26 26M14 14L10 10"
                stroke="#007ACC" stroke-width="2" stroke-linecap="round" />
            </svg>
          </div>
          <h3>Dark & Light Themes</h3>
          <p>Switch between beautiful light and dark themes that are easy on the eyes.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="8" y="8" width="24" height="24" rx="2" stroke="#007ACC" stroke-width="2" fill="none" />
              <path d="M20 15V25M15 20H25" stroke="#007ACC" stroke-width="2" stroke-linecap="round" />
            </svg>
          </div>
          <h3>Auto-Save</h3>
          <p>Your work is automatically saved to local storage. Never lose your progress.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="8" y="12" width="20" height="16" rx="2" stroke="#007ACC" stroke-width="2" fill="none" />
              <path d="M15 12V8L25 8V12" stroke="#007ACC" stroke-width="2" />
              <circle cx="28" cy="28" r="4" fill="#007ACC" />
            </svg>
          </div>
          <h3>Drag & Drop</h3>
          <p>Easily add images and links by dragging them directly into your pages.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="5" y="8" width="12" height="24" rx="1" stroke="#007ACC" stroke-width="2" fill="none" />
              <rect x="23" y="8" width="12" height="24" rx="1" stroke="#007ACC" stroke-width="2" fill="none" />
              <path d="M9 14H13M9 18H13M9 22H13" stroke="#28a745" stroke-width="1.5" stroke-linecap="round" />
              <path d="M27 14H31M27 18H31M27 22H31" stroke="#dc3545" stroke-width="1.5" stroke-linecap="round" />
            </svg>
          </div>
          <h3>Diff Checker</h3>
          <p>Compare left and right pages side-by-side with visual diff highlighting in book view mode.</p>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="home-footer">
      <div class="footer-content">
        <div class="footer-grid">
          <!-- About Section -->
          <div class="footer-section">
            <h3 class="footer-heading">Open Book</h3>
            <p class="footer-description">
              A modern, fully static markdown-based book editor with a beautiful two-page spread interface.
              Write, edit, and organize your content with powerful features.
            </p>
          </div>

          <!-- Features Links -->
          <div class="footer-section">
            <h3 class="footer-heading">Features</h3>
            <ul class="footer-links">
              <li><span class="footer-feature-item">Markdown Support</span></li>
              <li><span class="footer-feature-item">Mermaid Diagrams</span></li>
              <li><span class="footer-feature-item">Math Expressions</span></li>
              <li><span class="footer-feature-item">Syntax Highlighting</span></li>
              <li><span class="footer-feature-item">Dark & Light Themes</span></li>
            </ul>
          </div>

          <!-- Resources Links -->
          <div class="footer-section">
            <h3 class="footer-heading">Resources</h3>
            <ul class="footer-links">
              <li><a href="https://www.markdownguide.org/" target="_blank" rel="noopener noreferrer">Markdown Guide</a>
              </li>
              <li><a href="https://mermaid.js.org/intro/" target="_blank" rel="noopener noreferrer">Mermaid Docs</a>
              </li>
              <li><a href="https://katex.org/docs/supported.html" target="_blank" rel="noopener noreferrer">KaTeX
                  Reference</a></li>
            </ul>
          </div>

          <!-- Quick Links -->
          <div class="footer-section">
            <h3 class="footer-heading">Quick Links</h3>
            <ul class="footer-links">
              <li><router-link to="/edit">Editor</router-link></li>
              <li><router-link to="/view">View Mode</router-link></li>
              <li><a href="#" @click.prevent>Documentation</a></li>
              <li><a href="#" @click.prevent>GitHub</a></li>
            </ul>
          </div>
        </div>

        <!-- Footer Bottom -->
        <div class="footer-bottom">
          <p class="footer-copyright">
            © {{ new Date().getFullYear() }} Open Book.
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useTheme } from '@/composables/useTheme';
import mermaid from 'mermaid';
import { marked } from 'marked';
import katex from 'katex';
import hljs from 'highlight.js';

const router = useRouter();
const { isDarkTheme, toggleTheme } = useTheme();

// Track which copy button is showing tooltip
const copiedIndex = ref<number | null>(null);
const copiedMathIndex = ref<number | null>(null);
const copiedCodeIndex = ref<number | null>(null);

// Store code examples
const codeExamples = [
  `interface Book {
  title: string;
  author: string;
  pages: number;
}

function createBook(title: string, author: string): Book {
  return {
    title,
    author,
    pages: 0
  };
}`,
  `class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author
        self.pages = 0

    def add_chapter(self, name: str, pages: int):
        self.pages += pages
        print(f"Added chapter: {name}")
    
    def remove_chapter(self, name: str):
        self.pages -= pages
        print(f"Removed chapter: {name}")`
];

// Compute highlighted code
const highlightedCode = computed(() => {
  return codeExamples.map((code, index) => {
    const language = index === 0 ? 'typescript' : 'python';
    try {
      return hljs.highlight(code, { language }).value;
    } catch (e) {
      return hljs.highlightAuto(code).value;
    }
  });
});

// Store mermaid code for each example
const mermaidCodes = [
  `graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E`,
  `classDiagram
    class Book {
        +String title
        +String author
        +publish()
    }
    class Chapter {
        +String name
        +int pages
    }
    Book "1" --> "*" Chapter`,
  `erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ITEM : contains
    USER {
        string name
        string email
    }`
];

// Copy mermaid code to clipboard
async function copyMermaidCode(index: number) {
  const code = mermaidCodes[index];
  if (!code) return;

  try {
    await navigator.clipboard.writeText(code);

    // Show tooltip
    copiedIndex.value = index;

    // Hide tooltip after 2 seconds
    setTimeout(() => {
      copiedIndex.value = null;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy code:', err);
  }
}

// Try mermaid code - open in new tab without overwriting current work
function tryMermaidCode(index: number) {
  const code = mermaidCodes[index];
  if (!code) return;

  // Create a new book with the mermaid code
  const newBook = {
    filename: 'mermaid-example',
    spreads: [
      {
        left: `# Mermaid Example\n\n\`\`\`mermaid\n${code}\n\`\`\``,
        right: '',
        leftWidth: '1',
        rightWidth: '1'
      }
    ]
  };

  // Encode the book data as base64 to pass in URL
  const bookData = btoa(encodeURIComponent(JSON.stringify(newBook)));

  // Open in new tab with the example data
  const url = `${window.location.origin}/view?example=${bookData}`;
  window.open(url, '_blank');
}

// Copy code example to clipboard
async function copyCodeExample(index: number) {
  const code = codeExamples[index];
  if (!code) return;

  try {
    await navigator.clipboard.writeText(code);

    // Show tooltip
    copiedCodeIndex.value = index;

    // Hide tooltip after 2 seconds
    setTimeout(() => {
      copiedCodeIndex.value = null;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy code:', err);
  }
}

// Try code example - open in new tab
function tryCodeExample(index: number) {
  const code = codeExamples[index];
  if (!code) return;

  const language = index === 0 ? 'typescript' : 'python';

  // Create a new book with the code example
  const newBook = {
    filename: `${language}-example`,
    spreads: [
      {
        left: `# ${language.charAt(0).toUpperCase() + language.slice(1)} Example\n\n\`\`\`${language}\n${code}\n\`\`\``,
        right: '',
        leftWidth: '1',
        rightWidth: '1'
      }
    ]
  };

  // Encode the book data as base64 to pass in URL
  const bookData = btoa(encodeURIComponent(JSON.stringify(newBook)));

  // Open in new tab with the example data
  const url = `${window.location.origin}/view?example=${bookData}`;
  window.open(url, '_blank');
}

// Initialize Mermaid
function initMermaid() {
  mermaid.initialize({
    startOnLoad: false,
    theme: isDarkTheme.value ? 'dark' : 'default',
    securityLevel: 'loose',
    fontFamily: 'inherit'
  });
}

// Render all Mermaid diagrams
async function renderMermaidDiagrams() {
  initMermaid();

  // Wait a bit for DOM to be ready
  await new Promise(resolve => setTimeout(resolve, 100));

  // Look for both original code elements and already-rendered containers
  const mermaidExamples = document.querySelectorAll('.mermaid-example');

  mermaidExamples.forEach((example, index) => {
    const preview = example.querySelector('.mermaid-preview');
    if (!preview) return;

    // Get the code from mermaidCodes array instead of DOM
    const code = mermaidCodes[index];
    if (!code) return;

    // Find or create the container
    let container = preview.querySelector('.mermaid-rendered') as HTMLElement;

    if (!container) {
      // First time rendering - replace the code element
      const codeElement = preview.querySelector('.mermaid-code');
      if (!codeElement) return;

      container = document.createElement('div');
      container.className = 'mermaid-rendered';
      container.setAttribute('data-index', index.toString());
      codeElement.parentElement?.replaceChild(container, codeElement);
    }

    // Render the diagram
    mermaid.render(`mermaid-svg-${Date.now()}-${index}`, code).then(({ svg }) => {
      container.innerHTML = svg;
    }).catch((error) => {
      console.error('Mermaid rendering error:', error);
      // Fallback to showing code if rendering fails
      container.innerHTML = `<pre class="mermaid-code">${code}</pre>`;
    });
  });
}

// Store math code for each example (for preview - no titles)
const mathCodesPreview = [
  `Einstein's equation: $E = mc^2$

Pythagorean theorem:

$$
a^2 + b^2 = c^2
$$

The golden ratio: $\\phi = \\frac{1 + \\sqrt{5}}{2}$`,
  `Derivative definition:

$$
f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}
$$

Fundamental theorem of calculus:

$$
\\int_a^b f(x) dx = F(b) - F(a)
$$

Sum notation: $\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$`,
  `Normal distribution:

$$
f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x-\\mu}{\\sigma}\\right)^2}
$$

Matrix:

$$
A = \\begin{pmatrix}
a & b \\\\
c & d
\\end{pmatrix}
$$

Binomial theorem: $\\binom{n}{k} = \\frac{n!}{k!(n-k)!}$`
];

// Store math code for each example (for "Try It" - with titles)
const mathCodes = [
  `# Basic Math Examples

Einstein's equation: $E = mc^2$

Pythagorean theorem:

$$
a^2 + b^2 = c^2
$$

The golden ratio: $\\phi = \\frac{1 + \\sqrt{5}}{2}$`,
  `# Calculus Examples

Derivative definition:

$$
f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}
$$

Fundamental theorem of calculus:

$$
\\int_a^b f(x) dx = F(b) - F(a)
$$

Sum notation: $\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$`,
  `# Advanced Math Examples

Normal distribution:

$$
f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x-\\mu}{\\sigma}\\right)^2}
$$

Matrix:

$$
A = \\begin{pmatrix}
a & b \\\\
c & d
\\end{pmatrix}
$$

Binomial theorem: $\\binom{n}{k} = \\frac{n!}{k!(n-k)!}$`
];

// Copy math code to clipboard
async function copyMathCode(index: number) {
  const code = mathCodes[index];
  if (!code) return;

  try {
    await navigator.clipboard.writeText(code);

    // Show tooltip
    copiedMathIndex.value = index;

    // Hide tooltip after 2 seconds
    setTimeout(() => {
      copiedMathIndex.value = null;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy code:', err);
  }
}

// Try math code - open in new tab without overwriting current work
function tryMathCode(index: number) {
  const code = mathCodes[index];
  if (!code) return;

  // Create a new book with the math code
  const newBook = {
    filename: 'math-example',
    spreads: [
      {
        left: code,
        right: '',
        leftWidth: '1',
        rightWidth: '1'
      }
    ]
  };

  // Encode the book data as base64 to pass in URL
  const bookData = btoa(encodeURIComponent(JSON.stringify(newBook)));

  // Open in new tab with the example data
  const url = `${window.location.origin}/view?example=${bookData}`;
  window.open(url, '_blank');
}

// Render math expressions in preview cards
async function renderMathExpressions() {
  // Wait a bit for DOM to be ready
  await new Promise(resolve => setTimeout(resolve, 100));

  const mathExamples = document.querySelectorAll('.math-example');

  mathExamples.forEach((example, index) => {
    const preview = example.querySelector('.math-preview');
    if (!preview) return;

    // Get the code from mathCodesPreview array (without titles)
    const code = mathCodesPreview[index];
    if (!code) return;

    // Find or create the container
    let container = preview.querySelector('.math-rendered') as HTMLElement;

    if (!container) {
      // First time rendering - replace the code element
      const codeElement = preview.querySelector('.math-code');
      if (!codeElement) return;

      container = document.createElement('div');
      container.className = 'math-rendered';
      container.setAttribute('data-index', index.toString());
      codeElement.parentElement?.replaceChild(container, codeElement);
    }

    // Render the markdown with math
    renderMarkdownWithMath(code, container);
  });
}

// Helper function to render markdown with math expressions
function renderMarkdownWithMath(markdown: string, targetElement: HTMLElement) {
  // Store math expressions before markdown processing
  const mathBlocks: { placeholder: string; content: string; display: boolean }[] = [];
  let mathIndex = 0;

  // Protect block math ($$...$$) - must come before inline math
  let processedMarkdown = markdown.replace(/\$\$([\s\S]+?)\$\$/g, (match, content) => {
    const placeholder = `MATH_BLOCK_${mathIndex++}`;
    mathBlocks.push({ placeholder, content: content.trim(), display: true });
    return placeholder;
  });

  // Protect inline math ($...$)
  processedMarkdown = processedMarkdown.replace(/\$([^\$\n]+?)\$/g, (match, content) => {
    const placeholder = `MATH_INLINE_${mathIndex++}`;
    mathBlocks.push({ placeholder, content: content.trim(), display: false });
    return placeholder;
  });

  // Configure marked
  marked.setOptions({
    gfm: true,
    breaks: true,
    headerIds: true,
    mangle: false
  });

  // Render markdown
  let html = marked.parse(processedMarkdown) as string;

  // Restore math expressions as placeholders
  mathBlocks.forEach(({ placeholder, content, display }) => {
    const mathPlaceholder = display
      ? `<div class="math-placeholder" data-math="${escapeHtml(content)}" data-display="true"></div>`
      : `<span class="math-placeholder" data-math="${escapeHtml(content)}" data-display="false"></span>`;
    html = html.replace(placeholder, mathPlaceholder);
  });

  targetElement.innerHTML = html;

  // Render KaTeX math expressions from placeholders
  renderMathPlaceholders(targetElement);
}

// Helper function to escape HTML
function escapeHtml(text: string): string {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Render math placeholders with KaTeX
function renderMathPlaceholders(element: HTMLElement) {
  try {
    const placeholders = element.querySelectorAll('.math-placeholder');

    placeholders.forEach((placeholder) => {
      const mathContent = placeholder.getAttribute('data-math');
      const isDisplay = placeholder.getAttribute('data-display') === 'true';

      if (!mathContent) return;

      try {
        // Create container for rendered math
        const container = document.createElement(isDisplay ? 'div' : 'span');

        // Render math with KaTeX
        katex.render(mathContent, container, {
          displayMode: isDisplay,
          throwOnError: false,
          strict: false,
          trust: false
        });

        // Replace placeholder with rendered math
        placeholder.replaceWith(container);
      } catch (error) {
        console.error('KaTeX rendering error:', error);
        // Keep the placeholder if rendering fails
        placeholder.textContent = isDisplay ? `$$${mathContent}$$` : `$${mathContent}$`;
      }
    });
  } catch (error) {
    console.error('Math placeholder processing error:', error);
  }
}

function startWriting() {
  // Always start in edit mode - update localStorage before navigating
  localStorage.setItem('openbook_viewmode', 'false');
  router.push('/edit');
}

// Render diagrams when component mounts
onMounted(() => {
  renderMermaidDiagrams();
  renderMathExpressions();
});

// Re-render diagrams when theme changes
watch(isDarkTheme, () => {
  renderMermaidDiagrams();
  renderMathExpressions();
});
</script>

<style scoped>
.home {
  background: var(--bg-color);
  color: var(--text-color);
}

/* Navigation Bar */
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg-color);
  border-bottom: 1px solid var(--border-color);
}

.navbar-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 40px;
}

.navbar-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-color);
  text-decoration: none;
  font-size: 16px;
  font-weight: 600;
  transition: opacity 0.2s ease;
}

.navbar-logo:hover {
  opacity: 0.7;
}

.navbar-links {
  display: flex;
  gap: 4px;
}

.navbar-link {
  padding: 6px 12px;
  color: var(--text-color);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  border-radius: 6px;
  transition: background-color 0.2s ease;
  opacity: 0.7;
}

.navbar-link:hover {
  background: var(--page-bg);
  opacity: 1;
}

.navbar-link.router-link-active {
  background: var(--page-bg);
  opacity: 1;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.theme-toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-color);
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.theme-toggle-btn:hover {
  background: var(--page-bg);
}

.navbar-signup-btn {
  padding: 6px 14px;
  background: #007ACC;
  border: none;
  border-radius: 6px;
  color: #ffffff;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: opacity 0.2s ease;
}

.navbar-signup-btn:hover {
  opacity: 0.9;
}

/* Hero Section */
.hero {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 120px 32px 80px;
  background: var(--bg-color);
}

.hero-content {
  max-width: 720px;
  text-align: center;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  margin: 0 0 16px;
  color: var(--text-color);
  letter-spacing: -0.02em;
}

.hero-subtitle {
  font-size: 20px;
  font-weight: 400;
  margin: 0 0 24px;
  color: var(--text-color);
  opacity: 0.6;
}

.hero-description {
  font-size: 16px;
  line-height: 1.6;
  margin: 0 0 40px;
  color: var(--text-color);
  opacity: 0.6;
  max-width: 560px;
  margin-left: auto;
  margin-right: auto;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 500;
  color: #ffffff;
  background: #007ACC;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.cta-button:hover {
  opacity: 0.9;
}

.cta-button:active {
  opacity: 0.8;
}

/* Mermaid Examples Section */
.mermaid-section {
  padding: 80px 32px;
  background: var(--page-bg);
  border-top: 1px solid var(--border-color);
}

.mermaid-content {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: 32px;
  font-weight: 600;
  margin: 0 0 16px;
  color: var(--text-color);
}

.section-description {
  text-align: center;
  font-size: 16px;
  line-height: 1.6;
  margin: 0 0 48px;
  color: var(--text-color);
  opacity: 0.6;
  max-width: 640px;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 48px;
}

.mermaid-examples {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
}

.mermaid-example {
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 20px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.mermaid-example:hover {
  border-color: rgba(0, 122, 204, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

body.dark-theme .mermaid-example:hover {
  box-shadow: 0 2px 8px rgba(0, 122, 204, 0.1);
}

.mermaid-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.mermaid-example h3 {
  font-size: 15px;
  font-weight: 600;
  margin: 0;
  color: var(--text-color);
}

.mermaid-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 6px 8px;
  cursor: pointer;
  color: var(--text-color);
  opacity: 0.6;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.action-btn:hover {
  opacity: 1;
  border-color: #007ACC;
  color: #007ACC;
  background: rgba(0, 122, 204, 0.05);
}

.action-btn:active {
  transform: scale(0.95);
}

.action-btn svg {
  display: block;
}

.copy-tooltip {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  background: #007ACC;
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  pointer-events: none;
  animation: tooltipFadeIn 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.copy-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 4px solid transparent;
  border-top-color: #007ACC;
}

@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-4px);
  }

  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

.mermaid-preview {
  background: var(--page-bg);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: 16px;
  overflow-x: auto;
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mermaid-rendered {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mermaid-rendered svg {
  max-width: 100%;
  height: auto;
}

.mermaid-code {
  margin: 0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'source-code-pro', monospace;
  font-size: 12px;
  line-height: 1.6;
  color: var(--text-color);
  opacity: 0.8;
  white-space: pre;
  overflow-x: auto;
}

.mermaid-footer {
  margin-top: 32px;
  text-align: center;
}

.see-more-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #007ACC;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.see-more-link:hover {
  background: rgba(0, 122, 204, 0.08);
  gap: 8px;
}

.see-more-link svg {
  transition: transform 0.2s ease;
}

.see-more-link:hover svg {
  transform: translateX(2px);
}

/* Code Syntax Highlighting Section */
.code-section {
  padding: 80px 32px;
  background: var(--bg-color);
  border-top: 1px solid var(--border-color);
}

.code-content {
  max-width: 1200px;
  margin: 0 auto;
}

.code-examples {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
}

.code-example {
  background: var(--page-bg);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 20px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.code-example:hover {
  border-color: rgba(0, 122, 204, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

body.dark-theme .code-example:hover {
  box-shadow: 0 2px 8px rgba(0, 122, 204, 0.1);
}

.code-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.code-example h3 {
  font-size: 15px;
  font-weight: 600;
  margin: 0;
  color: var(--text-color);
}

.code-actions {
  display: flex;
  gap: 8px;
}

.code-preview {
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  overflow: hidden;
}

.code-preview pre {
  margin: 0;
  padding: 16px;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.5;
}

.code-preview code {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
  display: block;
}

.code-footer {
  margin-top: 32px;
  text-align: center;
}

/* Diff Checker Section */
.diff-section {
  padding: 80px 32px;
  background: var(--page-bg);
  border-top: 1px solid var(--border-color);
}

.diff-content {
  max-width: 1200px;
  margin: 0 auto;
}

.diff-example {
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 24px;
  margin-top: 32px;
}

.diff-example-header {
  margin-bottom: 24px;
  text-align: center;
}

.diff-example-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px;
  color: var(--text-color);
}

.diff-example-header p {
  font-size: 14px;
  margin: 0;
  color: var(--text-color);
  opacity: 0.6;
}

.diff-example-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.diff-pane {
  border: 1px solid var(--border-color);
  border-radius: 6px;
  overflow: hidden;
}

.diff-pane-header {
  background: var(--page-bg);
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-color);
  border-bottom: 1px solid var(--border-color);
}

.diff-pane-body {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
  font-size: 13px;
  line-height: 1.4;
}

.diff-pane-body .diff-line {
  padding: 2px 8px;
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.diff-pane-body .diff-symbol {
  display: inline-block;
  width: 20px;
  font-weight: bold;
  margin-right: 8px;
  user-select: none;
}

.diff-pane-body .diff-line-added {
  background-color: #e6ffed;
  border-left: 3px solid #28a745;
  color: #24292f;
}

.diff-pane-body .diff-line-added .diff-symbol {
  color: #28a745;
}

.diff-pane-body .diff-line-removed {
  background-color: #ffeef0;
  border-left: 3px solid #dc3545;
  color: #24292f;
}

.diff-pane-body .diff-line-removed .diff-symbol {
  color: #dc3545;
}

.diff-pane-body .diff-line-placeholder {
  background-color: #f5f5f5;
  border-left: 3px solid #d0d0d0;
  color: #57606a;
}

.diff-pane-body .diff-line-placeholder .diff-symbol {
  color: #999;
}

.diff-pane-body .diff-line-unchanged {
  background-color: transparent;
  border-left: 3px solid transparent;
}

.diff-legend {
  display: flex;
  gap: 24px;
  justify-content: center;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
}

.diff-legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-color);
}

.diff-legend-box {
  width: 16px;
  height: 16px;
  border-radius: 3px;
  border: 1px solid var(--border-color);
}

.diff-legend-added {
  background-color: #e6ffed;
  border-color: #28a745;
}

.diff-legend-removed {
  background-color: #ffeef0;
  border-color: #dc3545;
}

.diff-legend-placeholder {
  background-color: #f5f5f5;
  border-color: #d0d0d0;
}

/* Dark theme diff colors */
body.dark-theme .diff-pane-body .diff-line-added {
  background-color: #1e4620;
  border-left-color: #3fb950;
  color: #c9d1d9;
}

body.dark-theme .diff-pane-body .diff-line-added .diff-symbol {
  color: #3fb950;
}

body.dark-theme .diff-pane-body .diff-line-removed {
  background-color: #4a1c1c;
  border-left-color: #f85149;
  color: #252627;
}

body.dark-theme .diff-pane-body .diff-line-removed .diff-symbol {
  color: #f85149;
}

body.dark-theme .diff-pane-body .diff-line-placeholder {
  background-color: #0d1117;
  border-left-color: #444;
  color: #8b949e;
}

body.dark-theme .diff-pane-body .diff-line-placeholder .diff-symbol {
  color: #666;
}

body.dark-theme .diff-legend-added {
  background-color: #1e4620;
  border-color: #3fb950;
}

body.dark-theme .diff-legend-removed {
  background-color: #4a1c1c;
  border-color: #f85149;
}

body.dark-theme .diff-legend-placeholder {
  background-color: #0d1117;
  border-color: #444;
}

/* Mathematical Expressions Section */
.math-section {
  padding: 80px 32px;
  background: var(--bg-color);
  border-top: 1px solid var(--border-color);
}

.math-content {
  max-width: 1200px;
  margin: 0 auto;
}

.math-examples {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
}

.math-example {
  background: var(--page-bg);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 20px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.math-example:hover {
  border-color: rgba(0, 122, 204, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

body.dark-theme .math-example:hover {
  box-shadow: 0 2px 8px rgba(0, 122, 204, 0.1);
}

.math-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.math-example h3 {
  font-size: 15px;
  font-weight: 600;
  margin: 0;
  color: var(--text-color);
}

.math-actions {
  display: flex;
  gap: 8px;
}

.math-preview {
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: 16px;
  overflow-x: auto;
  min-height: 150px;
}

.math-code {
  margin: 0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'source-code-pro', monospace;
  font-size: 12px;
  line-height: 1.6;
  color: var(--text-color);
  opacity: 0.8;
  white-space: pre;
  overflow-x: auto;
}

.math-rendered {
  color: var(--text-color);
  font-size: 14px;
  line-height: 1.8;
}

.math-rendered h1 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: var(--text-color);
}

.math-rendered p {
  margin: 8px 0;
  color: var(--text-color);
}

.math-rendered .katex {
  font-size: 1em;
  color: var(--text-color);
}

.math-rendered .katex-display {
  margin: 12px 0;
  overflow-x: auto;
  overflow-y: hidden;
}

/* Dark theme support for KaTeX in math previews */
body.dark-theme .math-rendered .katex {
  color: var(--text-color);
}

body.dark-theme .math-rendered .katex .mord,
body.dark-theme .math-rendered .katex .mbin,
body.dark-theme .math-rendered .katex .mrel,
body.dark-theme .math-rendered .katex .mop,
body.dark-theme .math-rendered .katex .mpunct,
body.dark-theme .math-rendered .katex .mopen,
body.dark-theme .math-rendered .katex .mclose,
body.dark-theme .math-rendered .katex .minner {
  color: var(--text-color);
}

.math-footer {
  margin-top: 32px;
  text-align: center;
}

/* Features Section */
.features {
  padding: 80px 32px;
  background: var(--bg-color);
}

.features-title {
  text-align: center;
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 48px;
  color: var(--text-color);
}

.features-grid {
  max-width: 1000px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.feature-card {
  padding: 24px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border-color: rgba(0, 122, 204, 0.3);
}

body.dark-theme .feature-card:hover {
  box-shadow: 0 2px 8px rgba(0, 122, 204, 0.1);
}

.feature-icon {
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.feature-card h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px;
  color: var(--text-color);
}

.feature-card p {
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
  color: var(--text-color);
  opacity: 0.6;
}

/* Footer */
.home-footer {
  background: var(--page-bg);
  border-top: 1px solid var(--border-color);
  padding: 80px 32px 32px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 48px;
  margin-bottom: 48px;
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: center;
}

.footer-heading {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: var(--text-color);
}

.footer-description {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-color);
  opacity: 0.7;
  max-width: 320px;
  margin-left: auto;
  margin-right: auto;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
}

.footer-links li {
  margin: 0;
}

.footer-links a {
  color: var(--text-color);
  text-decoration: none;
  font-size: 14px;
  opacity: 0.7;
  transition: all 0.2s ease;
  display: inline-block;
}

.footer-links a:hover {
  opacity: 1;
  color: #007ACC;
}

.footer-feature-item {
  color: var(--text-color);
  font-size: 14px;
  opacity: 0.7;
  display: inline-block;
}

.footer-bottom {
  border-top: 1px solid var(--border-color);
  padding-top: 24px;
  text-align: center;
}

.footer-copyright {
  margin: 0;
  font-size: 13px;
  color: var(--text-color);
  opacity: 0.6;
}

/* Responsive */
@media (max-width: 768px) {
  .navbar-content {
    padding: 0 16px;
  }

  .navbar-left {
    gap: 16px;
  }

  .navbar-links {
    display: none;
  }

  .navbar-right {
    gap: 8px;
  }

  .navbar-link {
    display: none;
  }

  .navbar-signup-btn {
    padding: 6px 12px;
    font-size: 13px;
  }

  .hero {
    padding: 60px 20px;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .hero-description {
    font-size: 15px;
  }

  .section-title {
    font-size: 28px;
  }

  .section-description {
    font-size: 15px;
  }

  .mermaid-section {
    padding: 60px 20px;
  }

  .mermaid-examples {
    grid-template-columns: 1fr;
  }

  .mermaid-code {
    font-size: 11px;
  }

  .code-section {
    padding: 60px 20px;
  }

  .code-examples {
    grid-template-columns: 1fr;
  }

  .features-title {
    font-size: 24px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .math-section {
    padding: 60px 20px;
  }

  .math-examples {
    grid-template-columns: 1fr;
  }

  .diff-section {
    padding: 60px 20px;
  }

  .diff-example-content {
    grid-template-columns: 1fr;
  }

  .diff-legend {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .footer-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .footer-description {
    max-width: 100%;
  }
}
</style>

<style>
/* Import highlight.js theme */
@import 'highlight.js/styles/github.css';

/* Dark theme for highlight.js */
body.dark-theme .code-preview {
  background: #0d1117;
}

body.dark-theme .hljs {
  background: #0d1117;
  color: #c9d1d9;
}

body.dark-theme .hljs-keyword,
body.dark-theme .hljs-selector-tag,
body.dark-theme .hljs-literal,
body.dark-theme .hljs-section,
body.dark-theme .hljs-link {
  color: #ff7b72;
}

body.dark-theme .hljs-function .hljs-keyword {
  color: #d2a8ff;
}

body.dark-theme .hljs-subst {
  color: #c9d1d9;
}

body.dark-theme .hljs-string,
body.dark-theme .hljs-title,
body.dark-theme .hljs-name,
body.dark-theme .hljs-type,
body.dark-theme .hljs-attribute,
body.dark-theme .hljs-symbol,
body.dark-theme .hljs-bullet,
body.dark-theme .hljs-addition,
body.dark-theme .hljs-variable,
body.dark-theme .hljs-template-tag,
body.dark-theme .hljs-template-variable {
  color: #a5d6ff;
}

body.dark-theme .hljs-comment,
body.dark-theme .hljs-quote,
body.dark-theme .hljs-deletion,
body.dark-theme .hljs-meta {
  color: #8b949e;
}

body.dark-theme .hljs-doctag,
body.dark-theme .hljs-strong {
  font-weight: bold;
}

body.dark-theme .hljs-emphasis {
  font-style: italic;
}

body.dark-theme .hljs-number {
  color: #79c0ff;
}

body.dark-theme .hljs-built_in,
body.dark-theme .hljs-class .hljs-title {
  color: #ffa657;
}
</style>
