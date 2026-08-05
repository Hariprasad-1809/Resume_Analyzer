import axios from "axios";

/**
 * Resolves the Backend API Base URL.
 * Sanitizes trailing slashes and falls back seamlessly to the live Render deployment.
 */
export const getApiBaseUrl = (): string => {
  let url = "https://resume-analyzer-gqte.onrender.com";

  if (typeof window !== "undefined") {
    const saved = localStorage.getItem("settings_api_url");
    if (saved && saved.trim() !== "") {
      url = saved.trim();
    } else if (process.env.NEXT_PUBLIC_API_URL && process.env.NEXT_PUBLIC_API_URL.trim() !== "") {
      url = process.env.NEXT_PUBLIC_API_URL.trim();
    }
  } else if (process.env.NEXT_PUBLIC_API_URL && process.env.NEXT_PUBLIC_API_URL.trim() !== "") {
    url = process.env.NEXT_PUBLIC_API_URL.trim();
  }

  // Remove any trailing slashes
  return url.replace(/\/+$/, "");
};

/**
 * Pre-configured Axios client instance for API requests.
 */
export const apiClient = axios.create();

// Add request interceptor to dynamically apply latest base URL
apiClient.interceptors.request.use((config) => {
  const baseUrl = getApiBaseUrl();
  if (config.url && !config.url.startsWith("http://") && !config.url.startsWith("https://")) {
    config.url = `${baseUrl}${config.url.startsWith("/") ? "" : "/"}${config.url}`;
  }
  return config;
});

export default apiClient;
