
import {
  useCallback,
  useEffect,
  useState,
} from "react";

import customerService from "../services/customerService";

import type {
  Customer,
} from "../types/customer";

import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function Customers() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [customers, setCustomers] =
    useState<Customer[]>([]);

  const [total, setTotal] =
    useState(0);

  const [page, setPage] =
    useState(1);

  const [pages, setPages] =
    useState(0);

  const [search, setSearch] =
    useState("");

  const [statusFilter, setStatusFilter] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const limit = 10;

  const loadCustomers = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      const skip = (page - 1) * limit;

      const data = await customerService.list({
        skip,
        limit,
        search: search.trim() || undefined,
        status: statusFilter || undefined,
      });

      setCustomers(Array.isArray(data) ? data : []);

      setTotal(
        Array.isArray(data)
          ? data.length
          : 0,
      );

      setPages(
        Math.max(
          1,
          Math.ceil(
            (Array.isArray(data)
              ? data.length
              : 0) / limit,
          ),
        ),
      );
    } catch (err: any) {
      const message =
        err?.response?.data?.detail;

      setError(
        typeof message === "string"
          ? message
          : "Failed to load customers.",
      );
    } finally {
      setLoading(false);
    }
  }, [
    page,
    search,
    statusFilter,
  ]);

  useEffect(() => {
    loadCustomers();
  }, [loadCustomers]);

  const handleSearch = () => {
    setPage(1);
  };

  const handleDelete = async (
    customerId: number,
  ) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this customer?",
    );

    if (!confirmed) {
      return;
    }

    try {
      await customerService.delete(
        customerId,
      );

      await loadCustomers();
    } catch (err: any) {
      const message =
        err?.response?.data?.detail;

      setError(
        typeof message === "string"
          ? message
          : "Failed to delete customer.",
      );
    }
  };

  return (
    <div>
      <Navbar />

      <div className="app-layout">
        <Sidebar />

        <main className="page-content">

          {/* Page Header */}
          <div className="page-header-row">
            <div>

              {/* Back Button
              <button
                type="button"
                className="back-button"
                onClick={() =>
                  navigate("/dashboard")
                }
                aria-label="Back to dashboard"
                title="Back to dashboard"
              >
                <span aria-hidden="true">
                  ←
                </span>{" "}
                Back
              </button> */}

              <h1>Customers</h1>

              <p>
                Total Customers: {total}
              </p>

            </div>
          </div>

          {/* Search & Filters */}
          <section
            className="toolbar"
            aria-label="Customer filters"
          >
            <input
              type="text"
              placeholder="Search customers..."
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  handleSearch();
                }
              }}
              aria-label="Search customers"
            />

            <select
              value={statusFilter}
              onChange={(event) => {
                setStatusFilter(
                  event.target.value,
                );

                setPage(1);
              }}
              aria-label="Filter customers by status"
            >
              <option value="">
                All Statuses
              </option>

              <option value="active">
                Active
              </option>

              <option value="inactive">
                Inactive
              </option>
            </select>

            <button
              type="button"
              onClick={handleSearch}
            >
              Search
            </button>

            <button
              type="button"
              className="button-secondary"
              onClick={loadCustomers}
            >
              Refresh
            </button>
          </section>

          {/* Loading State */}
          {loading && (
            <div
              className="skeleton-list"
              aria-label="Loading customers"
            >
              <span className="skeleton" />
              <span className="skeleton" />
              <span className="skeleton" />
            </div>
          )}

          {/* Error State */}
          {error && (
            <div
              className="alert alert-error"
              role="alert"
            >
              <p>{error}</p>

              <button
                type="button"
                onClick={loadCustomers}
              >
                Retry
              </button>
            </div>
          )}

          {/* Empty State */}
          {!loading &&
            !error &&
            customers.length === 0 && (
              <section className="empty-state">
                <h2>
                  No customers found
                </h2>

                <p>
                  Try changing your search
                  or status filter.
                </p>
              </section>
            )}

          {/* Customers Table */}
          {!loading &&
            customers.length > 0 && (
              <div className="table-wrap">

                <table>
                  <thead>
                    <tr>
                      <th>ID</th>

                      <th>Name</th>

                      <th>Email</th>

                      <th>Phone</th>

                      <th>Company</th>

                      <th>Address</th>

                      <th>Status</th>

                      <th>Created</th>

                      {user?.role === "admin" && (
                        <th>
                          Actions
                        </th>
                      )}
                    </tr>
                  </thead>

                  <tbody>
                    {customers.map(
                      (customer) => (
                        <tr
                          key={
                            customer.id
                          }
                        >
                          <td>
                            {customer.id}
                          </td>

                          <td>
                            {customer.name}
                          </td>

                          <td>
                            {customer.email}
                          </td>

                          <td>
                            {customer.phone ||
                              "-"}
                          </td>

                          <td>
                            {customer.company ||
                              "-"}
                          </td>

                          <td>
                            {customer.address ||
                              "-"}
                          </td>

                          <td>
                            {customer.status}
                          </td>

                          <td>
                            {new Date(
                              customer.created_at,
                            ).toLocaleString()}
                          </td>

                          {user?.role ===
                            "admin" && (
                            <td>
                              <button
                                type="button"
                                onClick={() =>
                                  handleDelete(
                                    customer.id,
                                  )
                                }
                              >
                                Delete
                              </button>
                            </td>
                          )}
                        </tr>
                      ),
                    )}
                  </tbody>
                </table>

              </div>
            )}

          {/* Pagination */}
          {!loading &&
            pages > 0 &&
            customers.length > 0 && (
              <div className="pagination">

                <button
                  disabled={page <= 1}
                  onClick={() =>
                    setPage(
                      (current) =>
                        current - 1,
                    )
                  }
                >
                  Previous
                </button>

                <span>
                  Page {page} of {pages}
                </span>

                <button
                  disabled={
                    page >= pages
                  }
                  onClick={() =>
                    setPage(
                      (current) =>
                        current + 1,
                    )
                  }
                >
                  Next
                </button>

              </div>
            )}

        </main>
      </div>
    </div>
  );
}

export default Customers;
