import React,{ useEffect, useState } from "react";
import { customers } from "../api";
import { Plus, Search, Building2 } from "lucide-react";
import Modal from "../components/Modal";
export default function Customers() {
  const [d, setD] = useState({ items: [], total: 0 }),
    [search, setSearch] = useState(""),
    [open, setOpen] = useState(false),
    [f, setF] = useState({
      name: "",
      email: "",
      phone: "",
      company: "",
      address: "",
    });
  const load = () =>
    customers
      .list({ search: search || undefined, page: 1, limit: 20 })
      .then((r) => setD(r.data));
  useEffect(load, [search]);
  const submit = async (e) => {
    e.preventDefault();
    await customers.create(f);
    setOpen(false);
    load();
  };
  return (
    <>
      <div className="page-intro">
        <div>
          <h2>Customers</h2>
          <p>Manage customer profiles and support history.</p>
        </div>
        <button className="primary" onClick={() => setOpen(true)}>
          <Plus size={17} /> Add customer
        </button>
      </div>
      <div className="toolbar">
        <div className="search">
          <Search size={17} />
          <input
            placeholder="Search customers…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>
      <div className="customer-grid">
        {d.items.map((c) => (
          <div className="customer-card" key={c.id}>
            <div className="customer-icon">
              <Building2 size={20} />
            </div>
            <div>
              <h3>{c.name}</h3>
              <p>{c.company || "Independent customer"}</p>
              <span>{c.email}</span>
            </div>
            <i>{c.status}</i>
          </div>
        ))}
        {!d.items.length && (
          <div className="empty">
            <Building2 size={30} />
            <b>No customers yet</b>
            <span>Add your first customer profile.</span>
          </div>
        )}
      </div>
      <Modal open={open} onClose={() => setOpen(false)} title="Add customer">
        <form className="form-grid" onSubmit={submit}>
          {[
            ["name", "Name"],
            ["email", "Email"],
            ["phone", "Phone"],
            ["company", "Company"],
          ].map(([k, l]) => (
            <label key={k}>
              {l}
              <input
                required={k === "name" || k === "email"}
                value={f[k]}
                onChange={(e) => setF({ ...f, [k]: e.target.value })}
              />
            </label>
          ))}
          <label className="full">
            Address
            <textarea
              rows="3"
              value={f.address}
              onChange={(e) => setF({ ...f, address: e.target.value })}
            />
          </label>
          <button className="primary full">Save customer</button>
        </form>
      </Modal>
    </>
  );
}
