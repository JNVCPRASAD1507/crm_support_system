import { FormEvent, useEffect, useState } from "react";
import categoryService from "../services/categoryService";
import type { Category } from "../types/category";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function Categories() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState({
    name: "",
    description: "",
    is_active: true,
  });

  const load = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await categoryService.list({ limit: 100 });
      setCategories(data);
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(typeof message === "string" ? message : "Failed to load categories.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await categoryService.create({
        name: form.name,
        description: form.description || null,
        is_active: form.is_active,
      });
      setShowCreate(false);
      setForm({ name: "", description: "", is_active: true });
      load();
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(typeof message === "string" ? message : "Failed to create category.");
    }
  };

  const handleUpdate = async (e: FormEvent) => {
    e.preventDefault();
    if (editingId == null) return;
    try {
      await categoryService.update(editingId, {
        name: form.name,
        description: form.description || null,
        is_active: form.is_active,
      });
      setEditingId(null);
      setForm({ name: "", description: "", is_active: true });
      load();
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(typeof message === "string" ? message : "Failed to update category.");
    }
  };

  const startEdit = (c: Category) => {
    setEditingId(c.id);
    setForm({
      name: c.name,
      description: c.description || "",
      is_active: c.is_active,
    });
    setShowCreate(false);
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm("Delete this category?")) return;
    try {
      await categoryService.delete(id);
      load();
    } catch (err: any) {
      const message = err?.response?.data?.detail;
      setError(typeof message === "string" ? message : "Failed to delete category.");
    }
  };

  return (
    <div>
      <Navbar />
      <div className="app-layout">
        <Sidebar />
        <main className="page-content">
          <h1>Categories</h1>
          {error && <p style={{ color: "crimson" }}>{error}</p>}

          <button
            type="button"
            onClick={() => {
              setShowCreate(!showCreate);
              setEditingId(null);
              setForm({ name: "", description: "", is_active: true });
            }}
            style={{ marginBottom: 16 }}
          >
            {showCreate ? "Cancel" : "New Category"}
          </button>

          {(showCreate || editingId != null) && (
            <form
              onSubmit={editingId != null ? handleUpdate : handleCreate}
              style={{
                border: "1px solid var(--border)",
                padding: 16,
                marginBottom: 24,
                maxWidth: 400,
              }}
            >
              <h3>{editingId != null ? "Edit Category" : "Create Category"}</h3>
              <div style={{ display: "grid", gap: 8 }}>
                <label>
                  Name
                  <input
                    required
                    minLength={2}
                    value={form.name}
                    onChange={(e) =>
                      setForm({ ...form, name: e.target.value })
                    }
                  />
                </label>
                <label>
                  Description
                  <textarea
                    rows={3}
                    value={form.description}
                    onChange={(e) =>
                      setForm({ ...form, description: e.target.value })
                    }
                  />
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={form.is_active}
                    onChange={(e) =>
                      setForm({ ...form, is_active: e.target.checked })
                    }
                  />{" "}
                  Active
                </label>
                <button type="submit">
                  {editingId != null ? "Save" : "Create"}
                </button>
              </div>
            </form>
          )}

          {loading ? (
            <p>Loading...</p>
          ) : categories.length === 0 ? (
            <p>No categories.</p>
          ) : (
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ textAlign: "left", borderBottom: "1px solid var(--border)" }}>
                  <th style={{ padding: 8 }}>ID</th>
                  <th style={{ padding: 8 }}>Name</th>
                  <th style={{ padding: 8 }}>Description</th>
                  <th style={{ padding: 8 }}>Active</th>
                  <th style={{ padding: 8 }}>Created</th>
                  <th style={{ padding: 8 }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {categories.map((c) => (
                  <tr key={c.id} style={{ borderBottom: "1px solid var(--border)" }}>
                    <td style={{ padding: 8 }}>{c.id}</td>
                    <td style={{ padding: 8 }}>{c.name}</td>
                    <td style={{ padding: 8 }}>{c.description ?? "—"}</td>
                    <td style={{ padding: 8 }}>{c.is_active ? "Yes" : "No"}</td>
                    <td style={{ padding: 8 }}>
                      {new Date(c.created_at).toLocaleDateString()}
                    </td>
                    <td style={{ padding: 8 }}>
                      <button type="button" onClick={() => startEdit(c)}>
                        Edit
                      </button>{" "}
                      <button type="button" onClick={() => handleDelete(c.id)}>
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </main>
      </div>
    </div>
  );
}

export default Categories;
