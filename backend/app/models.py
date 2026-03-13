from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from DateTime import DateTime

class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    industry = Column(String, index=True)
    products = relationship("Product", back_populates="business")
    from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    name = Column(String, index=True)
    base_cost = Column(Float)
    market = Column(String, index=True)
    business = relationship("Business", back_populates="products")
    sales = relationship("Sale", back_populates="product")

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    date = Column(Date)
    units_sold = Column(Integer)
    price = Column(Float)
    product = relationship("Product", back_populates="sales")

class CountryIndicator(Base):
    __tablename__ = "country_indicators"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, index=True)
    date = Column(Date)
    inflation_rate = Column(Float)
    risk_score = Column(Float)
    currency_volatility = Column(Float)

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, index=True)
    title = Column(String)
    description = Column(String)
    expected_profit_change = Column(Float)
    risk_level = Column(String)
    status = Column(String, default="new")
    from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)