import { api } from "./client";
import type { UserSettings, UserProfile } from "@/types";

export async function getSettings(): Promise<UserSettings> {
  const response = await api.get<UserSettings>("/settings/");
  return response.results!;
}

export async function updateSettings(
  data: Partial<UserSettings>,
): Promise<UserSettings> {
  const response = await api.put<UserSettings>("/settings/", data);
  return response.results!;
}

export async function getUserProfile(): Promise<UserProfile> {
  const response = await api.get<UserProfile>("/auth/profile/");
  return response.results!;
}
