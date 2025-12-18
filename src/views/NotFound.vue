<template>
  <div class="not-found">
    <div class="not-found-content">
      <!-- Error Message -->
      <h1 class="error-code">404</h1>
      <h2 class="error-title">Page Not Found</h2>
      <p class="error-description">
        The page you're looking for doesn't exist or has been moved.
      </p>

      <!-- Action Buttons -->
      <div class="action-buttons">
        <button class="primary-button" @click="goHome">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 10L10 3L17 10M5 8V17H8V13H12V17H15V8" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          Go to Home
        </button>

        <button class="secondary-button" @click="goToEditor">
          Start Writing
        </button>
      </div>

      <!-- Helpful Links -->
      <div class="helpful-links">
        <p class="links-title">You might be looking for:</p>
        <div class="links-list">
          <a @click.prevent="goHome" href="/">Home Page</a>
          <span class="separator">•</span>
          <a @click.prevent="goToEditor" href="/edit">Editor</a>
          <span class="separator">•</span>
          <a @click.prevent="goToView" href="/view">View Mode</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

function goHome() {
  router.push('/');
}

function goToEditor() {
  router.push('/edit');
}

function goToView() {
  router.push('/view');
}
</script>

<style scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: var(--bg-color);
  color: var(--text-color);
  padding: 20px;
}

.not-found-content {
  max-width: 600px;
  text-align: center;
}

/* Error Icon */
.error-icon {
  margin: 0 auto 30px;
  color: var(--text-color);
  opacity: 0.6;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {

  0%,
  100% {
    transform: translateY(0px);
  }

  50% {
    transform: translateY(-10px);
  }
}

/* Error Text */
.error-code {
  font-size: 96px;
  font-weight: 700;
  margin: 0 0 16px;
  background: linear-gradient(135deg, #007ACC 0%, #005a9e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}

.error-title {
  font-size: 36px;
  font-weight: 600;
  margin: 0 0 16px;
  color: var(--text-color);
}

.error-description {
  font-size: 18px;
  line-height: 1.6;
  margin: 0 0 40px;
  color: var(--text-color);
  opacity: 0.7;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 60px;
  flex-wrap: wrap;
}

.primary-button,
.secondary-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.primary-button {
  color: #ffffff;
  background: linear-gradient(135deg, #007ACC 0%, #005a9e 100%);
  box-shadow: 0 4px 12px rgba(0, 122, 204, 0.3);
}

.primary-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 122, 204, 0.4);
}

.secondary-button {
  color: var(--text-color);
  background: var(--page-bg);
  border: 2px solid var(--border-color);
}

.secondary-button:hover {
  border-color: #007ACC;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Helpful Links */
.helpful-links {
  padding-top: 40px;
  border-top: 1px solid var(--border-color);
}

.links-title {
  font-size: 14px;
  margin: 0 0 12px;
  color: var(--text-color);
  opacity: 0.6;
  font-weight: 500;
}

.links-list {
  display: flex;
  gap: 12px;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.links-list a {
  color: #007ACC;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  cursor: pointer;
}

.links-list a:hover {
  text-decoration: underline;
  color: #005a9e;
}

.separator {
  color: var(--text-color);
  opacity: 0.3;
  font-size: 14px;
}

/* Responsive */
@media (max-width: 768px) {
  .error-code {
    font-size: 72px;
  }

  .error-title {
    font-size: 28px;
  }

  .error-description {
    font-size: 16px;
  }

  .action-buttons {
    flex-direction: column;
    align-items: stretch;
  }

  .primary-button,
  .secondary-button {
    width: 100%;
    justify-content: center;
  }
}
</style>
