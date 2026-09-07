import { FormEvent, useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import ticketService from "../services/ticketService";
import type { Ticket } from "../types/ticket";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function TicketDetails() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({
    subject: "",
    description: "",
    priority: "",
    status: "",
    assigned_agent_id: "",
    category_id: "",
  });

  const loadTicket = async () => {
    if (!id) return;
    try {
      setLoading(true);
      setError("");
      const data = await ticketService.getById(Number(id));
      setTicket(data);
      setForm({
        subject: data.subject,
        description: data.description,
        priority: data.priority,
        status: data.status,
        assigned_agent_id: data.assigned_agent_id?.toString() || "",
        category_id: data.category_id?.toString() || "",
      });
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(typeof message === "string" ? message : "Failed to load ticket.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTicket();
  }, [id]);

  const handleUpdate = async (e: FormEvent) => {
    e.preventDefault();
    if (!id) return;
    try {
      setError("");
      const updated = await ticketService.update(Number(id), {
        subject: form.subject || undefined,
        description: form.description || undefined,
        priority: form.priority || undefined,
        status: form.status || undefined,
        assigned_agent_id: form.assigned_agent_id
          ? Number(form.assigned_agent_id)
          : null,
        category_id: form.category_id ? Number(form.category_id) : null,
      });
      setTicket(updated);
      setEditing(false);
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(typeof message === "string" ? message : "Failed to update ticket.");
    }
  };

  const handleDelete = async () => {
    if (!id || !window.confirm("Delete this ticket?")) return;
    try {
      await ticketService.delete(Number(id));
      navigate("/tickets");
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(typeof message === "string" ? message : "Failed to delete ticket.");
    }
  };

  const canEdit =
    user?.role === "admin" || user?.role === "support_agent";

  if (loading) {
    return (
      <div>
        <Navbar />
        <p style={{ padding: 24 }}>Loading ticket...</p>
      </div>
    );
  }

  if (error && !ticket) {
    return (
      <div>
        <Navbar />
        <div style={{ padding: 24 }}>
          <p style={{ color: "crimson" }}>{error}</p>
          <Link to="/tickets">Back to tickets</Link>
        </div>
      </div>
    );
  }

  if (!ticket) {
    return (
      <div>
        <Navbar />
        <p style={{ padding: 24 }}>Ticket not found.</p>
      </div>
    );
  }

  return (
    <div>
      <Navbar />
      <div className="app-layout">
        <Sidebar />
        <main className="page-content">
          <p>
            <Link to="/tickets">← Back to Tickets</Link>
          </p>
          <h1>Ticket #{ticket.id}</h1>
          {error && <p style={{ color: "crimson" }}>{error}</p>}

          {!editing ? (
            <div>
              <p>
                <strong>Subject:</strong> {ticket.subject}
              </p>
              <p>
                <strong>Description:</strong>
              </p>
              <p style={{ whiteSpace: "pre-wrap" }}>{ticket.description}</p>
              <p>
                <strong>Status:</strong> {ticket.status}
              </p>
              <p>
                <strong>Priority:</strong> {ticket.priority}
              </p>
              <p>
                <strong>Customer ID:</strong> {ticket.customer_id}
              </p>
              <p>
                <strong>Assigned Agent:</strong>{" "}
                {ticket.assigned_agent_id ?? "Unassigned"}
              </p>
              <p>
                <strong>Category ID:</strong> {ticket.category_id ?? "—"}
              </p>
              <p>
                <strong>Created:</strong>{" "}
                {new Date(ticket.created_at).toLocaleString()}
              </p>
              <p>
                <strong>Updated:</strong>{" "}
                {new Date(ticket.updated_at).toLocaleString()}
              </p>
              {ticket.sla_deadline && (
                <p>
                  <strong>SLA Deadline:</strong>{" "}
                  {new Date(ticket.sla_deadline).toLocaleString()}
                </p>
              )}
              {ticket.resolved_at && (
                <p>
                  <strong>Resolved:</strong>{" "}
                  {new Date(ticket.resolved_at).toLocaleString()}
                </p>
              )}

              {canEdit && (
                <div style={{ marginTop: 16, display: "flex", gap: 8 }}>
                  <button type="button" onClick={() => setEditing(true)}>
                    Edit
                  </button>
                  {user?.role === "admin" && (
                    <button type="button" onClick={handleDelete}>
                      Delete
                    </button>
                  )}
                </div>
              )}
            </div>
          ) : (
            <form onSubmit={handleUpdate} style={{ maxWidth: 480 }}>
              <div style={{ display: "grid", gap: 8 }}>
                <label>
                  Subject
                  <input
                    value={form.subject}
                    onChange={(e) =>
                      setForm({ ...form, subject: e.target.value })
                    }
                    required
                    minLength={3}
                  />
                </label>
                <label>
                  Description
                  <textarea
                    rows={5}
                    value={form.description}
                    onChange={(e) =>
                      setForm({ ...form, description: e.target.value })
                    }
                    required
                    minLength={5}
                  />
                </label>
                <label>
                  Status
                  <select
                    value={form.status}
                    onChange={(e) =>
                      setForm({ ...form, status: e.target.value })
                    }
                  >
                    <option value="open">Open</option>
                    <option value="in_progress">In Progress</option>
                    <option value="resolved">Resolved</option>
                    <option value="closed">Closed</option>
                  </select>
                </label>
                <label>
                  Priority
                  <select
                    value={form.priority}
                    onChange={(e) =>
                      setForm({ ...form, priority: e.target.value })
                    }
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="critical">Critical</option>
                  </select>
                </label>
                <label>
                  Assigned Agent ID
                  <input
                    type="number"
                    value={form.assigned_agent_id}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        assigned_agent_id: e.target.value,
                      })
                    }
                  />
                </label>
                <label>
                  Category ID
                  <input
                    type="number"
                    value={form.category_id}
                    onChange={(e) =>
                      setForm({ ...form, category_id: e.target.value })
                    }
                  />
                </label>
                <div style={{ display: "flex", gap: 8 }}>
                  <button type="submit">Save</button>
                  <button type="button" onClick={() => setEditing(false)}>
                    Cancel
                  </button>
                </div>
              </div>
            </form>
          )}
        </main>
      </div>
    </div>
  );
}

export default TicketDetails;
