// client/src/pages/ProductsPage.jsx
import { useTest } from "../hooks/useTest";

export default function TestPage() {
  const { products, loading, error } = useTest();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>❌ Failed to load products.</div>;

  return (
    <div>
      <h1>상품 목록</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "1rem" }}>
        {products.map((p) => (
          <div key={p.id} style={{ border: "1px solid #ccc", padding: "1rem" }}>
            {p.image && (
              <img
                src={`http://127.0.0.1:8000${p.image}`}
                alt={p.title}
                style={{ width: "100%", height: "auto" }}
              />
            )}
            <h3>{p.title}</h3>
            <p>{p.description}</p>
            <p>{p.price} 원</p>
          </div>
        ))}
      </div>
    </div>
  );
}
