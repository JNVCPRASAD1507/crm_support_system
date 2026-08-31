
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { LifeBuoy, ShieldCheck } from "lucide-react";
import { auth } from "../api";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
    phone: "",
  });

  const [err, setErr] = useState("");
  const [success, setSuccess] = useState("");
  const [busy, setBusy] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const submit = async (e) => {
    e.preventDefault();

    setBusy(true);
    setErr("");
    setSuccess("");

    try {
      await auth.register({
        full_name: form.full_name,
        email: form.email,
        password: form.password,
        phone: form.phone || null,
      });

      setSuccess("Account created successfully. Redirecting to login...");

      setTimeout(() => {
        navigate("/login");
      }, 1200);
    } catch (x) {
      const detail = x.response?.data?.detail;

      if (Array.isArray(detail)) {
        setErr(detail.map((item) => item.msg).join(", "));
      } else if (typeof detail === "string") {
        setErr(detail);
      } else {
        setErr("Unable to create account");
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

          <h1>Start resolving customer issues with ease.</h1>

          <p>
            Create your workspace account and manage support requests from
            one calm, organized platform.
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
        <div className="eyebrow">GET STARTED</div>

        <h2>Create account</h2>

        <p>Enter your details to create your customer account.</p>

        <label>
          Full name
          <input
            name="full_name"
            value={form.full_name}
            onChange={handleChange}
            type="text"
            placeholder="Enter your full name"
            minLength={2}
            maxLength={120}
            required
          />
        </label>

        <label>
          Email
          <input
            name="email"
            value={form.email}
            onChange={handleChange}
            type="email"
            placeholder="you@example.com"
            required
          />
        </label>

        <label>
          Phone
          <input
            name="phone"
            value={form.phone}
            onChange={handleChange}
            type="tel"
            placeholder="Enter your phone number"
          />
        </label>

        <label>
          Password
          <input
            name="password"
            value={form.password}
            onChange={handleChange}
            type="password"
            placeholder="Minimum 8 characters"
            minLength={8}
            required
          />
        </label>

        {err && <div className="error">{err}</div>}

        {success && <div className="success">{success}</div>}

        <button className="primary wide" disabled={busy}>
          {busy ? "Creating account…" : "Create account"}
        </button>

        <div className="demo">
          Already have an account?{" "}
          <Link to="/login">Sign in</Link>
        </div>
      </form>
    </div>
  );
}

