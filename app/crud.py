# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 23:20:33 2025

@author: wee_cheong
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func
from . import models, database
from datetime import date, datetime
from typing import Optional, List

def get_prices(db: Session, product: Optional[str] = None, start_date: Optional[date] = None, 
               end_date: Optional[date] = None, limit: int = 1000):
    query = db.query(database.PriceRecord)
    
    if product:
        query = query.filter(database.PriceRecord.product.ilike(f"%{product}%"))
    if start_date:
        query = query.filter(database.PriceRecord.time >= start_date)
    if end_date:
        query = query.filter(database.PriceRecord.time <= end_date)
    
    return query.order_by(desc(database.PriceRecord.time)).limit(limit).all()

def get_latest_prices(db: Session, products: Optional[List[str]] = None):
    subquery = db.query(
        database.PriceRecord.product,
        func.max(database.PriceRecord.time).label('max_time')
    ).group_by(database.PriceRecord.product)
    
    if products:
        subquery = subquery.filter(database.PriceRecord.product.in_(products))
    
    subquery = subquery.subquery()
    
    query = db.query(database.PriceRecord).join(
        subquery,
        and_(
            database.PriceRecord.product == subquery.c.product,
            database.PriceRecord.time == subquery.c.max_time
        )
    )
    
    return query.order_by(database.PriceRecord.product).all()

def bulk_upsert_prices(db: Session, prices: List[models.PriceCreate]):
    updated_count = 0
    inserted_count = 0
    
    for price_data in prices:
        existing = db.query(database.PriceRecord).filter(
            and_(
                database.PriceRecord.time == price_data.time,
                database.PriceRecord.product == price_data.product
            )
        ).first()
        
        if existing:
            existing.price = price_data.price
            existing.updated_at = datetime.utcnow()
            updated_count += 1
        else:
            db_price = database.PriceRecord(**price_data.dict())
            db.add(db_price)
            inserted_count += 1
    
    db.commit()
    return {"inserted": inserted_count, "updated": updated_count}