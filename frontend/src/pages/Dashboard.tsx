
import {
  useEffect,
  useState,
} from "react";

import dashboardService from "../services/dashboardService";

import type {
  DashboardResponse,
} from "../types/dashboard";

import { useAuth } from "../context/AuthContext";

function Dashboard() {
  const { user, logout } = useAuth();

  const [dashboard, setDashboard] =
    useState<DashboardResponse | null>(
      null,
    );

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {
    const loadDashboard =
      async () => {
        try {
          setLoading(true);
          setError("");

          const data =
            await dashboardService.getDashboard();

          setDashboard(data);
        } catch (err: any) {
          const message =
            err?.response?.data?.detail;

          setError(
            typeof message === "string"
              ? message
              : "Failed to load dashboard.",
          );
        } finally {
          setLoading(false);
        }
      };

    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div>
        <h1>Dashboard</h1>
        <p>
          Loading dashboard...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <h1>Dashboard</h1>

        <p>
          {error}
        </p>

        <button
          onClick={() =>
            window.location.reload()
          }
        >
          Retry
        </button>
      </div>
    );
  }

  if (!dashboard) {
    return (
      <div>
        No dashboard data.
      </div>
    );
  }

  return (
    <div>
      <header>
        <div>
          <h1>
            Dashboard
          </h1>

          <p>
            Welcome,{" "}
            {user?.full_name}
          </p>

          <p>
            Role: {user?.role}
          </p>
        </div>

        <button
          onClick={logout}
        >
          Logout
        </button>
      </header>

      <hr />

      <section>
        <h2>
          Tickets
        </h2>

        <div>
          <div>
            <strong>
              Total Tickets
            </strong>

            <p>
              {dashboard.total_tickets}
            </p>
          </div>

          <div>
            <strong>
              Open
            </strong>

            <p>
              {dashboard.open_tickets}
            </p>
          </div>

          <div>
            <strong>
              In Progress
            </strong>

            <p>
              {dashboard.in_progress_tickets}
            </p>
          </div>

          <div>
            <strong>
              Resolved
            </strong>

            <p>
              {dashboard.resolved_tickets}
            </p>
          </div>

          <div>
            <strong>
              Closed
            </strong>

            <p>
              {dashboard.closed_tickets}
            </p>
          </div>
        </div>
      </section>

      <hr />

      <section>
        <h2>
          Priority
        </h2>

        <div>
          <div>
            <strong>
              High Priority
            </strong>

            <p>
              {dashboard.high_priority_tickets}
            </p>
          </div>

          <div>
            <strong>
              Critical Priority
            </strong>

            <p>
              {dashboard.critical_priority_tickets}
            </p>
          </div>

          <div>
            <strong>
              Unassigned
            </strong>

            <p>
              {dashboard.unassigned_tickets}
            </p>
          </div>
        </div>
      </section>

      <hr />

      <section>
        <h2>
          Customers
        </h2>

        <div>
          <div>
            <strong>
              Total Customers
            </strong>

            <p>
              {dashboard.total_customers}
            </p>
          </div>

          <div>
            <strong>
              Active Customers
            </strong>

            <p>
              {dashboard.active_customers}
            </p>
          </div>
        </div>
      </section>

      <hr />

      <section>
        <h2>
          Support Agents
        </h2>

        <div>
          <div>
            <strong>
              Total Agents
            </strong>

            <p>
              {dashboard.total_agents}
            </p>
          </div>

          <div>
            <strong>
              Active Agents
            </strong>

            <p>
              {dashboard.active_agents}
            </p>
          </div>
        </div>
      </section>

      <hr />

      <section>
        <h2>
          SLA
        </h2>

        <div>
          <div>
            <strong>
              SLA Breached
            </strong>

            <p>
              {dashboard.sla_breached}
            </p>
          </div>

          <div>
            <strong>
              SLA Pending
            </strong>

            <p>
              {dashboard.sla_pending}
            </p>
          </div>

          <div>
            <strong>
              First Response Pending
            </strong>

            <p>
              {dashboard.first_response_pending}
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;

