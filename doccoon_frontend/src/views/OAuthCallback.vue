<template>
  <div class="flex items-center justify-center min-h-screen bg-[var(--bg-color)] text-[var(--text-color)]">
    <p class="text-sm opacity-60">Completing sign in...</p>
  </div>
</template>

<script setup lang="ts">
// This page is opened in a popup by the OAuth flow.
// The parent window reads the URL params and closes this popup.
// This component exists only to render something while the popup is open.
</script>
