import { api } from './client';
import type { Notification } from '@/types';

export async function getNotifications(): Promise<Notification[]> {
  const response = await api.get<Notification[]>('/notifications/');
  return response.results ?? [];
}

export async function markAsRead(id: number): Promise<void> {
  await api.put(`/notifications/${id}/read/`);
}

export async function markAllAsRead(): Promise<void> {
  await api.put('/notifications/read-all/');
}

export async function deleteNotification(id: number): Promise<void> {
  await api.del(`/notifications/${id}/`);
}
