import { reactive } from 'vue';
import type { ModalOptions, ModalState } from '@/types';

export function useModal() {
  const modalState = reactive<ModalState>({
    visible: false,
    title: '',
    message: '',
    isDanger: false,
    resolve: null
  });

  function showModal(options: ModalOptions): Promise<boolean> {
    return new Promise((resolve) => {
      modalState.visible = true;
      modalState.title = options.title;
      modalState.message = options.message;
      modalState.isDanger = options.isDanger || false;
      modalState.resolve = resolve;
    });
  }

  function confirm() {
    if (modalState.resolve) {
      modalState.resolve(true);
    }
    hideModal();
  }

  function cancel() {
    if (modalState.resolve) {
      modalState.resolve(false);
    }
    hideModal();
  }

  function hideModal() {
    modalState.visible = false;
    modalState.title = '';
    modalState.message = '';
    modalState.isDanger = false;
    modalState.resolve = null;
  }

  return {
    modalState,
    showModal,
    confirm,
    cancel
  };
}

