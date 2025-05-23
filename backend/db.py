import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Numeric, Text, JSON, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
import json

DB_USER=os.getenv("DB_USER")
DB_PWD=os.getenv("DB_PWD", "3789mwPK")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class HousingListing(Base):
    """
    PostgreSQL Database Model for Housing Listings
    """
    __tablename__ = "housing_listings"
    
    listingid = Column(Integer, primary_key=True, index=True)
    accountid = Column(Integer)
    dateavailable = Column(String)
    lengthavailable = Column(String)
    listingaddress = Column(String)
    unitnumber = Column(String)
    listingcity = Column(String)
    listingzip = Column(String)
    shortdescription = Column(Text)
    longdescription = Column(Text)
    rentamount = Column(Numeric)
    rentamountadjusted = Column(Numeric)
    renttype = Column(String)
    pets = Column(String)
    amenities = Column(String)
    genderpreference = Column(String)
    bedrooms = Column(Numeric)
    bathrooms = Column(Numeric)
    listingtypes = Column(String)
    housingtype = Column(String)
    gmaplatitude = Column(Numeric)
    gmaplongitude = Column(Numeric)
    coordinates = Column(String)
    locationconfirmed = Column(Boolean)
    listingexpirationdate = Column(String)
    active = Column(Boolean)
    listingwithincity = Column(Boolean)
    listingphotos = Column(JSON)
    createdate = Column(String)
    lastupdated = Column(String)
    safetyratings = Column(Text)
    safetyratingaddress = Column(Text)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    transit_score = Column(Numeric)
    drive_time = Column(Numeric)
    walk_time = Column(Numeric)
    bike_time = Column(Numeric)
    drive_routes = Column(Text)
    walk_routes = Column(Text)
    bike_routes = Column(Text)
    amenities_score = Column(Numeric)
    overallsafetyrating = Column(Numeric)
    overallsafetyratingpct = Column(Numeric)
    hasvalidcertificateofoccupancy = Column(Boolean)
    meetsminimumrequirements = Column(Boolean)
    exceedsrequirements = Column(Boolean)
    hasfireresistantconstructiontype = Column(Boolean)
    satisfiesapplicablecode = Column(Boolean)
    certificateexpirationdate = Column(String)
    combined_bedrooms_bathrooms = Column(Numeric)
    nearest_neighbor_listingids = Column(Text)
    predictedrent = Column(Numeric)
    differenceinfairvalue = Column(Numeric)

Base.metadata.create_all(bind=engine)


