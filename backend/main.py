from fastapi import FastAPI, Request
import pickle
import numpy as np
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from db import HousingListing, get_db
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.options("/{full_path:path}")
async def preflight_handler():
    return {"message": "Preflight OK"}
 
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Response: {response.status_code}")
    return response
 
@app.get("/listings/")
def get_listings(db: Session = Depends(get_db)):
    """
    Gets all listings in Database
    """
    listings = db.query(HousingListing).all()
    return listings  

@app.get("/listing/{listing_id}")
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    """
    Gets listing from database by ID
    """
    listing = db.query(HousingListing).filter(HousingListing.listingid==listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Hello from Arjun!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)