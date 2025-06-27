# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 23:20:07 2025

@author: wee_cheong
"""

from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal

class PriceBase(BaseModel):
    time: datetime
    product: str = Field(..., max_length=50)
    price: Optional[Decimal] = Field(None, ge=0)

class PriceCreate(PriceBase):
    pass

class Price(PriceBase):
    id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PriceResponse(BaseModel):
    count: int
    data: List[Price]

class BulkPriceCreate(BaseModel):
    prices: List[PriceCreate]