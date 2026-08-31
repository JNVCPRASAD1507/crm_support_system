import React,{ useEffect, useState } from "react";
import { categories } from "../api";
import Modal from "../components/Modal";
import { Plus, Tags } from "lucide-react";
export default function Categories() {
  const [list, setList] = useState([]),
    [open, setOpen] = useState(false),
    [f, setF] = useState({ name: "", description: "" });
  const load = () => categories.list().then((r) => setList(r.data));
  useEffect(load, []);
  const submit = async (e) => {
    e.preventDefault();
    await categories.create(f);
    setOpen(false);
    setF({ name: "", description: "" });
    load();
  };
  return (
    <>
      <div className="page-intro">
        <div>
          <h2>Categories</h2>
          <p>Organize incoming support requests.</p>
        </div>
        <button className="primary" onClick={() => setOpen(true)}>
          <Plus size={17} /> New category
        </button>
      </div>
      <div className="category-list">
        {list.map((c) => (
          <div className="category-row" key={c.id}>
            <div className="customer-icon">
              <Tags size={18} />
            </div>
            <div>
              <b>{c.name}</b>
              <p>{c.description || "No description"}</p>
            </div>
            <span className="badge open">
              {c.is_active ? "active" : "inactive"}
            </span>
          </div>
        ))}
      </div>
      <Modal open={open} onClose={() => setOpen(false)} title="New category">
        <form onSubmit={submit}>
          <label>
            Name
            <input
              required
              value={f.name}
              onChange={(e) => setF({ ...f, name: e.target.value })}
            />
          </label>
          <label>
            Description
            <textarea
              rows="4"
              value={f.description}
              onChange={(e) => setF({ ...f, description: e.target.value })}
            />
          </label>
          <button className="primary wide">Create category</button>
        </form>
      </Modal>
    </>
  );
}
