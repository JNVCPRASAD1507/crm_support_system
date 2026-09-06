import { useEffect, useState } from "react";
import auditLogService from "../services/auditLogService";
import type { AuditLog } from "../types/auditLog";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function AuditLogs() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await auditLogService.list({ limit: 100 });
        setLogs(data);
      } catch (err: any) {
        const message = err?.response?.data?.detail;
        setError(
          typeof message === "string" ? message : "Failed to load audit logs.",
        );
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <div>
      <Navbar />
      <div style={{ display: "flex" }}>
        <Sidebar />
        <main style={{ flex: 1, padding: 24 }}>
          <h1>Audit Logs</h1>
          {error && <p style={{ color: "crimson" }}>{error}</p>}

          {loading ? (
            <p>Loading...</p>
          ) : logs.length === 0 ? (
            <p>No audit logs.</p>
          ) : (
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
              <thead>
                <tr style={{ textAlign: "left", borderBottom: "1px solid var(--border)" }}>
                  <th style={{ padding: 8 }}>ID</th>
                  <th style={{ padding: 8 }}>Action</th>
                  <th style={{ padding: 8 }}>Entity</th>
                  <th style={{ padding: 8 }}>User</th>
                  <th style={{ padding: 8 }}>Description</th>
                  <th style={{ padding: 8 }}>When</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr
                    key={log.id}
                    style={{ borderBottom: "1px solid var(--border)" }}
                  >
                    <td style={{ padding: 8 }}>{log.id}</td>
                    <td style={{ padding: 8 }}>{log.action}</td>
                    <td style={{ padding: 8 }}>
                      {log.entity_type}
                      {log.entity_id != null ? ` #${log.entity_id}` : ""}
                    </td>
                    <td style={{ padding: 8 }}>{log.user_id ?? "—"}</td>
                    <td style={{ padding: 8 }}>{log.description ?? "—"}</td>
                    <td style={{ padding: 8 }}>
                      {new Date(log.created_at).toLocaleString()}
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

export default AuditLogs;
