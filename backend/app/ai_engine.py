 from sqlalchemy.orm import Session
from . import models

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

        # Simple averages instead of pandas/numpy
        avg_price = sum(s.price for s in sales) / len(sales)
        avg_units = sum(s.units_sold for s in sales) / len(sales)
        current_revenue = avg_price * avg_units

        # Simple heuristic recommendation
        recommended_price = avg_price * 1.05  # +5%
        expected_units = avg_units * 0.98      # slight drop
        expected_revenue = recommended_price * expected_units

        delta = expected_revenue - current_revenue

        title = f"Optimise price for {p.name}"
        desc = (
            f"Suggested price: {recommended_price:.2f}. "
            f"Expected revenue change: {delta:.2f}. "
            f"Based on average historical performance."
        )

        recs.append(
            models.Recommendation(
                business_id=business_id,
                title=title,
                description=desc,
                expected_profit_change=float(delta),
                risk_level="medium",
            )
        )

    for r in recs:
        db.add(r)
    db.commit()

    return recs