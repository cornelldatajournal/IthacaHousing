from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from db import HousingListing, get_db
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.get("/listings/")
def get_listings(db: Session = Depends(get_db)):
    """
    Gets all listings in Database
    """
    listings = db.query(HousingListing).all()
    return listings

@app.get("/listing/")
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    """
    Gets listing from database by ID
    """
    listing = db.query(HousingListing).filter(HousingListing.ListingId==listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)