import api from "../api/axios";

import type {
  SLA,
  SLACreateRequest,
  SLAUpdateRequest,
} from "../types/sla";

export interface SLAListParams {
  skip?: number;
  limit?: number;
  active_only?: boolean;
}

const slaService = {
  async list(params?: SLAListParams): Promise<SLA[]> {
    const response = await api.get<SLA[]>("/slas", {
      params,
    });
    return response.data;
  },

  async getById(slaId: number): Promise<SLA> {
    const response = await api.get<SLA>(`/slas/${slaId}`);
    return response.data;
  },

  async create(data: SLACreateRequest): Promise<SLA> {
    const response = await api.post<SLA>("/slas", data);
    return response.data;
  },

  async update(
    slaId: number,
    data: SLAUpdateRequest,
  ): Promise<SLA> {
    const response = await api.put<SLA>(
      `/slas/${slaId}`,
      data,
    );
    return response.data;
  },

  async delete(slaId: number): Promise<void> {
    await api.delete(`/slas/${slaId}`);
  },
};

export default slaService;
