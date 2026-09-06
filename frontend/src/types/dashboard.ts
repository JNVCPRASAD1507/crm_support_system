export interface DashboardResponse {
  total_tickets: number;

  open_tickets: number;
  in_progress_tickets: number;
  resolved_tickets: number;
  closed_tickets: number;

  high_priority_tickets: number;
  critical_priority_tickets: number;

  unassigned_tickets: number;

  total_customers: number;
  active_customers: number;

  total_agents: number;
  active_agents: number;

  sla_breached: number;
  sla_pending: number;

  first_response_pending: number;
}