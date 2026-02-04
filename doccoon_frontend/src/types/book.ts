export interface Spread {
  left: string;
  right: string;
  leftWidth: string;
  rightWidth: string;
  leftPageId?: number;
  rightPageId?: number;
}

export interface Book {
  id?: number;
  filename: string;
  status?: string;
  spreads: Spread[];
}

export interface AppState {
  book: Book;
  currentSpreadIndex: number;
  isViewMode: boolean;
  isDarkTheme: boolean;
  isSaving: boolean;
}

export interface BookSummary {
  id: number;
  title: string;
  description: string;
  year: number;
  status: string;
  page_count: number;
  image_count: number;
  book_size: number;
  created_at: string;
  modified_at: string;
}
