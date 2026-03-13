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
    from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
        from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True