
import api from "../api/axios";

import type {
  DashboardResponse,
} from "../types/dashboard";

const dashboardService = {
  async getDashboard(): Promise<DashboardResponse> {
    const response =
      await api.get<DashboardResponse>(
        "/dashboard",
      );

    return response.data;
  },
};

export default dashboardService;

