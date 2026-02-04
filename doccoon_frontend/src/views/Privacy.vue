<template>
    <div class="min-h-screen bg-[var(--bg-color)]">
        <!-- Header -->
        <nav
            class="sticky top-0 z-100 bg-[var(--bg-color)] border-b border-[var(--border-color)]"
        >
            <div
                class="max-w-[800px] mx-auto px-8 max-md:px-4 h-[60px] flex items-center justify-between"
            >
                <router-link
                    to="/"
                    class="flex items-center gap-2 text-[var(--text-color)] no-underline"
                >
                    <img
                        :src="isDarkTheme ? logoDark : logoLight"
                        alt="Doccoon"
                        class="h-8"
                    />
                    <span class="text-base font-semibold">Doccoon</span>
                </router-link>

                <button
                    class="flex items-center justify-center w-8 h-8 bg-transparent border border-[var(--border-color)] rounded-md text-[var(--text-color)] cursor-pointer transition-colors duration-200 hover:bg-[var(--section-alt-bg)]"
                    title="Toggle theme"
                    @click="toggleTheme"
                >
                    <BaseIcon :name="isDarkTheme ? 'sun' : 'moon'" :size="16" />
                </button>
            </div>
        </nav>

        <!-- Content -->
        <main class="max-w-[800px] mx-auto px-8 max-md:px-4 py-12">
            <div class="mb-8">
                <p
                    class="text-sm font-semibold tracking-widest uppercase text-primary mb-2"
                >
                    Legal
                </p>
                <h1
                    class="text-[32px] max-md:text-[24px] font-bold text-[var(--text-color)] mb-4"
                >
                    Privacy Policy
                </h1>
                <p class="text-sm text-[var(--text-color)] opacity-50">
                    Last updated: {{ lastUpdated }}
                </p>
            </div>

            <div class="prose">
                <section class="mb-8">
                    <h2>Introduction</h2>
                    <p>
                        At Doccoon, we take your privacy seriously. This Privacy
                        Policy explains how we collect, use, disclose, and
                        safeguard your information when you use our service.
                    </p>
                </section>

                <section class="mb-8">
                    <h2>Information We Collect</h2>
                    <h3>Account Information</h3>
                    <p>
                        When you create an account, we collect your email
                        address, name, and authentication credentials. If you
                        sign in using Google or GitHub, we receive basic profile
                        information from those services.
                    </p>

                    <h3>Content Data</h3>
                    <p>
                        We store the books and pages you create within Doccoon.
                        This content is associated with your account and synced
                        to our servers to enable cloud storage and cross-device
                        access.
                    </p>

                    <h3>Usage Information</h3>
                    <p>
                        We collect information about how you interact with our
                        service, including features used, pages visited, and
                        actions taken. This helps us improve the product.
                    </p>

                    <h3>API Keys</h3>
                    <p>
                        If you add OpenAI or Gemini API keys, they are encrypted
                        and stored securely on our servers. These keys are only
                        used to process AI requests on your behalf.
                    </p>
                </section>

                <section class="mb-8">
                    <h2>How We Use Your Information</h2>
                    <ul>
                        <li>To provide and maintain our service</li>
                        <li>To sync your content across devices</li>
                        <li>To process AI-powered features using your API keys</li>
                        <li>To send important service notifications</li>
                        <li>To improve and personalize your experience</li>
                        <li>To respond to your inquiries and support requests</li>
                    </ul>
                </section>

                <section class="mb-8">
                    <h2>Data Security</h2>
                    <p>
                        We implement industry-standard security measures to
                        protect your data, including:
                    </p>
                    <ul>
                        <li>Encryption of data in transit (HTTPS/TLS)</li>
                        <li>Encryption of sensitive data at rest</li>
                        <li>Secure authentication with JWT tokens</li>
                        <li>Regular security audits and updates</li>
                    </ul>
                </section>

                <section class="mb-8">
                    <h2>Data Sharing</h2>
                    <p>
                        We do not sell your personal information. We may share
                        data only in the following circumstances:
                    </p>
                    <ul>
                        <li>
                            With AI providers (OpenAI, Google) when you use AI
                            features, using your own API keys
                        </li>
                        <li>
                            When you explicitly share content via share links
                        </li>
                        <li>To comply with legal obligations</li>
                        <li>To protect our rights and prevent fraud</li>
                    </ul>
                </section>

                <section class="mb-8">
                    <h2>Your Rights</h2>
                    <p>You have the right to:</p>
                    <ul>
                        <li>Access your personal data</li>
                        <li>Correct inaccurate data</li>
                        <li>Delete your account and associated data</li>
                        <li>Export your content</li>
                        <li>Withdraw consent for optional processing</li>
                    </ul>
                </section>

                <section class="mb-8">
                    <h2>Cookies</h2>
                    <p>
                        We use essential cookies to maintain your session and
                        preferences. We do not use tracking cookies or
                        third-party advertising cookies.
                    </p>
                </section>

                <section class="mb-8">
                    <h2>Data Retention</h2>
                    <p>
                        We retain your data for as long as your account is
                        active. When you delete your account, we remove your
                        personal data within 30 days, except where we are
                        required to retain it for legal purposes.
                    </p>
                </section>

                <section class="mb-8">
                    <h2>Contact Us</h2>
                    <p>
                        If you have questions about this Privacy Policy or our
                        data practices, please contact us at
                        <a href="mailto:privacy@doccoon.com" class="text-primary"
                            >privacy@doccoon.com</a
                        >.
                    </p>
                </section>

                <section>
                    <h2>Changes to This Policy</h2>
                    <p>
                        We may update this Privacy Policy from time to time. We
                        will notify you of significant changes by email or
                        through the service.
                    </p>
                </section>
            </div>
        </main>

        <!-- Footer -->
        <footer
            class="border-t border-[var(--border-color)] py-6 px-8 text-center"
        >
            <p class="text-sm text-[var(--text-color)] opacity-50">
                &copy; {{ new Date().getFullYear() }} Doccoon. All rights
                reserved.
            </p>
        </footer>
    </div>
</template>

<script setup lang="ts">
import { useTheme } from "@/composables/useTheme";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import logoLight from "@/assets/logo-light.png";
import logoDark from "@/assets/logo-dark.png";

const { isDarkTheme, toggleTheme } = useTheme();

const lastUpdated = new Date().toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
});
</script>

<style scoped>
.prose {
    color: var(--text-color);
    line-height: 1.7;
}

.prose h2 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    color: var(--text-color);
}

.prose h3 {
    font-size: 1rem;
    font-weight: 600;
    margin-top: 1.25rem;
    margin-bottom: 0.5rem;
    color: var(--text-color);
}

.prose p {
    margin-bottom: 1rem;
    opacity: 0.8;
}

.prose ul {
    margin-bottom: 1rem;
    padding-left: 1.5rem;
    opacity: 0.8;
}

.prose li {
    margin-bottom: 0.5rem;
}

.prose a {
    text-decoration: none;
}

.prose a:hover {
    text-decoration: underline;
}
</style>
