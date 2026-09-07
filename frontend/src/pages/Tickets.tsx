import { FormEvent, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import ticketService from "../services/ticketService";
import type { Ticket } from "../types/ticket";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function Tickets() {
  const { user } = useAuth();
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");
  const [search, setSearch] = useState("");
  const [showCreate, setShowCreate] = useState(false);

  const [form, setForm] = useState({
    customer_id: "",
    category_id: "",
    subject: "",
    description: "",
    priority: "medium",
  });

  const loadTickets = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await ticketService.list({
        status: statusFilter || undefined,
        priority: priorityFilter || undefined,
        search: search || undefined,
        limit: 50,
      });
      setTickets(data.items);
      setTotal(data.total);
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(typeof message === "string" ? message : "Failed to load tickets.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTickets();
  }, [statusFilter, priorityFilter]);

  const handleSearch = (e: FormEvent) => {
    e.preventDefault();
    loadTickets();
  };

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault();
    try {
      setError("");
      await ticketService.create({
        customer_id: Number(form.customer_id),
        category_id: form.category_id ? Number(form.category_id) : null,
        subject: form.subject,
        description: form.description,
        priority: form.priority,
      });
      setShowCreate(false);
      setForm({
        customer_id: "",
        category_id: "",
        subject: "",
        description: "",
        priority: "medium",
      });
      loadTickets();
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(typeof message === "string" ? message : "Failed to create ticket.");
    }
  };

  return (
    <div>
      <Navbar />
      <div className="app-layout">
        <Sidebar />
        <main className="page-content">
          <h1>Tickets</h1>
          <p>Total: {total}</p>

          {error && <p style={{ color: "crimson" }}>{error}</p>}

          <div style={{ display: "flex", gap: 12, marginBottom: 16, flexWrap: "wrap" }}>
            <form onSubmit={handleSearch} style={{ display: "flex", gap: 8 }}>
              <input
                placeholder="Search..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
              <button type="submit">Search</button>
            </form>

            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="">All Status</option>
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>

            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
            >
              <option value="">All Priority</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>

            <button type="button" onClick={() => setShowCreate(!showCreate)}>
              {showCreate ? "Cancel" : "New Ticket"}
            </button>
          </div>

          {showCreate && (
            <form
              onSubmit={handleCreate}
              style={{
                border: "1px solid var(--border)",
                padding: 16,
                marginBottom: 24,
                borderRadius: 8,
              }}
            >
              <h3>Create Ticket</h3>
              <div style={{ display: "grid", gap: 8, maxWidth: 480 }}>
                <label>
                  Customer ID
                  <input
                    type="number"
                    required
                    value={form.customer_id}
                    onChange={(e) =>
                      setForm({ ...form, customer_id: e.target.value })
                    }
                  />
                </label>
                <label>
                  Category ID (optional)
                  <input
                    type="number"
                    value={form.category_id}
                    onChange={(e) =>
                      setForm({ ...form, category_id: e.target.value })
                    }
                  />
                </label>
                <label>
                  Subject
                  <input
                    required
                    minLength={3}
                    value={form.subject}
                    onChange={(e) =>
                      setForm({ ...form, subject: e.target.value })
                    }
                  />
                </label>
                <label>
                  Description
                  <textarea
                    required
                    minLength={5}
                    rows={4}
                    value={form.description}
                    onChange={(e) =>
                      setForm({ ...form, description: e.target.value })
                    }
                  />
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
                <button type="submit">Create</button>
              </div>
            </form>
          )}

          {loading ? (
            <p>Loading tickets...</p>
          ) : tickets.length === 0 ? (
            <p>No tickets found.</p>
          ) : (
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
              }}
            >
              <thead>
                <tr style={{ textAlign: "left", borderBottom: "1px solid var(--border)" }}>
                  <th style={{ padding: 8 }}>ID</th>
                  <th style={{ padding: 8 }}>Subject</th>
                  <th style={{ padding: 8 }}>Status</th>
                  <th style={{ padding: 8 }}>Priority</th>
                  <th style={{ padding: 8 }}>Customer</th>
                  <th style={{ padding: 8 }}>Created</th>
                  <th style={{ padding: 8 }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {tickets.map((t) => (
                  <tr key={t.id} style={{ borderBottom: "1px solid var(--border)" }}>
                    <td style={{ padding: 8 }}>{t.id}</td>
                    <td style={{ padding: 8 }}>{t.subject}</td>
                    <td style={{ padding: 8 }}>{t.status}</td>
                    <td style={{ padding: 8 }}>{t.priority}</td>
                    <td style={{ padding: 8 }}>{t.customer_id}</td>
                    <td style={{ padding: 8 }}>
                      {new Date(t.created_at).toLocaleString()}
                    </td>
                    <td style={{ padding: 8 }}>
                      <Link to={`/tickets/${t.id}`}>View</Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </main>
      </div>
    </div>
  );
}

export default Tickets;
