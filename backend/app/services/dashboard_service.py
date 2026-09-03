from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.dashboard import DashboardResponse


class DashboardService:

    def __init__(self, db):
        self.repository = DashboardRepository(db)

    def get_dashboard(self) -> DashboardResponse:
        return DashboardResponse(
            total_tickets=self.repository.get_total_tickets(),

            open_tickets=self.repository.get_tickets_by_status(
                "open"
            ),

            in_progress_tickets=self.repository.get_tickets_by_status(
                "in_progress"
            ),

            resolved_tickets=self.repository.get_tickets_by_status(
                "resolved"
            ),

            closed_tickets=self.repository.get_tickets_by_status(
                "closed"
            ),

            high_priority_tickets=self.repository.get_tickets_by_priority(
                "high"
            ),

            critical_priority_tickets=self.repository.get_tickets_by_priority(
                "critical"
            ),

            unassigned_tickets=self.repository.get_unassigned_tickets(),

            total_customers=self.repository.get_total_customers(),

            active_customers=self.repository.get_active_customers(),

            total_agents=self.repository.get_total_agents(),

            active_agents=self.repository.get_active_agents(),

            sla_breached=self.repository.get_sla_breached(),

            sla_pending=self.repository.get_sla_pending(),

            first_response_pending=self.repository.get_first_response_pending(),
        )