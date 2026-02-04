<template>
  <BaseModal
    :visible="visible"
    :title="title ?? 'Select Page'"
    size="md"
    @close="cancel"
  >
    <p class="m-0 mb-6 text-[var(--text-color)] opacity-80 text-sm leading-relaxed">
      {{ message ?? 'Choose which page to view:' }}
    </p>

    <div class="flex gap-4 justify-center">
      <button
        class="flex-1 flex flex-col items-center gap-3 py-6 px-4 bg-transparent border-2 border-[var(--border-color)] rounded-lg cursor-pointer transition-all duration-200 text-[var(--text-color)] hover:border-primary hover:bg-[rgba(0,122,204,0.05)] hover:-translate-y-0.5 hover:shadow-[0_4px_12px_rgba(0,122,204,0.15)] active:translate-y-0"
        @click="selectLeft"
      >
        <div class="w-[60px] h-[60px] flex items-center justify-center bg-[var(--border-color)] rounded-md transition-all duration-200">
          <BaseIcon name="page-doc" :size="24" />
        </div>
        <span class="text-base font-semibold">Left Page</span>
        <span class="text-xs opacity-60">Current left content</span>
      </button>

      <button
        class="flex-1 flex flex-col items-center gap-3 py-6 px-4 bg-transparent border-2 border-[var(--border-color)] rounded-lg cursor-pointer transition-all duration-200 text-[var(--text-color)] hover:border-primary hover:bg-[rgba(0,122,204,0.05)] hover:-translate-y-0.5 hover:shadow-[0_4px_12px_rgba(0,122,204,0.15)] active:translate-y-0"
        @click="selectRight"
      >
        <div class="w-[60px] h-[60px] flex items-center justify-center bg-[var(--border-color)] rounded-md transition-all duration-200">
          <BaseIcon name="page-doc" :size="24" />
        </div>
        <span class="text-base font-semibold">Right Page</span>
        <span class="text-xs opacity-60">Current right content</span>
      </button>
    </div>

    <template #footer>
      <BaseButton variant="secondary" size="sm" @click="cancel">
        Cancel
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
import BaseModal from '@/components/ui/BaseModal.vue';
import BaseButton from '@/components/ui/BaseButton.vue';
import BaseIcon from '@/components/ui/BaseIcon.vue';

defineProps<{
  visible: boolean;
  title?: string;
  message?: string;
}>();

const emit = defineEmits<{
  'select-left': [];
  'select-right': [];
  'cancel': [];
}>();

function selectLeft() {
  emit('select-left');
}

function selectRight() {
  emit('select-right');
}

function cancel() {
  emit('cancel');
}
</script>
