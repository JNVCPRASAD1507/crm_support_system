import api from "../api/axios";

import type {
  Ticket,
  TicketCreateRequest,
  TicketListResponse,
  TicketUpdateRequest,
} from "../types/ticket";

export interface TicketListParams {
  skip?: number;
  limit?: number;
  status?: string;
  priority?: string;
  customer_id?: number;
  assigned_agent_id?: number;
  search?: string;
}

const ticketService = {
  async list(
    params?: TicketListParams,
  ): Promise<TicketListResponse> {
    const response = await api.get<TicketListResponse>(
      "/tickets",
      { params },
    );
    return response.data;
  },

  async getById(ticketId: number): Promise<Ticket> {
    const response = await api.get<Ticket>(
      `/tickets/${ticketId}`,
    );
    return response.data;
  },

  async create(data: TicketCreateRequest): Promise<Ticket> {
    const response = await api.post<Ticket>(
      "/tickets",
      data,
    );
    return response.data;
  },

  async update(
    ticketId: number,
    data: TicketUpdateRequest,
  ): Promise<Ticket> {
    const response = await api.put<Ticket>(
      `/tickets/${ticketId}`,
      data,
    );
    return response.data;
  },

  async delete(ticketId: number): Promise<void> {
    await api.delete(`/tickets/${ticketId}`);
  },
};

export default ticketService;
