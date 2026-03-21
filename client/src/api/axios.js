import axios from "axios";

// create axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE,
  withCredentials: true, // send cookies with every request
  timeout: 10000, // stop waiting after 10 seconds
});

// response interceptor
api.interceptors.response.use(
  // return successful response as is
  (response) => response,

  // handle response errors
  async (error) => {
    const originalRequest = error.config;

    // do not retry refresh request itself
    if (originalRequest?.url?.includes("/api/auth/refresh/")) {
      window.dispatchEvent(new Event("auth:logout"));
      return Promise.reject(error);
    }

    // try refresh only once for 401 errors
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // use plain axios here to avoid interceptor conflicts
        await axios.post(
          `${process.env.REACT_APP_API_BASE}/api/auth/refresh/`,
          {},
          {
            withCredentials: true,
            timeout: 10000, // use the same timeout for refresh
          }
        );

        // retry the original request
        return api(originalRequest);
      } catch (refreshError) {
        window.dispatchEvent(new Event("auth:logout"));
        return Promise.reject(refreshError);
      }
    }

    // reject all other errors
    return Promise.reject(error);
  }
);

export default api;