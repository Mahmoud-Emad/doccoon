<template>
  <BaseModal :visible="visible" :title="title" size="md" @close="onCancel">
    <p class="m-0 text-sm leading-relaxed text-[var(--text-color)]">
      {{ message }}
    </p>

    <template #footer>
      <BaseButton variant="secondary" size="sm" @click="onCancel">
        Cancel
      </BaseButton>
      <BaseButton
        :variant="isDanger ? 'danger' : 'primary'"
        size="sm"
        @click="onConfirm"
      >
        Confirm
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
import BaseModal from '@/components/ui/BaseModal.vue';
import BaseButton from '@/components/ui/BaseButton.vue';

defineProps<{
  visible: boolean;
  title: string;
  message: string;
  isDanger: boolean;
}>();

const emit = defineEmits<{
  confirm: [];
  cancel: [];
}>();

function onConfirm() {
  emit('confirm');
}

function onCancel() {
  emit('cancel');
}
</script>
