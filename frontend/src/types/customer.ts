export interface Customer {
  id: number;
  name: string;
  email: string;
  phone: string | null;
  company: string | null;
  address: string | null;
  status: string;
  created_at: string;
  user_id?: number | null;
}

export interface CustomerCreateRequest {
  name: string;
  email: string;
  phone?: string | null;
  company?: string | null;
  address?: string | null;
  status?: string;
}

export interface CustomerUpdateRequest {
  name?: string;
  email?: string;
  phone?: string | null;
  company?: string | null;
  address?: string | null;
  status?: string;
}