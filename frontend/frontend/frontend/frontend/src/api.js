const BASE_URL = import.meta.env.VITE_API_URL;

export async function createBusiness(name, industry) {
  const res = await fetch(`${BASE_URL}/business?name=${name}&industry=${industry}`, {
    method: "POST"
  });
  return res.json();
}

export async function createProduct(businessId, name, baseCost, market) {
  const params = new URLSearchParams({
    business_id: businessId,
    name,
    base_cost: baseCost,
    market
  });
  const res = await fetch(`${BASE_URL}/product?${params.toString()}`, {
    method: "POST"
  });
  return res.json();
}

export async function createSale(productId, date, units, price) {
  const params = new URLSearchParams({
    product_id: productId,
    date,
    units_sold: units,
    price
  });
  const res = await fetch(`${BASE_URL}/sale?${params.toString()}`, {
    method: "POST"
  });
  return res.json();
}

export async function generateRecommendations(businessId) {
  const res = await fetch(
    `${BASE_URL}/ai/generate-recommendations?business_id=${businessId}`,
    { method: "POST" }
  );
  return res.json();
}

export async function getRecommendations(businessId) {
  const res = await fetch(
    `${BASE_URL}/recommendations?business_id=${businessId}`
  );
  return res.json();
}