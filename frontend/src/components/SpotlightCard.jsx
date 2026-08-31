import React from "react";
export default function SpotlightCard({ children, className = "" }) {
  return <div className={`spotlight-card ${className}`}>{children}</div>;
}
