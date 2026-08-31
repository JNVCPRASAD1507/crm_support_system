import { NavLink, Outlet } from "react-router-dom";
import React from "react";

import {
  LayoutDashboard,
  Ticket,
  Users,
  Tags,
  UserRound,
  LogOut,
  Bell,
  LifeBuoy,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
export default function AppLayout() {
  const { user, logout } = useAuth();
  const nav = [
    ["/", "Dashboard", LayoutDashboard],
    ["/tickets", "Tickets", Ticket],
    ...(user?.role !== "customer" ? [["/customers", "Customers", Users]] : []),
    ...(user?.role === "admin"
      ? [
          ["/categories", "Categories", Tags],
          ["/agents", "Agents", UserRound],
        ]
      : []),
    ["/notifications", "Notifications", Bell],
  ];
  return (
    <div className="shell">
      <aside>
        <div className="brand">
          <div className="logo">
            <LifeBuoy size={20} />
          </div>
          <div>
            <b>Resolve</b>
            <small>CRM Support</small>
          </div>
        </div>
        <div className="workspace">WORKSPACE</div>
        {nav.map(([to, label, I]) => (
          <NavLink key={to} to={to} end={to === "/"} className="nav">
            <I size={18} />
            <span>{label}</span>
          </NavLink>
        ))}
        <div className="side-bottom">
          <div className="mini-user">
            <div className="avatar">{user?.full_name?.[0]}</div>
            <div>
              <b>{user?.full_name}</b>
              <small>{user?.role?.replace("_", " ")}</small>
            </div>
          </div>
          <button className="logout" onClick={logout}>
            <LogOut size={16} />
            Sign out
          </button>
        </div>
      </aside>
      <main>
        <header>
          <div>
            <div className="eyebrow">CUSTOMER OPERATIONS</div>
            <h1>Support workspace</h1>
          </div>
          <div className="header-right">
            <span className="online-dot">● Live</span>
            <div className="avatar">{user?.full_name?.[0]}</div>
          </div>
        </header>
        <section className="content">
          <Outlet />
        </section>
      </main>
    </div>
  );
}
