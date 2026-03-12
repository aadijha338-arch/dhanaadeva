import React, { useState } from "react";
import {
  createBusiness,
  createProduct,
  createSale,
  generateRecommendations,
  getRecommendations
} from "./api";

function App() {
  const [business, setBusiness] = useState(null);
  const [product, setProduct] = useState(null);
  const [recs, setRecs] = useState([]);

  const [bizName, setBizName] = useState("");
  const [industry, setIndustry] = useState("");
  const [prodName, setProdName] = useState("");
  const [baseCost, setBaseCost] = useState("");
  const [market, setMarket] = useState("UK");
  const [saleDate, setSaleDate] = useState("");
  const [units, setUnits] = useState("");
  const [price, setPrice] = useState("");

  async function handleCreateBusiness(e) {
    e.preventDefault();
    const b = await createBusiness(bizName, industry);
    setBusiness(b);
  }

  async function handleCreateProduct(e) {
    e.preventDefault();
    if (!business) return;
    const p = await createProduct(
      business.id,
      prodName,
      parseFloat(baseCost),
      market
    );
    setProduct(p);
  }

  async function handleAddSale(e) {
    e.preventDefault();
    if (!product) return;
    await createSale(product.id, saleDate, parseInt(units), parseFloat(price));
    alert("Sale added");
  }

  async function handleGenerateRecs() {
    if (!business) return;
    await generateRecommendations(business.id);
    const r = await getRecommendations(business.id);
    setRecs(r);
  }

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>DhanaaDev – Profit Intelligence</h1>

      <section>
        <h2>1. Business</h2>
        <form onSubmit={handleCreateBusiness}>
          <input
            placeholder="Business name"
            value={bizName}
            onChange={(e) => setBizName(e.target.value)}
          />
          <input
            placeholder="Industry"
            value={industry}
            onChange={(e) => setIndustry(e.target.value)}
          />
          <button type="submit">Save business</button>
        </form>
        {business && <p>Current business: {business.name}</p>}
      </section>

      <section>
        <h2>2. Product & Market</h2>
        <form onSubmit={handleCreateProduct}>
          <input
            placeholder="Product name"
            value={prodName}
            onChange={(e) => setProdName(e.target.value)}
          />
          <input
            placeholder="Base cost"
            value={baseCost}
            onChange={(e) => setBaseCost(e.target.value)}
          />
          <input
            placeholder="Market (e.g. UK)"
            value={market}
            onChange={(e) => setMarket(e.target.value)}
          />
          <button type="submit" disabled={!business}>
            Save product
          </button>
        </form>
        {product && <p>Current product: {product.name} ({product.market})</p>}
      </section>

      <section>
        <h2>3. Sales data</h2>
        <form onSubmit={handleAddSale}>
          <input
            type="date"
            value={saleDate}
            onChange={(e) => setSaleDate(e.target.value)}
          />
          <input
            placeholder="Units sold"
            value={units}
            onChange={(e) => setUnits(e.target.value)}
          />
          <input
            placeholder="Price"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
          />
          <button type="submit" disabled={!product}>
            Add sale
          </button>
        </form>
      </section>

      <section>
        <h2>4. AI Recommendations</h2>
        <button onClick={handleGenerateRecs} disabled={!business}>
          Run AI engine
        </button>
        <ul>
          {recs.map((r) => (
            <li key={r.id} style={{ marginTop: "1rem" }}>
              <strong>{r.title}</strong>
              <br />
              {r.description}
              <br />
              Expected profit change: {r.expected_profit_change.toFixed(2)} (
              {r.risk_level})
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

export default App;