import { api } from "@/api/client";
import type { BookSummary } from "@/types";

export interface CreateBookPayload {
  title: string;
  description?: string;
  year?: number;
}

export interface UpdateBookPayload {
  title?: string;
  description?: string;
  year?: number;
}

export interface BookPage {
  id: number;
  content: string;
  page_number: number;
}

export interface BookInfo {
  id: number;
  title: string;
  description: string;
  year: number;
  status: string;
}

export interface BookDetail extends BookInfo {
  pages: BookPage[];
}

export async function getBooks(signal?: AbortSignal): Promise<BookSummary[]> {
  return api.getAllPaginated<BookSummary>("/books/", signal);
}

export async function getBook(bookId: number): Promise<BookDetail | null> {
  const response = await api.get<BookDetail>(`/books/${bookId}/`);
  return response.results ?? null;
}

export async function createBook(
  payload: CreateBookPayload,
): Promise<BookInfo | null> {
  const response = await api.post<BookInfo>("/books/", payload);
  return response.results ?? null;
}

export async function updateBook(
  bookId: number,
  payload: UpdateBookPayload,
): Promise<BookInfo | null> {
  const response = await api.put<BookInfo>(`/books/${bookId}/`, payload);
  return response.results ?? null;
}

export async function deleteBook(bookId: number): Promise<boolean> {
  await api.del(`/books/${bookId}/`);
  return true;
}

export async function togglePublishBook(
  bookId: number,
): Promise<BookInfo | null> {
  const response = await api.post<BookInfo>(`/books/${bookId}/publish/`);
  return response.results ?? null;
}
