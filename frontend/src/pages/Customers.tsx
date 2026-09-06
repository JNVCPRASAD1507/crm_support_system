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

function Customers() {
  const { user } = useAuth();

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

  const loadCustomers =
    useCallback(async () => {
      try {
        setLoading(true);
        setError("");

        const skip =
          (page - 1) * limit;

        const data =
          await customerService.list({
            skip,
            limit,
            search:
              search.trim() || undefined,
            status:
              statusFilter || undefined,
          });

        setCustomers(
          data.items,
        );

        setTotal(
          data.total,
        );

        setPages(
          data.pages,
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

  const handleSearch =
    () => {
      setPage(1);
    };

  const handleDelete =
    async (
      customerId: number,
    ) => {
      const confirmed =
        window.confirm(
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
      <header>
        <h1>
          Customers
        </h1>

        <p>
          Total Customers: {total}
        </p>
      </header>

      <hr />

      <section>
        <input
          type="text"
          placeholder="Search customers..."
          value={search}
          onChange={(event) =>
            setSearch(
              event.target.value,
            )
          }
          onKeyDown={(event) => {
            if (
              event.key === "Enter"
            ) {
              handleSearch();
            }
          }}
        />

        <select
          value={statusFilter}
          onChange={(event) => {
            setStatusFilter(
              event.target.value,
            );

            setPage(1);
          }}
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
          onClick={handleSearch}
        >
          Search
        </button>

        <button
          onClick={loadCustomers}
        >
          Refresh
        </button>
      </section>

      <hr />

      {loading && (
        <p>
          Loading customers...
        </p>
      )}

      {error && (
        <div>
          <p>
            {error}
          </p>

          <button
            onClick={loadCustomers}
          >
            Retry
          </button>
        </div>
      )}

      {!loading &&
        !error &&
        customers.length === 0 && (
          <p>
            No customers found.
          </p>
        )}

      {!loading &&
        customers.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>
                  ID
                </th>

                <th>
                  User ID
                </th>

                <th>
                  Phone
                </th>

                <th>
                  Address
                </th>

                <th>
                  Status
                </th>

                <th>
                  Created
                </th>

                {user?.role ===
                  "admin" && (
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
                      {customer.user_id}
                    </td>

                    <td>
                      {customer.phone ||
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
        )}

      <hr />

      {!loading &&
        pages > 0 && (
          <div>
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
              {" "}
              Page {page} of {pages}{" "}
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
    </div>
  );
}

export default Customers;

