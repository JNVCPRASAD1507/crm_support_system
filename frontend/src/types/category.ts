export interface Category {
  id: number;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
}

export interface CategoryCreateRequest {
  name: string;
  description?: string | null;
  is_active?: boolean;
}

export interface CategoryUpdateRequest {
  name?: string;
  description?: string | null;
  is_active?: boolean;
}
