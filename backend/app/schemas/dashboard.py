from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_tickets: int

    open_tickets: int
    in_progress_tickets: int
    resolved_tickets: int
    closed_tickets: int

    high_priority_tickets: int
    critical_priority_tickets: int

    unassigned_tickets: int

    total_customers: int
    active_customers: int

    total_agents: int
    active_agents: int

    sla_breached: int
    sla_pending: int

    first_response_pending: int