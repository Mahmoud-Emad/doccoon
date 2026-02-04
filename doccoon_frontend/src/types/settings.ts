export interface UserSettings {
  id: number;
  auto_save_enabled: boolean;
  auto_save_interval: number;
  notification_enabled: boolean;
  theme: "light" | "dark";
  profile_visible: boolean;
  view_mode: boolean;
  layout_mode: "book" | "page";
  live_preview: boolean;
}

export interface AIProviderKey {
  id: number;
  provider: string;
  label: string;
  masked_key: string;
  model: string;
  is_active: boolean;
  created_at: string;
}

export interface AIProviderKeyCreate {
  provider: string;
  label: string;
  api_key: string;
  model: string;
  is_active?: boolean;
}

export interface Notification {
  id: number;
  notification_type: string;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
}

export interface UserProfile {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  full_name: string;
  has_password: boolean;
}

export interface UserProfileUpdate {
  first_name: string;
  last_name: string;
}
