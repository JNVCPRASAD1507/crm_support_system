import { createContext, useContext, useEffect, useState } from "react";
import { auth } from "../api";
import React from "react";
const C = createContext();
export function AuthProvider({ children }) {
  const [user, setUser] = useState(() =>
    JSON.parse(localStorage.getItem("crm_user") || "null"),
  );
  const [loading, setLoading] = useState(!!localStorage.getItem("crm_token"));
  useEffect(() => {
    if (localStorage.getItem("crm_token"))
      auth
        .profile()
        .then((r) => {
          setUser(r.data);
          localStorage.setItem("crm_user", JSON.stringify(r.data));
        })
        .catch(() => {})
        .finally(() => setLoading(false));
  }, []);
  const login = async (d) => {
    const r = await auth.login(d);
    localStorage.setItem("crm_token", r.data.access_token);
    const p = await auth.profile();
    setUser(p.data);
    localStorage.setItem("crm_user", JSON.stringify(p.data));
  };
  const logout = () => {
    localStorage.clear();
    setUser(null);
    window.location = "/login";
  };
  return (
    <C.Provider value={{ user, login, logout, loading }}>{children}</C.Provider>
  );
}
export const useAuth = () => useContext(C);
