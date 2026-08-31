import React,{ useEffect, useState } from "react";
import { dashboard } from "../api";
import { useAuth } from "../context/AuthContext";
import StatCard from "../components/StatCard";
import {
  Ticket,
  Users,
  AlertTriangle,
  CheckCircle,
  Clock,
  ShieldAlert,
} from "lucide-react";
import SpotlightCard from "../components/SpotlightCard";
export default function Dashboard() {
  const { user } = useAuth();
  const [d, setD] = useState({});
  useEffect(() => {
    dashboard[
      user.role === "admin"
        ? "admin"
        : user.role === "support_agent"
          ? "agent"
          : "customer"
    ]().then((r) => setD(r.data));
  }, [user]);
  const cards = [
    ["Total tickets", d.total_tickets, Ticket],
    ["Open", d.open_tickets, Clock],
    ["In progress", d.in_progress_tickets, AlertTriangle],
    ["Resolved", d.resolved_tickets, CheckCircle],
    ["Critical", d.critical_tickets, ShieldAlert],
    ["SLA breached", d.sla_breached_tickets, AlertTriangle],
  ];
  return (
    <>
      <div className="page-intro">
        <div>
          <h2>Good morning, {user.full_name.split(" ")[0]}.</h2>
          <p>Here’s what is happening across your support queue.</p>
        </div>
        <span className="date-pill">Today · Operations</span>
      </div>
      <div className="stats">
        {cards.map(([l, v, I]) => (
          <StatCard key={l} label={l} value={v} icon={I} />
        ))}
      </div>
      {user.role === "admin" && (
        <div className="grid-2">
          <SpotlightCard>
            <div className="section-title">
              <div>
                <h3>Workspace overview</h3>
                <p>People and workload at a glance.</p>
              </div>
            </div>
            <div className="overview">
              <div>
                <b>{d.total_customers || 0}</b>
                <span>Customers</span>
              </div>
              <div>
                <b>{d.total_support_agents || 0}</b>
                <span>Support agents</span>
              </div>
              <div>
                <b>{d.total_tickets || 0}</b>
                <span>All tickets</span>
              </div>
            </div>
          </SpotlightCard>
          <SpotlightCard>
            <h3>Service health</h3>
            <p className="muted">
              SLA policies are monitored continuously in the backend.
            </p>
            <div className="health">
              <span></span>
              <b>Monitoring active</b>
              <small>Low 48h · Medium 24h · High 8h · Critical 2h</small>
            </div>
          </SpotlightCard>
        </div>
      )}
    </>
  );
}
