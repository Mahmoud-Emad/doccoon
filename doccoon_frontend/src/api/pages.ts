import { api } from "@/api/client";

export interface PageData {
  id: number;
  content: string;
  page_number: number;
  created_at: string;
  modified_at: string;
}

export interface CreatePagePayload {
  content: string;
}

export interface UpdatePagePayload {
  content?: string;
  page_number?: number;
}

export async function createPage(
  bookId: number,
  payload: CreatePagePayload,
): Promise<PageData | null> {
  const response = await api.post<PageData>(
    `/books/${bookId}/pages/`,
    payload,
  );
  return response.results ?? null;
}

export async function updatePage(
  bookId: number,
  pageId: number,
  payload: UpdatePagePayload,
): Promise<PageData | null> {
  const response = await api.put<PageData>(
    `/books/${bookId}/pages/${pageId}/`,
    payload,
  );
  return response.results ?? null;
}

export async function deletePage(
  bookId: number,
  pageId: number,
): Promise<boolean> {
  await api.del(`/books/${bookId}/pages/${pageId}/`);
  return true;
}
