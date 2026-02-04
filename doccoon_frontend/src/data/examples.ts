// Predefined examples for the home page "Try it" functionality
// Each example has a unique key for simple URL references

export interface ExampleBook {
  filename: string;
  spreads: Array<{
    left: string;
    right: string;
    leftWidth: string;
    rightWidth: string;
  }>;
}

export const examples: Record<string, ExampleBook> = {
  // Code examples
  typescript: {
    filename: "typescript-example",
    spreads: [
      {
        left: `# TypeScript Example

\`\`\`typescript
interface Book {
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
}
\`\`\``,
        right: "",
        leftWidth: "1",
        rightWidth: "1",
      },
    ],
  },
  python: {
    filename: "python-example",
    spreads: [
      {
        left: `# Python Example

\`\`\`python
class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author
        self.pages = 0

    def add_chapter(self, name: str, pages: int):
        self.pages += pages
        print(f"Added chapter: {name}")

    def remove_chapter(self, name: str):
        self.pages -= pages
        print(f"Removed chapter: {name}")
\`\`\``,
        right: "",
        leftWidth: "1",
        rightWidth: "1",
      },
    ],
  },

  // Math examples
  "math-basic": {
    filename: "math-example",
    spreads: [
      {
        left: `# Basic Math Examples

Einstein's equation: $E = mc^2$

Pythagorean theorem:

$$
a^2 + b^2 = c^2
$$

The golden ratio: $\\phi = \\frac{1 + \\sqrt{5}}{2}$`,
        right: "",
        leftWidth: "1",
        rightWidth: "1",
      },
    ],
  },
  "math-calculus": {
    filename: "math-example",
    spreads: [
      {
        left: `# Calculus Examples

Derivative definition:

$$
f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}
$$

Fundamental theorem of calculus:

$$
\\int_a^b f(x) dx = F(b) - F(a)
$$

Sum notation: $\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$`,
        right: "",
        leftWidth: "1",
        rightWidth: "1",
      },
    ],
  },
  "math-advanced": {
    filename: "math-example",
    spreads: [
      {
        left: `# Advanced Math Examples

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

Binomial theorem: $\\binom{n}{k} = \\frac{n!}{k!(n-k)!}$`,
        right: "",
        leftWidth: "1",
        rightWidth: "1",
      },
    ],
  },

  // Mermaid examples
  flowchart: {
    filename: "mermaid-example",
    spreads: [
      {
        left: `# Mermaid Flowchart

\`\`\`mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
\`\`\``,
        right: "",
        leftWidth: "1",
        rightWidth: "1",
      },
    ],
  },
  "class-diagram": {
    filename: "mermaid-example",
    spreads: [
      {
        left: `# Mermaid Class Diagram

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
\`\`\``,
        right: "",
        leftWidth: "1",
        rightWidth: "1",
      },
    ],
  },
  "er-diagram": {
    filename: "mermaid-example",
    spreads: [
      {
        left: `# Entity Relationship Diagram

\`\`\`mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ITEM : contains
    USER {
        string name
        string email
    }
\`\`\``,
        right: "",
        leftWidth: "1",
        rightWidth: "1",
      },
    ],
  },

  // Diff example
  diff: {
    filename: "diff-example",
    spreads: [
      {
        left: `# Doccoon Features

- **Markdown Support**
- **Mermaid Diagrams**
- **Math Expressions**
- **Syntax Highlighting**
- **Dark & Light Themes**
`,
        right: `# Doccoon Features

- **Markdown Support**
- **Math Expressions**
- **Syntax Highlighting**
- **Dark & Light Themes**
- **Diff Checker**
`,
        leftWidth: "1",
        rightWidth: "1",
      },
    ],
  },
};

export function getExample(key: string): ExampleBook | undefined {
  return examples[key];
}
