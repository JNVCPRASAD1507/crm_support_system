import { FormEvent, useEffect, useState } from "react";
import slaService from "../services/slaService";
import type { SLA } from "../types/sla";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function SLAPage() {
  const [slas, setSlas] = useState<SLA[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState({
    name: "",
    description: "",
    priority: "medium",
    response_time_minutes: 60,
    resolution_time_minutes: 240,
    is_active: true,
  });

  const load = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await slaService.list({ limit: 100 });
      setSlas(data);
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(typeof message === "string" ? message : "Failed to load SLAs.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await slaService.create({
        name: form.name,
        description: form.description || null,
        priority: form.priority,
        response_time_minutes: form.response_time_minutes,
        resolution_time_minutes: form.resolution_time_minutes,
        is_active: form.is_active,
      });
      setShowCreate(false);
      setForm({
        name: "",
        description: "",
        priority: "medium",
        response_time_minutes: 60,
        resolution_time_minutes: 240,
        is_active: true,
      });
      load();
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(typeof message === "string" ? message : "Failed to create SLA.");
    }
  };

  const handleUpdate = async (e: FormEvent) => {
    e.preventDefault();
    if (editingId == null) return;
    try {
      await slaService.update(editingId, {
        name: form.name,
        description: form.description || null,
        priority: form.priority,
        response_time_minutes: form.response_time_minutes,
        resolution_time_minutes: form.resolution_time_minutes,
        is_active: form.is_active,
      });
      setEditingId(null);
      load();
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(typeof message === "string" ? message : "Failed to update SLA.");
    }
  };

  const startEdit = (s: SLA) => {
    setEditingId(s.id);
    setForm({
      name: s.name,
      description: s.description || "",
      priority: s.priority,
      response_time_minutes: s.response_time_minutes,
      resolution_time_minutes: s.resolution_time_minutes,
      is_active: s.is_active,
    });
    setShowCreate(false);
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm("Delete this SLA policy?")) return;
    try {
      await slaService.delete(id);
      load();
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(typeof message === "string" ? message : "Failed to delete SLA.");
    }
  };

  return (
    <div>
      <Navbar />
      <div className="app-layout">
        <Sidebar />
        <main className="page-content">
          <h1>SLA Policies</h1>
          {error && <p style={{ color: "crimson" }}>{error}</p>}

          <button
            type="button"
            onClick={() => {
              setShowCreate(!showCreate);
              setEditingId(null);
            }}
            style={{ marginBottom: 16 }}
          >
            {showCreate ? "Cancel" : "New SLA"}
          </button>

          {(showCreate || editingId != null) && (
            <form
              onSubmit={editingId != null ? handleUpdate : handleCreate}
              style={{
                border: "1px solid var(--border)",
                padding: 16,
                marginBottom: 24,
                maxWidth: 480,
              }}
            >
              <h3>{editingId != null ? "Edit SLA" : "Create SLA"}</h3>
              <div style={{ display: "grid", gap: 8 }}>
                <label>
                  Name
                  <input
                    required
                    value={form.name}
                    onChange={(e) =>
                      setForm({ ...form, name: e.target.value })
                    }
                  />
                </label>
                <label>
                  Description
                  <textarea
                    rows={2}
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
                <label>
                  Response Time (minutes)
                  <input
                    type="number"
                    min={1}
                    required
                    value={form.response_time_minutes}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        response_time_minutes: Number(e.target.value),
                      })
                    }
                  />
                </label>
                <label>
                  Resolution Time (minutes)
                  <input
                    type="number"
                    min={1}
                    required
                    value={form.resolution_time_minutes}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        resolution_time_minutes: Number(e.target.value),
                      })
                    }
                  />
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={form.is_active}
                    onChange={(e) =>
                      setForm({ ...form, is_active: e.target.checked })
                    }
                  />{" "}
                  Active
                </label>
                <button type="submit">
                  {editingId != null ? "Save" : "Create"}
                </button>
              </div>
            </form>
          )}

          {loading ? (
            <p>Loading...</p>
          ) : slas.length === 0 ? (
            <p>No SLA policies.</p>
          ) : (
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ textAlign: "left", borderBottom: "1px solid var(--border)" }}>
                  <th style={{ padding: 8 }}>ID</th>
                  <th style={{ padding: 8 }}>Name</th>
                  <th style={{ padding: 8 }}>Priority</th>
                  <th style={{ padding: 8 }}>Response (min)</th>
                  <th style={{ padding: 8 }}>Resolution (min)</th>
                  <th style={{ padding: 8 }}>Active</th>
                  <th style={{ padding: 8 }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {slas.map((s) => (
                  <tr key={s.id} style={{ borderBottom: "1px solid var(--border)" }}>
                    <td style={{ padding: 8 }}>{s.id}</td>
                    <td style={{ padding: 8 }}>{s.name}</td>
                    <td style={{ padding: 8 }}>{s.priority}</td>
                    <td style={{ padding: 8 }}>{s.response_time_minutes}</td>
                    <td style={{ padding: 8 }}>{s.resolution_time_minutes}</td>
                    <td style={{ padding: 8 }}>{s.is_active ? "Yes" : "No"}</td>
                    <td style={{ padding: 8 }}>
                      <button type="button" onClick={() => startEdit(s)}>
                        Edit
                      </button>{" "}
                      <button type="button" onClick={() => handleDelete(s.id)}>
                        Delete
                      </button>
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

export default SLAPage;
