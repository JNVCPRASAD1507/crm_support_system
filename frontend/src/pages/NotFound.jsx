import { Link } from "react-router-dom";
import React from "react";

export default function NotFound() {
  return (
    <div className="empty">
      <h2>404</h2>
      <p>Page not found.</p>
      <Link to="/" className="primary">
        Back to dashboard
      </Link>
    </div>
  );
}
