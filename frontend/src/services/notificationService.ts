import api from "../api/axios";
import type { Notification } from "../types/notification";

const notificationService = {
  async list(): Promise<Notification[]> {
    const response = await api.get<Notification[]>("/notifications");
    return response.data;
  },

  async markRead(id: number): Promise<Notification> {
    const response = await api.put<Notification>(
      `/notifications/${id}/read`,
    );
    return response.data;
  },

  async markAllRead(): Promise<{ message: string }> {
    const response = await api.put<{ message: string }>(
      "/notifications/read-all",
    );
    return response.data;
  },
};

export default notificationService;
