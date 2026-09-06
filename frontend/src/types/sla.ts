export interface SLA {
  id: number;
  name: string;
  description: string | null;
  priority: string;
  response_time_minutes: number;
  resolution_time_minutes: number;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface SLACreateRequest {
  name: string;
  description?: string | null;
  priority: string;
  response_time_minutes: number;
  resolution_time_minutes: number;
  is_active?: boolean;
}

export interface SLAUpdateRequest {
  name?: string;
  description?: string | null;
  priority?: string;
  response_time_minutes?: number;
  resolution_time_minutes?: number;
  is_active?: boolean;
}
