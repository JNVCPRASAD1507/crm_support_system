import React from "react";


export default function StatusBadge({ value }) {
  return (
    <span className={`badge ${String(value).replaceAll("_", "-")}`}>
      {String(value).replaceAll("_", " ")}
    </span>
  );
}
