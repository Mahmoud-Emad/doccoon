import { api } from './client';
import type { AIProviderKey, AIProviderKeyCreate } from '@/types';

export async function getAIKeys(): Promise<AIProviderKey[]> {
  const response = await api.get<AIProviderKey[]>('/ai/keys/');
  return response.results ?? [];
}

export async function createAIKey(data: AIProviderKeyCreate): Promise<AIProviderKey> {
  const response = await api.post<AIProviderKey>('/ai/keys/', data);
  return response.results!;
}

export async function updateAIKey(
  id: number,
  data: Partial<AIProviderKeyCreate>,
): Promise<AIProviderKey> {
  const response = await api.put<AIProviderKey>(`/ai/keys/${id}/`, data);
  return response.results!;
}

export async function deleteAIKey(id: number): Promise<void> {
  await api.del(`/ai/keys/${id}/`);
}
