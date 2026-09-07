import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const items = [
  ["/dashboard", "Dashboard", "▦"],
  ["/tickets", "Tickets", "◫"],
  ["/customers", "Customers", "♙"],
] as const;

function Sidebar() {
  const { user } = useAuth();
  const isAdmin = user?.role === "admin";
  const isAgent = user?.role === "support_agent" || isAdmin;
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `nav-link${isActive ? " active" : ""}`;

  return (
    <aside className="sidebar" aria-label="Primary navigation">
      <nav className="sidebar-nav">
        <p className="nav-section-label">Workspace</p>
        {items.map(([to, label, icon]) => (
          <NavLink key={to} to={to} className={linkClass}>
            <span aria-hidden="true">{icon}</span>
            {label}
          </NavLink>
        ))}
        {isAgent && (
          <NavLink to="/categories" className={linkClass}>
            <span aria-hidden="true">⌘</span>Categories
          </NavLink>
        )}
        {isAdmin && (
          <>
            <p className="nav-section-label">Administration</p>
            <NavLink to="/sla" className={linkClass}>
              <span aria-hidden="true">◷</span>SLA
            </NavLink>
            <NavLink to="/notifications" className={linkClass}>
              <span aria-hidden="true">◉</span>Notifications
            </NavLink>
            <NavLink to="/audit-logs" className={linkClass}>
              <span aria-hidden="true">≡</span>Audit Logs
            </NavLink>
          </>
        )}
      </nav>
      <div className="sidebar-foot">
        <span className="status-dot" /> API-connected workspace
      </div>
    </aside>
  );
}

export default Sidebar;
