import { api } from "@/api/client";

export interface ShareResponse {
  id: number;
  share_token: string;
  is_active: boolean;
  created_at: string;
}

export interface SharedPageData {
  id: number;
  content: string;
  page_number: number;
  book_title: string;
  book_is_public: boolean;
  created_at: string;
  modified_at: string;
}

export interface SharedBookData {
  id: number;
  title: string;
  description: string;
  year: number;
  status: string;
  pages: { id: number; content: string; page_number: number }[];
}

export async function sharePage(
  bookId: number,
  pageId: number,
): Promise<ShareResponse | null> {
  const response = await api.post<ShareResponse>(
    `/books/${bookId}/pages/${pageId}/share/`,
  );
  return response.results ?? null;
}

export async function unsharePage(
  bookId: number,
  pageId: number,
): Promise<boolean> {
  await api.del(`/books/${bookId}/pages/${pageId}/share/`);
  return true;
}

export async function getSharedPage(
  token: string,
): Promise<SharedPageData | null> {
  const response = await api.get<SharedPageData>(`/shared/page/${token}/`);
  return response.results ?? null;
}

export async function shareBook(
  bookId: number,
): Promise<ShareResponse | null> {
  const response = await api.post<ShareResponse>(`/books/${bookId}/share/`);
  return response.results ?? null;
}

export async function unshareBook(bookId: number): Promise<boolean> {
  await api.del(`/books/${bookId}/share/`);
  return true;
}

export async function getSharedBook(
  token: string,
): Promise<SharedBookData | null> {
  const response = await api.get<SharedBookData>(`/shared/book/${token}/`);
  return response.results ?? null;
}
