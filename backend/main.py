from fastapi import FastAPI, Request, Response
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from db import HousingListing, get_db
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
import logging
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial import Voronoi
import pandas as pd
from fastapi.responses import JSONResponse
from shapely.geometry import Polygon
import geopandas as gpd
from sqlalchemy import func
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import Summary, Gauge
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

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

@app.get("/top-ten-listings/")
def get_top_ten_listings(db: Session = Depends(get_db)):
    """
    Gets top ten listings in Database
    """
    top_listings = db.query(HousingListing).order_by(
        ((HousingListing.predictedrent - HousingListing.rentamountadjusted) / HousingListing.rentamountadjusted).desc()
    ).limit(10).all()

    return top_listings 

@app.get("/bottom-ten-listings/")
def get_bottom_ten_listings(db: Session = Depends(get_db)):
    """
    Gets bottom ten listings in Database
    """
    bottom_listings = db.query(HousingListing).order_by(
        ((HousingListing.predictedrent - HousingListing.rentamountadjusted) / HousingListing.rentamountadjusted)
    ).limit(10).all()

    return bottom_listings 

@app.get("/clusters/")
def cluster_neighborhoods(db: Session = Depends(get_db)):
    """
    Clusters Neighborhoods by Price to find "natural pricing neighborhoods"
    """
    listings = db.query(HousingListing.latitude, HousingListing.longitude, HousingListing.rentamountadjusted).all()

    df = pd.DataFrame(listings, columns=["latitude", "longitude", "rentamount"])

    if df.empty:
        return {"error": "No listings found"}

    Z = linkage(df[["latitude", "longitude"]], method="ward")  
    df["hierarchal_cluster"] = fcluster(Z, t=8, criterion="maxclust")
    df["rentamount_scaled"] = (df["rentamount"] - df["rentamount"].min()) / (df["rentamount"].max() - df["rentamount"].min())

    return df.to_dict(orient="records")

@app.get("/heatmap/")
def heatmap_neighborhoods(db: Session = Depends(get_db)):
    """
    Heatmaps Neighborhoods by Price to find "natural pricing neighborhoods"
    """
    listings = db.query(HousingListing.latitude, HousingListing.longitude, HousingListing.rentamountadjusted).all()

    df = pd.DataFrame(listings, columns=["latitude", "longitude", "rentamount"])

    if df.empty:
        return {"error": "No listings found"}

    df["rentamount"] = pd.to_numeric(df["rentamount"], errors="coerce")
    df["rentamount_scaled"] = df["rentamount"] / df["rentamount"].max()

    df = df.dropna()  

    heat_data = df[["latitude", "longitude", "rentamount_scaled"]].values.tolist()

    return {"heat_data": heat_data}

@app.get("/voronoi/")
def voronoi_neighborhoods(db: Session = Depends(get_db)):
    """
    Generates Voronoi polygons based on rental pricing data.
    """
    listings = db.query(HousingListing.latitude, HousingListing.longitude, HousingListing.rentamountadjusted).all()

    df = pd.DataFrame(listings, columns=["latitude", "longitude", "rentamount"])

    df["rentamount"] = pd.to_numeric(df["rentamount"], errors="coerce")
    df.dropna(inplace=True)

    points = df[["longitude", "latitude"]].values  
    rent_values = df["rentamount"].values 

    vor = Voronoi(points)
    
    polygons = []
    for region in vor.regions:
        if not region or -1 in region:  
            continue
        polygon_coords = [vor.vertices[i] for i in region]
        polygons.append(Polygon(polygon_coords))

    gdf = gpd.GeoDataFrame({"geometry": polygons, "rent": rent_values[:len(polygons)]})
    gdf["rent_scaled"] = gdf["rent"] / gdf["rent"].max()  
    
    geojson = gdf.to_json()

    return JSONResponse(content=geojson)

@app.get("/listing/beds/{n_beds}")
def get_listing_beds(n_beds: int, db: Session = Depends(get_db)):
    """
    Gets listing from database by ID
    """
    if n_beds == 0:
        listings = db.query(HousingListing).all()
    elif n_beds != 5:
        listings = db.query(HousingListing).filter(HousingListing.bedrooms==n_beds).all()
    else:
        listings = db.query(HousingListing).filter(HousingListing.bedrooms>=n_beds).all()
    if not listings:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listings

@app.get("/listing/baths/{n_baths}")
def get_listing_baths(n_baths: int, db: Session = Depends(get_db)):
    """
    Gets listing from database by ID
    """
    n_baths = float(n_baths / 2)
    if n_baths == 0:
        listings = db.query(HousingListing).all()
    elif n_baths != 3:
        listings = db.query(HousingListing).filter(HousingListing.bathrooms==n_baths).all()
    else:
        listings = db.query(HousingListing).filter(HousingListing.bathrooms>=n_baths).all()
    if not listings:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listings

@app.get("/listing/walks")
def get_listing_walk(db: Session = Depends(get_db)):
    """
    Gets listing from database by ID
    """
    mean_walking_time = db.query(func.avg(HousingListing.avg_walking_time)).scalar()
    listings = db.query(HousingListing).filter(HousingListing.avg_walking_time<mean_walking_time).all()
    if not listings:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listings

@app.get("/listing/transit")
def get_listing_transit(db: Session = Depends(get_db)):
    """
    Gets listing from database by ID
    """
    mean_transit_score = db.query(func.avg(HousingListing.transit_score)).scalar()
    listings = db.query(HousingListing).filter(HousingListing.transit_score>mean_transit_score).all()
    if not listings:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listings

@app.get("/listing/pets")
def get_listing_pet(db: Session = Depends(get_db)):
    """
    Gets listing from database by ID
    """
    listings = db.query(HousingListing).filter(HousingListing.pets=="Yes").all()
    if not listings:
        raise HTTPException(status_code=404, detail="Listing not found")
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

"""
METRICS
Prometheus + Grafana
"""
PREDICTION_ERROR = Summary("prediction_error", "Absolute error between prediction and actual")

def get_prediction_error(db: Session):
    """
    Gets mean squared error from database
    """
    listings = db.query(HousingListing).all()
    errors = [(listing.rentamount - listing.predictedrent)**2 for listing in listings]
    mse = np.mean(errors)
    return mse

@app.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    """
    Gets metrics for Prometheus
    """
    mse = get_prediction_error(db)
    PREDICTION_ERROR.observe(mse)

    data = generate_latest()

    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

@app.get("/")
async def root():
    return {"message": "Hello from Arjun!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)