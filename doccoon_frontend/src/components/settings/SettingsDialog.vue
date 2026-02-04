<template>
  <BaseModal :visible="visible" size="lg" @close="$emit('update:visible', false)">
    <div class="flex min-h-[480px] max-h-[70vh] -m-6">
      <!-- Sidebar -->
      <nav class="w-48 shrink-0 border-r border-[var(--border-color)] bg-[var(--bg-color)] p-2 flex flex-col gap-0.5 rounded-l-lg">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          class="flex items-center gap-2.5 px-3 py-2 text-sm rounded-md cursor-pointer border-none transition-colors duration-150 text-left"
          :class="
            activeTab === tab.id
              ? 'bg-[var(--page-bg)] text-[var(--text-color)] font-medium'
              : 'bg-transparent text-[var(--text-color)] opacity-70 hover:bg-[var(--page-bg)] hover:opacity-100'
          "
          @click="activeTab = tab.id"
        >
          <BaseIcon :name="tab.icon" :size="16" />
          {{ tab.label }}
        </button>
      </nav>

      <!-- Content -->
      <div class="flex-1 overflow-y-auto p-6">
        <h2 class="text-lg font-semibold text-[var(--text-color)] mb-4">
          {{ currentTab?.label }}
        </h2>

        <GeneralTab v-if="activeTab === 'general'" />
        <PreferencesTab v-else-if="activeTab === 'preferences'" />
        <PrivacySecurityTab v-else-if="activeTab === 'privacy'" />
        <AIConfigTab v-else-if="activeTab === 'ai'" />
      </div>
    </div>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import BaseModal from '@/components/ui/BaseModal.vue';
import BaseIcon from '@/components/ui/BaseIcon.vue';
import GeneralTab from './GeneralTab.vue';
import PreferencesTab from './PreferencesTab.vue';
import PrivacySecurityTab from './PrivacySecurityTab.vue';
import AIConfigTab from './AIConfigTab.vue';

defineProps<{
  visible: boolean;
}>();

defineEmits<{
  'update:visible': [value: boolean];
}>();

const tabs = [
  { id: 'general', label: 'General', icon: 'user' },
  { id: 'preferences', label: 'Preferences', icon: 'palette' },
  { id: 'privacy', label: 'Privacy & Security', icon: 'shield' },
  { id: 'ai', label: 'AI Configuration', icon: 'cpu' },
] as const;

type TabId = (typeof tabs)[number]['id'];

const activeTab = ref<TabId>('general');

const currentTab = computed(() => tabs.find((t) => t.id === activeTab.value));
</script>
