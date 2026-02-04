export interface ModalOptions {
  title: string;
  message: string;
  isDanger?: boolean;
}

export interface ModalState {
  visible: boolean;
  title: string;
  message: string;
  isDanger: boolean;
  resolve: ((value: boolean) => void) | null;
}

