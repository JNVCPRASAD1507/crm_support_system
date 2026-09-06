export interface Ticket {
  id: number;
  customer_id: number;
  assigned_agent_id: number | null;
  category_id: number | null;
  subject: string;
  description: string;
  priority: string;
  status: string;
  created_at: string;
  updated_at: string;
  resolved_at: string | null;
  sla_deadline: string | null;
  first_response_at: string | null;
}

export interface TicketListResponse {
  items: Ticket[];
  total: number;
  skip: number;
  limit: number;
  page: number;
  pages: number;
}

export interface TicketCreateRequest {
  customer_id: number;
  category_id?: number | null;
  subject: string;
  description: string;
  priority?: string;
}

export interface TicketUpdateRequest {
  category_id?: number | null;
  assigned_agent_id?: number | null;
  subject?: string;
  description?: string;
  priority?: string;
  status?: string;
}
