export interface Spread {
  left: string;
  right: string;
  leftWidth: string;
  rightWidth: string;
}

export interface Book {
  filename: string;
  spreads: Spread[];
}

export interface AppState {
  book: Book;
  currentSpreadIndex: number;
  isViewMode: boolean;
  isDarkTheme: boolean;
  isSaving: boolean;
}

