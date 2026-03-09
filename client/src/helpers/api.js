const API_BASE = `${process.env.REACT_APP_API_BASE}/api`;

export async function getProducts() {
  const res = await fetch(`${API_BASE}/products/`);
  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }
  return res.json();
}
