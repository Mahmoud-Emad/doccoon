# [Doccoon](https://doccoon.com/)

A fully static front-end markdown-based book editor with a beautiful two-page spread interface.

## Features

- **Markdown Support** - Write content using standard Markdown syntax
- **Mermaid Diagrams** - Create flowcharts, sequence diagrams, and more
- **Math Expressions** - Render LaTeX math equations with KaTeX
- **Syntax Highlighting** - Code blocks with syntax highlighting
- **Dark & Light Themes** - Toggle between themes
- **Two-Page Spread** - Book-like reading and editing experience
- **Page View Mode** - Focus on a single page
- **Line Numbers** - Track your position while editing
- **Auto-Save** - Your work is automatically saved to browser storage
- **Fully Static** - No backend required, runs entirely in the browser

## Getting Started

### Option 1: Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the application at http://localhost:8080
```

To stop the container:

```bash
docker-compose down
```

### Option 2: Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Option 3: Docker without Compose

```bash
# Build the Docker image
docker build -t doccoon .

# Run the container
docker run -d -p 8080:80 --name doccoon doccoon

# Access the application at http://localhost:8080
```

### Usage

1. Open the application in your browser
2. Click "Get Started" to open the editor
3. Start writing in Markdown format
4. Toggle between Edit and View modes to see your rendered content
5. Switch between Book View (two pages) and Page View (single page)
6. Your work is automatically saved

## Keyboard Shortcuts

- **Edit/View Mode** - Toggle between editing and viewing
- **Book/Page View** - Switch between two-page and single-page layouts
- **Theme Toggle** - Switch between light and dark themes

## Technology Stack

- Vue 3
- TypeScript
- Vite
- Marked.js (Markdown rendering)
- KaTeX (Math rendering)
- Mermaid (Diagram rendering)

## License

MIT

## Author

© 2025 Doccoon
