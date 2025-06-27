# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 23:21:33 2025

@author: wee_cheong
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from .. import crud, models, database

router = APIRouter(prefix="/prices", tags=["prices"])

@router.get("/", response_model=models.PriceResponse)
def get_prices(
    product: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = Query(1000, ge=1, le=10000),
    db: Session = Depends(database.get_db)
):
    try:
        prices = crud.get_prices(db, product, start_date, end_date, limit)
        return models.PriceResponse(count=len(prices), data=prices)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/latest", response_model=models.PriceResponse)
def get_latest_prices(
    products: Optional[str] = Query(None),
    db: Session = Depends(database.get_db)
):
    try:
        product_list = products.split(',') if products else None
        prices = crud.get_latest_prices(db, product_list)
        return models.PriceResponse(count=len(prices), data=prices)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/bulk")
def bulk_upload_prices(
    bulk_data: models.BulkPriceCreate,
    db: Session = Depends(database.get_db)
):
    try:
        result = crud.bulk_upsert_prices(db, bulk_data.prices)
        return {"message": f"Processed {len(bulk_data.prices)} records", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")