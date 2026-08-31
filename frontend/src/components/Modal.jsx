import React from "react";
export default function Modal({ open, onClose, title, children }) {
  if (!open) return null;
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-title">
          <h3>{title}</h3>
          <button onClick={onClose}>×</button>
        </div>
        {children}
      </div>
    </div>
  );
}
