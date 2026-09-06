export interface Customer {
  id: number;
  user_id: number;
  phone: string | null;
  address: string | null;
  status: string;
  created_at: string;
  updated_at: string | null;
}

export interface CustomerListResponse {
  items: Customer[];
  total: number;
  skip: number;
  limit: number;
  page: number;
  pages: number;
}

