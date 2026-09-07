import { useEffect, useState } from "react";
import notificationService from "../services/notificationService";
import type { Notification } from "../types/notification";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function Notifications() {
  const [items, setItems] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await notificationService.list();
      setItems(data);
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(
        typeof message === "string" ? message : "Failed to load notifications.",
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const markRead = async (id: number) => {
    try {
      await notificationService.markRead(id);
      load();
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(
        typeof message === "string" ? message : "Failed to mark as read.",
      );
    }
  };

  const markAll = async () => {
    try {
      await notificationService.markAllRead();
      load();
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(
        typeof message === "string" ? message : "Failed to mark all as read.",
      );
    }
  };

  return (
    <div>
      <Navbar />
      <div className="app-layout">
        <Sidebar />
        <main className="page-content">
          <h1>Notifications</h1>
          {error && <p style={{ color: "crimson" }}>{error}</p>}

          <button type="button" onClick={markAll} style={{ marginBottom: 16 }}>
            Mark all as read
          </button>

          {loading ? (
            <p>Loading...</p>
          ) : items.length === 0 ? (
            <p>No notifications.</p>
          ) : (
            <ul style={{ listStyle: "none", padding: 0 }}>
              {items.map((n) => (
                <li
                  key={n.id}
                  style={{
                    border: "1px solid var(--border)",
                    borderRadius: 8,
                    padding: 12,
                    marginBottom: 8,
                    background: n.is_read ? "transparent" : "var(--accent-bg)",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "flex-start",
                    }}
                  >
                    <div>
                      <strong>{n.title}</strong>
                      <p style={{ margin: "4px 0" }}>{n.message}</p>
                      <small>
                        {n.type}
                        {n.ticket_id != null && ` · Ticket #${n.ticket_id}`}
                        {" · "}
                        {new Date(n.created_at).toLocaleString()}
                      </small>
                    </div>
                    {!n.is_read && (
                      <button type="button" onClick={() => markRead(n.id)}>
                        Mark read
                      </button>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </main>
      </div>
    </div>
  );
}

export default Notifications;
