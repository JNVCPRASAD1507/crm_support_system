import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const linkStyle = ({ isActive }: { isActive: boolean }) => ({
  display: "block",
  padding: "8px 12px",
  marginBottom: 4,
  borderRadius: 6,
  textDecoration: "none",
  color: isActive ? "var(--accent)" : "var(--text)",
  background: isActive ? "var(--accent-bg)" : "transparent",
  fontWeight: isActive ? 600 : 400,
});

function Sidebar() {
  const { user } = useAuth();

  const isAdmin = user?.role === "admin";
  const isAgent = user?.role === "support_agent" || isAdmin;

  return (
    <aside
      style={{
        width: 220,
        padding: 16,
        borderRight: "1px solid var(--border)",
        minHeight: "calc(100vh - 60px)",
      }}
    >
      <nav>
        <NavLink to="/dashboard" style={linkStyle}>
          Dashboard
        </NavLink>
        <NavLink to="/tickets" style={linkStyle}>
          Tickets
        </NavLink>
        <NavLink to="/customers" style={linkStyle}>
          Customers
        </NavLink>
        {isAgent && (
          <NavLink to="/categories" style={linkStyle}>
            Categories
          </NavLink>
        )}
        {isAdmin && (
          <>
            <NavLink to="/sla" style={linkStyle}>
              SLA
            </NavLink>
            <NavLink to="/notifications" style={linkStyle}>
              Notifications
            </NavLink>
            <NavLink to="/audit-logs" style={linkStyle}>
              Audit Logs
            </NavLink>
          </>
        )}
      </nav>
    </aside>
  );
}

export default Sidebar;
