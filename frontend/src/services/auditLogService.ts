import api from "../api/axios";
import type { AuditLog } from "../types/auditLog";

export interface AuditLogListParams {
  skip?: number;
  limit?: number;
  entity_type?: string;
  user_id?: number;
}

const auditLogService = {
  async list(params?: AuditLogListParams): Promise<AuditLog[]> {
    const response = await api.get<AuditLog[]>("/audit-logs", {
      params,
    });
    return response.data;
  },
};

export default auditLogService;
