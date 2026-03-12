from pydantic import BaseModel
from datetime import date

class BusinessCreate(BaseModel):
    name: str
    industry: str

class ProductCreate(BaseModel):
    business_id: int
    name: str
    base_cost: float
    market: str

class SaleCreate(BaseModel):
    product_id: int
    date: date
    units_sold: int
    price: float

class CountryIndicatorCreate(BaseModel):
    country: str
    date: date
    inflation_rate: float
    risk_score: float
    currency_volatility: float