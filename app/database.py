# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 23:19:35 2025

@author: wee_cheong
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PriceRecord(Base):
    __tablename__ = "ice_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, nullable=False, index=True)
    product = Column(String(50), nullable=False, index=True)
    price = Column(Numeric(15, 6))
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (UniqueConstraint('time', 'product', name='unique_time_product'),)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)