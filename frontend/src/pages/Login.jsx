import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";
import { LifeBuoy, ShieldCheck } from "lucide-react";
export default function Login() {
  const { login } = useAuth();
  const [email, setEmail] = useState("admin@crm.local"),
    [password, setPassword] = useState("Admin@123"),
    [err, setErr] = useState(""),
    [busy, setBusy] = useState(false);
  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setErr("");
    try {
      await login({ email, password });
      location.href = "/";
    } catch (x) {
      const detail = x.response?.data?.detail;

      if (Array.isArray(detail)) {
        setErr(detail.map((item) => item.msg).join(", "));
      } else if (typeof detail === "string") {
        setErr(detail);
      } else {
        setErr("Unable to sign in");
      }
    } finally {
      setBusy(false);
    }
  };
  return (
    <div className="login-page">
      <div className="login-art">
        <div className="brand large">
          <div className="logo">
            <LifeBuoy />
          </div>
          <div>
            <b>Resolve</b>
            <small>CRM Support</small>
          </div>
        </div>
        <div>
          <div className="eyebrow">CUSTOMER OPERATIONS PLATFORM</div>
          <h1>Turn every ticket into a resolved customer.</h1>
          <p>
            One calm workspace for customers, support agents and administrators.
          </p>
        </div>
        <div className="art-card">
          <ShieldCheck />
          <div>
            <b>Secure by default</b>
            <span>JWT authentication · RBAC · SLA monitoring</span>
          </div>
        </div>
      </div>
      <form className="login-card" onSubmit={submit}>
        <div className="eyebrow">WELCOME BACK</div>
        <h2>Sign in</h2>
        <p>Use your workspace credentials to continue.</p>
        <label>
          Email
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="email"
            required
          />
        </label>
        <label>
          Password
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            required
          />
        </label>
        {err && <div className="error">{err}</div>}
        <button className="primary wide" disabled={busy}>
          {busy ? "Signing in…" : "Sign in to workspace"}
        </button>
        <div className="demo">
          <b>Demo admin</b>
          <span>admin@crm.local / Admin@123</span>

          <div>
            Don't have an account? <Link to="/register">Create account</Link>
          </div>
        </div>
      </form>
    </div>
  );
}
