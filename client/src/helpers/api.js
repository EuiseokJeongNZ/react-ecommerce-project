const API_BASE = "http://127.0.0.1:8000/api";

export async function getProducts() {
  const res = await fetch(`${API_BASE}/products/`);
  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }
  return res.json();
}
