
import {
  FormEvent,
  useState,
} from "react";

import {
  Link,
  useNavigate,
} from "react-router-dom";

import { useAuth } from "../context/AuthContext";

import type { UserRole } from "../types/auth";

function Register() {
  const navigate = useNavigate();

  const { register } = useAuth();

  const [fullName, setFullName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [phone, setPhone] =
    useState("");

  const [role, setRole] =
    useState<UserRole>("customer");

  const [error, setError] =
    useState("");

  const [success, setSuccess] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      await register({
        full_name: fullName,
        email,
        password,
        phone: phone || undefined,
        role,
      });

      setSuccess(
        "Registration successful. Redirecting to login...",
      );

      setTimeout(() => {
        navigate("/login");
      }, 1000);
    } catch (err: any) {
      const message =
        err?.response?.data?.detail;

      if (typeof message === "string") {
        setError(message);
      } else {
        setError(
          "Registration failed.",
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
      <h1>Create account</h1>
      <p>Set up your CRM Support workspace profile.</p>

      {error && <p className="alert alert-error" role="alert">{error}</p>}

      {success && <p className="alert alert-success" role="status">{success}</p>}

      <form
        onSubmit={handleSubmit}
      >
        <div>
          <label>
            Full Name
          </label>

          <input
            type="text"
            value={fullName}
            onChange={(event) =>
              setFullName(
                event.target.value,
              )
            }
            required
          />
        </div>

        <div>
          <label>
            Email
          </label>

          <input
            type="email"
            value={email}
            onChange={(event) =>
              setEmail(
                event.target.value,
              )
            }
            required
          />
        </div>

        <div>
          <label>
            Password
          </label>

          <input
            type="password"
            value={password}
            onChange={(event) =>
              setPassword(
                event.target.value,
              )
            }
            minLength={8}
            required
          />
        </div>

        <div>
          <label>
            Phone
          </label>

          <input
            type="tel"
            value={phone}
            onChange={(event) =>
              setPhone(
                event.target.value,
              )
            }
          />
        </div>

        <div>
          <label>
            Role
          </label>

          <select
            value={role}
            onChange={(event) =>
              setRole(
                event.target.value as UserRole,
              )
            }
          >
            <option value="customer">
              Customer
            </option>

            <option value="support_agent">
              Support Agent
            </option>

            <option value="admin">
              Admin
            </option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading}
        >
          {loading
            ? "Creating account..."
            : "Register"}
        </button>
      </form>

      <p>Already have an account? <Link to="/login">Login</Link></p>
      </div>
    </div>
  );
}

export default Register;
