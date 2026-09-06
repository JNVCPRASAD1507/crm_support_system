import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "12px 20px",
        borderBottom: "1px solid var(--border)",
        background: "var(--bg)",
      }}
    >
      <div>
        <Link
          to="/dashboard"
          style={{
            fontWeight: 600,
            color: "var(--text-h)",
            textDecoration: "none",
            marginRight: 16,
          }}
        >
          CRM Support
        </Link>
      </div>

      <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
        {user && (
          <>
            <span style={{ fontSize: 14 }}>
              {user.full_name} ({user.role})
            </span>
            <button type="button" onClick={handleLogout}>
              Logout
            </button>
          </>
        )}
      </div>
    </header>
  );
}

export default Navbar;
