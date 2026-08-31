import { useEffect, useState } from "react";
import React from "react";
import { agents } from "../api";
import { UserRound, CheckCircle, XCircle } from "lucide-react";
export default function Agents() {
  const [list, setList] = useState([]);
  useEffect(() => {
    agents.list().then((r) => setList(r.data));
  }, []);
  return (
    <>
      <div className="page-intro">
        <div>
          <h2>Support agents</h2>
          <p>Monitor availability and assignment readiness.</p>
        </div>
      </div>
      <div className="agent-grid">
        {list.map((a) => (
          <div className="agent-card" key={a.id}>
            <div className="avatar big">{a.full_name?.[0]}</div>
            <div>
              <h3>{a.full_name}</h3>
              <p>{a.email}</p>
            </div>
            <span>
              {a.is_active ? (
                <>
                  <CheckCircle size={15} /> Active
                </>
              ) : (
                <>
                  <XCircle size={15} /> Inactive
                </>
              )}
            </span>
          </div>
        ))}
        {!list.length && (
          <div className="empty">
            <UserRound size={30} />
            <b>No support agents</b>
            <span>Create agents from the API / admin tools.</span>
          </div>
        )}
      </div>
    </>
  );
}
