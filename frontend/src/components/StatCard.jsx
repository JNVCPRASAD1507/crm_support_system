import SpotlightCard from "./SpotlightCard";
import React from "react";

export default function StatCard({ label, value, icon: Icon, tone = "" }) {
  return (
    <SpotlightCard>
      <div className="stat-head">
        <span>{label}</span>
        <Icon size={18} />
      </div>
      <strong className={tone}>{value ?? 0}</strong>
    </SpotlightCard>
  );
}
