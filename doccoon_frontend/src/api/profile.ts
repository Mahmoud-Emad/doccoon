import { api } from './client';
import type { UserProfile, UserProfileUpdate } from '@/types';

export async function getProfile(): Promise<UserProfile> {
  const response = await api.get<UserProfile>('/auth/profile/');
  return response.results!;
}

export async function updateProfile(data: UserProfileUpdate): Promise<UserProfile> {
  const response = await api.put<UserProfile>('/auth/profile/', data);
  return response.results!;
}
