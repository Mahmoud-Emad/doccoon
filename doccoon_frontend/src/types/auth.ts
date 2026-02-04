export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  email: string;
  full_name: string;
  first_name: string;
  last_name: string;
  id: number;
}

export interface SocialAuthRequest {
  access_token: string;
}
