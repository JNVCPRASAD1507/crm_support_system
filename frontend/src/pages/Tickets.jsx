
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { tickets } from "../api";
import StatusBadge from "../components/StatusBadge";
import Modal from "../components/Modal";
import {
  Plus,
  Search,
  Ticket as TicketIcon,
  ChevronRight,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Tickets() {
  const { user } = useAuth();

  const [data, setData] = useState({
    items: [],
    total: 0,
  });

  const [search, setSearch] = useState("");
  const [open, setOpen] = useState(false);

  const [form, setForm] = useState({
    subject: "",
    description: "",
    priority: "medium",
  });

  const load = async () => {
    try {
      const response = await tickets.list({
        search: search || undefined,
        page: 1,
        limit: 20,
      });

      setData(response.data);
    } catch (error) {
      console.error("Failed to load tickets:", error);
    }
  };

  useEffect(() => {
    load();
  }, [search]);

  const create = async (e) => {
    e.preventDefault();

    try {
      await tickets.create(form);

      setOpen(false);

      setForm({
        subject: "",
        description: "",
        priority: "medium",
      });

      load();
    } catch (error) {
      console.error("Failed to create ticket:", error);
    }
  };

  return (
    <>
      <div className="page-intro">
        <div>
          <h2>Tickets</h2>
          <p>{data.total || 0} conversations in your queue.</p>
        </div>

        <button className="primary" onClick={() => setOpen(true)}>
          <Plus size={17} />
          New ticket
        </button>
      </div>

      <div className="toolbar">
        <div className="search">
          <Search size={17} />

          <input
            placeholder="Search subject or description…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div className="filters">
          <span>All</span>
          <span>Open</span>
          <span>Critical</span>
        </div>
      </div>

      <div className="table-card">
        <table>
          <thead>
            <tr>
              <th>Ticket</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Customer</th>
              <th>Updated</th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            {data.items.map((t) => (
              <tr key={t.id}>
                <td>
                  <Link
                    className="ticket-link"
                    to={`/tickets/${t.id}`}
                  >
                    <span className="ticket-number">
                      #{String(t.id).padStart(4, "0")}
                    </span>

                    <b>{t.subject}</b>
                  </Link>
                </td>

                <td>
                  <StatusBadge value={t.priority} />
                </td>

                <td>
                  <StatusBadge value={t.status} />
                </td>

                <td>Customer #{t.customer_id}</td>

                <td>
                  {t.updated_at
                    ? new Date(t.updated_at).toLocaleDateString()
                    : "—"}
                </td>

                <td>
                  <ChevronRight size={17} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {!data.items.length && (
          <div className="empty">
            <TicketIcon size={30} />
            <b>No tickets found</b>
            <span>
              Try a different search or create a new ticket.
            </span>
          </div>
        )}
      </div>

      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Create support ticket"
      >
        <form onSubmit={create} className="form-grid">
          <label>
            Subject

            <input
              required
              value={form.subject}
              onChange={(e) =>
                setForm({
                  ...form,
                  subject: e.target.value,
                })
              }
            />
          </label>

          <label>
            Priority

            <select
              value={form.priority}
              onChange={(e) =>
                setForm({
                  ...form,
                  priority: e.target.value,
                })
              }
            >
              {["low", "medium", "high", "critical"].map((x) => (
                <option key={x} value={x}>
                  {x}
                </option>
              ))}
            </select>
          </label>

          <label className="full">
            Description

            <textarea
              required
              rows="5"
              value={form.description}
              onChange={(e) =>
                setForm({
                  ...form,
                  description: e.target.value,
                })
              }
            />
          </label>

          <button className="primary full">
            Create ticket
          </button>
        </form>
      </Modal>
    </>
  );
}
