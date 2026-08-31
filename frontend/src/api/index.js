import api from "./client";
export const auth = {
  login: (d) => api.post("/auth/login", d),
  register: (d) => api.post("/auth/register", d),
  profile: () => api.get("/auth/profile"),
};
export const dashboard = {
  admin: () => api.get("/dashboard/admin"),
  agent: () => api.get("/dashboard/agent"),
  customer: () => api.get("/dashboard/customer"),
};
export const tickets = {
  list: (p) => api.get("/tickets", { params: p }),
  get: (id) => api.get(`/tickets/${id}`),
  create: (d) => api.post("/tickets", d),
  update: (id, d) => api.put(`/tickets/${id}`, d),
  assign: (id, d) => api.put(`/tickets/${id}/assign`, d),
  comments: (id) => api.get(`/tickets/${id}/comments`),
  addComment: (id, d) => api.post(`/tickets/${id}/comments`, d),
};
export const customers = {
  list: (p) => api.get("/customers", { params: p }),
  create: (d) => api.post("/customers", d),
  update: (id, d) => api.put(`/customers/${id}`, d),
  tickets: (id) => api.get(`/customers/${id}/tickets`),
};
export const categories = {
  list: () => api.get("/categories"),
  create: (d) => api.post("/categories", d),
};
export const agents = { list: () => api.get("/users/agents") };
export const notifications = {
  list: () => api.get("/notifications"),
  read: (id) => api.put(`/notifications/${id}/read`),
  readAll: () => api.put("/notifications/read-all"),
};
export default api;
