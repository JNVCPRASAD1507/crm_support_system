
import axios from "axios";

const rawBaseUrl =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000";

const baseURL = rawBaseUrl.replace(/\/$/, "");

const api = axios.create({
  baseURL,
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    const token =
      localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization =
        `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

api.interceptors.response.use(
  (response) => response,

  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");

      if (
        !window.location.pathname.startsWith(
          "/login",
        )
      ) {
        window.location.assign("/login");
      }
    }

    return Promise.reject(error);
  },
);

export default api;
