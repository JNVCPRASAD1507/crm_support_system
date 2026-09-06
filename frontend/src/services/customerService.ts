import api from "../api/axios";

import type {
  Customer,
  CustomerListResponse,
} from "../types/customer";

export interface CustomerListParams {
  skip?: number;
  limit?: number;
  search?: string;
  status?: string;
}

export interface CustomerCreateRequest {
  user_id: number;
  phone?: string;
  address?: string;
  status?: string;
}

export interface CustomerUpdateRequest {
  phone?: string;
  address?: string;
  status?: string;
}

const customerService = {
  async list(
    params?: CustomerListParams,
  ): Promise<CustomerListResponse> {
    const response =
      await api.get<CustomerListResponse>(
        "/customers",
        {
          params,
        },
      );

    return response.data;
  },

  async getById(
    customerId: number,
  ): Promise<Customer> {
    const response =
      await api.get<Customer>(
        `/customers/${customerId}`,
      );

    return response.data;
  },

  async getMe(): Promise<Customer> {
    const response =
      await api.get<Customer>(
        "/customers/me",
      );

    return response.data;
  },

  async create(
    data: CustomerCreateRequest,
  ): Promise<Customer> {
    const response =
      await api.post<Customer>(
        "/customers",
        data,
      );

    return response.data;
  },

  async update(
    customerId: number,
    data: CustomerUpdateRequest,
  ): Promise<Customer> {
    const response =
      await api.put<Customer>(
        `/customers/${customerId}`,
        data,
      );

    return response.data;
  },

  async delete(
    customerId: number,
  ): Promise<void> {
    await api.delete(
      `/customers/${customerId}`,
    );
  },
};

export default customerService;

