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
                    Terms of Service
                </h1>
                <p class="text-sm text-[var(--text-color)] opacity-50">
                    Last updated: {{ lastUpdated }}
                </p>
            </div>

            <div class="prose">
                <section class="mb-8">
                    <h2>Agreement to Terms</h2>
                    <p>
                        By accessing or using Doccoon, you agree to be bound by
                        these Terms of Service. If you do not agree to these
                        terms, please do not use our service.
                    </p>
                </section>

                <section class="mb-8">
                    <h2>Description of Service</h2>
                    <p>
                        Doccoon is a markdown-based book editor that allows you
                        to create, edit, and organize content with features
                        including cloud sync, AI-powered writing assistance, and
                        content sharing.
                    </p>
                </section>

                <section class="mb-8">
                    <h2>User Accounts</h2>
                    <p>
                        To access certain features, you must create an account.
                        You are responsible for:
                    </p>
                    <ul>
                        <li>Maintaining the security of your account credentials</li>
                        <li>All activities that occur under your account</li>
                        <li>Providing accurate and complete information</li>
                        <li>Notifying us of any unauthorized access</li>
                    </ul>
                </section>

                <section class="mb-8">
                    <h2>Acceptable Use</h2>
                    <p>You agree not to use Doccoon to:</p>
                    <ul>
                        <li>Violate any applicable laws or regulations</li>
                        <li>Infringe on intellectual property rights</li>
                        <li>Transmit malicious code or harmful content</li>
                        <li>Attempt to gain unauthorized access to our systems</li>
                        <li>Interfere with the service or other users</li>
                        <li>Create content that is illegal, harmful, or offensive</li>
                    </ul>
                </section>

                <section class="mb-8">
                    <h2>Your Content</h2>
                    <p>
                        You retain ownership of all content you create in
                        Doccoon. By using our service, you grant us a limited
                        license to store, process, and display your content as
                        necessary to provide the service.
                    </p>
                    <p>
                        You are solely responsible for your content and ensuring
                        you have the rights to use and share it.
                    </p>
                </section>

                <section class="mb-8">
                    <h2>AI Features</h2>
                    <p>
                        When you use AI-powered features, your content may be
                        sent to third-party AI providers (OpenAI, Google) for
                        processing. You are responsible for:
                    </p>
                    <ul>
                        <li>Providing your own API keys for AI features</li>
                        <li>
                            Complying with the terms of service of AI providers
                        </li>
                        <li>
                            Understanding that AI-generated content may not be
                            accurate
                        </li>
                        <li>Reviewing and verifying AI-generated content</li>
                    </ul>
                </section>

                <section class="mb-8">
                    <h2>Sharing and Privacy</h2>
                    <p>
                        When you share content via share links, that content
                        becomes accessible to anyone with the link. You are
                        responsible for managing your share links and revoking
                        access when appropriate.
                    </p>
                </section>

                <section class="mb-8">
                    <h2>Intellectual Property</h2>
                    <p>
                        Doccoon and its original content, features, and
                        functionality are owned by us and are protected by
                        copyright, trademark, and other intellectual property
                        laws.
                    </p>
                </section>

                <section class="mb-8">
                    <h2>Disclaimer of Warranties</h2>
                    <p>
                        Doccoon is provided "as is" and "as available" without
                        warranties of any kind. We do not guarantee that the
                        service will be uninterrupted, secure, or error-free.
                    </p>
                </section>

                <section class="mb-8">
                    <h2>Limitation of Liability</h2>
                    <p>
                        To the maximum extent permitted by law, we shall not be
                        liable for any indirect, incidental, special,
                        consequential, or punitive damages, including loss of
                        data, profits, or business opportunities.
                    </p>
                </section>

                <section class="mb-8">
                    <h2>Termination</h2>
                    <p>
                        We may terminate or suspend your account at any time for
                        violations of these terms. You may also delete your
                        account at any time through your profile settings.
                    </p>
                </section>

                <section class="mb-8">
                    <h2>Changes to Terms</h2>
                    <p>
                        We may update these Terms of Service from time to time.
                        Continued use of the service after changes constitutes
                        acceptance of the new terms.
                    </p>
                </section>

                <section>
                    <h2>Contact Us</h2>
                    <p>
                        If you have questions about these Terms of Service,
                        please contact us at
                        <a href="mailto:legal@doccoon.com" class="text-primary"
                            >legal@doccoon.com</a
                        >.
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
