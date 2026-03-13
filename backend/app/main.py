from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from . import models

# Import your auth router (FIX)
from .auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DhanaaDev API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# BUSINESS ENDPOINTS
# -------------------------

@app.post("/business")
def create_business(name: str, industry: str, db: Session = Depends(get_db)):
    b = models.Business(name=name, industry=industry)
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


# -------------------------
# PRODUCT ENDPOINTS
# -------------------------

@app.post("/product")
def create_product(
    business_id: int, name: str, base_cost: float, market: str,
    db: Session = Depends(get_db)
):
    p = models.Product(
        business_id=business_id,
        name=name,
        base_cost=base_cost,
        market=market
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


# -------------------------
# SALES ENDPOINTS
# -------------------------

@app.post("/sale")
def create_sale(
    product_id: int, date: str, units_sold: int, price: float,
    db: Session = Depends(get_db)
):
    from datetime import datetime
    s = models.Sale(
        product_id=product_id,
        date=datetime.fromisoformat(date).date(),
        units_sold=units_sold,
        price=price
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


# -------------------------
# COUNTRY INDICATOR ENDPOINTS
# -------------------------

@app.post("/country-indicator")
def create_country_indicator(
    country: str, date: str, inflation_rate: float,
    risk_score: float, currency_volatility: float,
    db: Session = Depends(get_db)
):
    from datetime import datetime
    ci = models.CountryIndicator(
        country=country,
        date=datetime.fromisoformat(date).date(),
        inflation_rate=inflation_rate,
        risk_score=risk_score,
        currency_volatility=currency_volatility
    )
    db.add(ci)
    db.commit()
    db.refresh(ci)
    return ci


# -------------------------
# AI ENGINE ENDPOINTS
# -------------------------

@app.post("/ai/generate-recommendations")
def generate_recs(business_id: int, db: Session = Depends(get_db)):
    return ai_engine.generate_recommendations(db, business_id)


@app.get("/recommendations")
def list_recs(business_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Recommendation)
        .filter(models.Recommendation.business_id == business_id)
        .all()
    )


# -------------------------
# AUTH ROUTER (FIXED)
# -------------------------

app.include_router(auth_router)