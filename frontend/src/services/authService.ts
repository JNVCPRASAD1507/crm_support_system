import api from "../api/axios";
import type {
  ChangePasswordRequest,
  LoginRequest,
  Profile,
  ProfileUpdateRequest,
  RegisterRequest,
  TokenResponse,
} from "../types/auth";

const authService = {
  async register(data: RegisterRequest): Promise<Profile> {
    const response = await api.post<Profile>(
      "/auth/register",
      data,
    );

    return response.data;
  },

  async login(data: LoginRequest): Promise<TokenResponse> {
    const response = await api.post<TokenResponse>(
      "/auth/login",
      data,
    );

    return response.data;
  },

  async getProfile(): Promise<Profile> {
    const response = await api.get<Profile>(
      "/auth/profile",
    );

    return response.data;
  },

  async updateProfile(
    data: ProfileUpdateRequest,
  ): Promise<Profile> {
    const response = await api.put<Profile>(
      "/auth/profile",
      data,
    );

    return response.data;
  },

  async changePassword(
    data: ChangePasswordRequest,
  ): Promise<{ message: string }> {
    const response = await api.put<{ message: string }>(
      "/auth/change-password",
      data,
    );

    return response.data;
  },
};

export default authService;