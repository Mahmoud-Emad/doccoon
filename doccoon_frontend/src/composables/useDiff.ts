import { ref } from "vue";
import * as Diff from "diff";
import { escapeHtml } from "@/utils/html";

export interface DiffLine {
  content: string;
  type: "added" | "removed" | "unchanged" | "placeholder";
  lineNumber: number;
}

export function useDiff() {
  const isDiffMode = ref(false);

  function toggleDiffMode() {
    isDiffMode.value = !isDiffMode.value;
  }

  function computeDiff(
    leftContent: string,
    rightContent: string,
  ): { left: DiffLine[]; right: DiffLine[] } {
    const diff = Diff.diffLines(leftContent, rightContent);

    const leftResult: DiffLine[] = [];
    const rightResult: DiffLine[] = [];

    let leftLineNumber = 1;
    let rightLineNumber = 1;

    diff.forEach((part) => {
      const lines = part.value.split("\n");
      // Remove the last empty line if it exists (from split)
      if (lines[lines.length - 1] === "") {
        lines.pop();
      }

      if (part.added) {
        // Lines added in right (not in left)
        lines.forEach((line) => {
          rightResult.push({
            content: line,
            type: "added",
            lineNumber: rightLineNumber++,
          });
          leftResult.push({
            content: "",
            type: "placeholder",
            lineNumber: -1,
          });
        });
      } else if (part.removed) {
        // Lines removed from left (not in right)
        lines.forEach((line) => {
          leftResult.push({
            content: line,
            type: "removed",
            lineNumber: leftLineNumber++,
          });
          rightResult.push({
            content: "",
            type: "placeholder",
            lineNumber: -1,
          });
        });
      } else {
        // Unchanged lines
        lines.forEach((line) => {
          leftResult.push({
            content: line,
            type: "unchanged",
            lineNumber: leftLineNumber++,
          });
          rightResult.push({
            content: line,
            type: "unchanged",
            lineNumber: rightLineNumber++,
          });
        });
      }
    });

    return { left: leftResult, right: rightResult };
  }

  function renderDiffToHtml(diffLines: DiffLine[]): string {
    return diffLines
      .map((line) => {
        let className = "";
        let symbol = "";

        if (line.type === "added") {
          className = "diff-line-added";
          symbol = '<span class="diff-symbol">+</span>';
        } else if (line.type === "removed") {
          className = "diff-line-removed";
          symbol = '<span class="diff-symbol">-</span>';
        } else if (line.type === "placeholder") {
          className = "diff-line-placeholder";
          symbol = '<span class="diff-symbol">&nbsp;</span>';
        }

        const escapedContent = escapeHtml(line.content);
        return `<div class="diff-line ${className}">${symbol}${escapedContent || "&nbsp;"}</div>`;
      })
      .join("");
  }

  return {
    isDiffMode,
    toggleDiffMode,
    computeDiff,
    renderDiffToHtml,
  };
}
