import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from . import models

def train_demand_model(df):
    X = df[["price"]]
    y = df["units"]
    model = RandomForestRegressor(n_estimators=200)
    model.fit(X, y)
    return model

def estimate_price_elasticity(df):
    X = df[["price"]]
    y = df["units"]
    model = LinearRegression()
    model.fit(X, y)
    return model.coef_[0]

def country_risk_adjustment(db: Session, country: str):
    indicators = (
        db.query(models.CountryIndicator)
        .filter(models.CountryIndicator.country == country)
        .all()
    )
    if not indicators:
        return 1.0

    df = pd.DataFrame([{
        "inflation": c.inflation_rate,
        "risk": c.risk_score,
        "volatility": c.currency_volatility
    } for c in indicators])

    score = (
        df["inflation"].mean() * 0.3 +
        df["risk"].mean() * 0.5 +
        df["volatility"].mean() * 0.2
    )

    return max(0.5, min(1.5, 1 + (score - 5) / 10))

def generate_recommendations(db: Session, business_id: int):
    products = (
        db.query(models.Product)
        .filter(models.Product.business_id == business_id)
        .all()
    )
    recs = []

    for p in products:
        sales = db.query(models.Sale).filter(models.Sale.product_id == p.id).all()
        if not sales:
            continue

        df = pd.DataFrame(
            [{"price": s.price, "units": s.units_sold} for s in sales]
        )

        demand_model = train_demand_model(df)
        elasticity = estimate_price_elasticity(df)

        price_range = np.linspace(df["price"].min() * 0.8,
                                  df["price"].max() * 1.2, 20)
        results = []
        for price in price_range:
            predicted_units = demand_model.predict([[price]])[0]
            revenue = price * predicted_units
            results.append((price, predicted_units, revenue))

        best_price, best_units, best_revenue = max(results, key=lambda x: x[2])
        current_revenue = df["price"].mean() * df["units"].mean()
        delta = best_revenue - current_revenue

        risk_factor = country_risk_adjustment(db, p.market or "UK")
        adjusted_delta = delta / risk_factor

        risk_level = "high" if risk_factor > 1.2 else "medium" if risk_factor > 1 else "low"

        title = f"Optimise price for {p.name} in {p.market}"
        desc = (
            f"Recommended price: {best_price:.2f}. "
            f"Expected revenue change: {adjusted_delta:.2f}. "
            f"Elasticity: {elasticity:.3f}. "
            f"Risk factor: {risk_factor:.2f} ({risk_level})."
        )

        recs.append(
            models.Recommendation(
                business_id=business_id,
                title=title,
                description=desc,
                expected_profit_change=float(adjusted_delta),
                risk_level=risk_level,
            )
        )

    for r in recs:
        db.add(r)
    db.commit()
    return recs