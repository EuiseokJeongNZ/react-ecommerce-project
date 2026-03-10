import axios from "axios";

// create axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE,
  withCredentials: true, // send cookies with every request
});

// response interceptor
api.interceptors.response.use(
  // return successful response as is
  (response) => response,

  // handle response errors
  async (error) => {
    // keep the original failed request
    const originalRequest = error.config;

    // try refresh only once when access token is expired
    if (error.response?.status === 401 && !originalRequest._retry) {
      // prevent infinite retry loop
      originalRequest._retry = true;

      try {
        // request a new access token using refresh cookie
        await api.post("/api/auth/refresh/");

        // retry the original request after refresh succeeds
        return api(originalRequest);
      } catch (refreshError) {
        // notify the app that authentication is no longer valid
        window.dispatchEvent(new Event("auth:logout"));

        // reject refresh failure
        return Promise.reject(refreshError);
      }
    }

    // reject all other errors
    return Promise.reject(error);
  }
);

export default api;