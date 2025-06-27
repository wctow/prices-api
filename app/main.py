# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 23:22:03 2025

@author: wee_cheong
"""

from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from .routers import prices
from .database import create_tables
import os

app = FastAPI(
    title="ICE Prices API",
    description="Railway-hosted API for ICE commodity prices",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    api_key = os.getenv("API_KEY")
    if not api_key or credentials.credentials != api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return credentials.credentials

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/")
def root():
    return {"message": "ICE Prices API", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(prices.router, dependencies=[Depends(verify_api_key)])