import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [dark, setDark] = useState(
    () => localStorage.getItem("theme") === "dark",
  );

  useEffect(() => {
    document.documentElement.dataset.theme = dark ? "dark" : "light";
    localStorage.setItem("theme", dark ? "dark" : "light");
  }, [dark]);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header className="topbar">
      <Link
        to="/dashboard"
        className="brand"
        aria-label="CRM Support dashboard"
      >
        <span className="brand-mark" aria-hidden="true">
          CS
        </span>
        <span className="brand-copy">
          <strong>CRM Support</strong>
          <small>Service workspace</small>
        </span>
      </Link>

      <div className="topbar-actions">
        <button
          className="icon-button"
          type="button"
          onClick={() => setDark((v) => !v)}
          aria-label="Toggle dark mode"
          title="Toggle dark mode"
        >
          {dark ? "☀" : "☾"}
        </button>
        {user && (
          <>
            <div
              className="user-chip"
              title={`${user.full_name} • ${user.role}`}
            >
              <span className="avatar" aria-hidden="true">
                {user.full_name?.charAt(0)?.toUpperCase() || "U"}
              </span>
              <span className="user-meta">
                <strong>{user.full_name}</strong>
                <small>{user.role.replaceAll("_", " ")}</small>
              </span>
            </div>
            <button
              className="button button-secondary logout-button"
              type="button"
              onClick={handleLogout}
            >
              Logout
            </button>
          </>
        )}
      </div>
    </header>
  );
}

export default Navbar;
