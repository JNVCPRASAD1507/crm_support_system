import React,{ useEffect, useState } from "react";
import { notifications } from "../api";
import { Bell, Check } from "lucide-react";
export default function Notifications() {
  const [list, setList] = useState([]);
  const load = () => notifications.list().then((r) => setList(r.data));
  useEffect(load, []);
  const read = async (id) => {
    await notifications.read(id);
    load();
  };
  return (
    <>
      <div className="page-intro">
        <div>
          <h2>Notifications</h2>
          <p>Ticket events, assignments and SLA alerts.</p>
        </div>
        <button
          className="ghost"
          onClick={async () => {
            await notifications.readAll();
            load();
          }}
        >
          <Check size={16} /> Mark all read
        </button>
      </div>
      <div className="notification-list">
        {list.map((n) => (
          <div className={`notification ${n.is_read ? "read" : ""}`} key={n.id}>
            <div className="customer-icon">
              <Bell size={17} />
            </div>
            <div>
              <b>{n.title}</b>
              <p>{n.message}</p>
              <small>{new Date(n.created_at).toLocaleString()}</small>
            </div>
            {!n.is_read && (
              <button className="ghost" onClick={() => read(n.id)}>
                Read
              </button>
            )}
          </div>
        ))}
        {!list.length && (
          <div className="empty">
            <Bell size={30} />
            <b>You're all caught up</b>
            <span>New ticket activity will appear here.</span>
          </div>
        )}
      </div>
    </>
  );
}
