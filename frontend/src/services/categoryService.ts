import api from "../api/axios";

import type {
  Category,
  CategoryCreateRequest,
  CategoryUpdateRequest,
} from "../types/category";

export interface CategoryListParams {
  skip?: number;
  limit?: number;
  active_only?: boolean;
}

const categoryService = {
  async list(
    params?: CategoryListParams,
  ): Promise<Category[]> {
    const response = await api.get<Category[]>(
      "/categories",
      { params },
    );
    return response.data;
  },

  async getById(categoryId: number): Promise<Category> {
    const response = await api.get<Category>(
      `/categories/${categoryId}`,
    );
    return response.data;
  },

  async create(data: CategoryCreateRequest): Promise<Category> {
    const response = await api.post<Category>(
      "/categories",
      data,
    );
    return response.data;
  },

  async update(
    categoryId: number,
    data: CategoryUpdateRequest,
  ): Promise<Category> {
    const response = await api.put<Category>(
      `/categories/${categoryId}`,
      data,
    );
    return response.data;
  },

  async delete(categoryId: number): Promise<void> {
    await api.delete(`/categories/${categoryId}`);
  },
};

export default categoryService;
