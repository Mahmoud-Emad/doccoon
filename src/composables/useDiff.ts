import { ref } from 'vue';
import * as Diff from 'diff';

export interface DiffLine {
  content: string;
  type: 'added' | 'removed' | 'unchanged' | 'placeholder';
  lineNumber: number;
}

export function useDiff() {
  const isDiffMode = ref(false);

  function toggleDiffMode() {
    isDiffMode.value = !isDiffMode.value;
  }

  function computeDiff(leftContent: string, rightContent: string): { left: DiffLine[], right: DiffLine[] } {
    // Note: leftLines and rightLines are not used in the current implementation
    // as we use Diff.diffLines which handles the splitting internally
    const diff = Diff.diffLines(leftContent, rightContent);

    const leftResult: DiffLine[] = [];
    const rightResult: DiffLine[] = [];

    let leftLineNumber = 1;
    let rightLineNumber = 1;

    diff.forEach(part => {
      const lines = part.value.split('\n');
      // Remove the last empty line if it exists (from split)
      if (lines[lines.length - 1] === '') {
        lines.pop();
      }

      if (part.added) {
        // Lines added in right (not in left)
        // Show as removed on left, and add placeholder on right
        lines.forEach(line => {
          leftResult.push({
            content: line,
            type: 'removed',
            lineNumber: leftLineNumber++
          });
          // Add placeholder in right pane to maintain alignment
          rightResult.push({
            content: '',
            type: 'placeholder',
            lineNumber: -1 // Placeholder doesn't have a real line number
          });
        });
      } else if (part.removed) {
        // Lines removed from left (not in right)
        // Show as added on right, and add placeholder on left
        lines.forEach(line => {
          rightResult.push({
            content: line,
            type: 'added',
            lineNumber: rightLineNumber++
          });
          // Add placeholder in left pane to maintain alignment
          leftResult.push({
            content: '',
            type: 'placeholder',
            lineNumber: -1 // Placeholder doesn't have a real line number
          });
        });
      } else {
        // Unchanged lines
        lines.forEach(line => {
          leftResult.push({
            content: line,
            type: 'unchanged',
            lineNumber: leftLineNumber++
          });
          rightResult.push({
            content: line,
            type: 'unchanged',
            lineNumber: rightLineNumber++
          });
        });
      }
    });

    return { left: leftResult, right: rightResult };
  }

  function renderDiffToHtml(diffLines: DiffLine[]): string {
    return diffLines.map(line => {
      let className = '';
      let symbol = '';

      if (line.type === 'added') {
        className = 'diff-line-added';
        symbol = '<span class="diff-symbol">+</span>';
      } else if (line.type === 'removed') {
        className = 'diff-line-removed';
        symbol = '<span class="diff-symbol">-</span>';
      } else if (line.type === 'placeholder') {
        className = 'diff-line-placeholder';
        symbol = '<span class="diff-symbol">&nbsp;</span>';
      }

      const escapedContent = escapeHtml(line.content);
      return `<div class="diff-line ${className}">${symbol}${escapedContent || '&nbsp;'}</div>`;
    }).join('');
  }

  function escapeHtml(text: string): string {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  return {
    isDiffMode,
    toggleDiffMode,
    computeDiff,
    renderDiffToHtml
  };
}

