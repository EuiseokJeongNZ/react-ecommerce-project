import axios from "axios";

// create axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE,
  withCredentials: true,
});

export default api;