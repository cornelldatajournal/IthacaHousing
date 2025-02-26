import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Numeric, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER=os.getenv("DB_USER")
DB_PWD=os.getenv("DB_PWD")
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
    createdate = Column(String)
    lastupdated = Column(String)
    safetyratings = Column(Text)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    avg_walking_time = Column(Numeric)
    ag_quad_time = Column(Numeric)
    arts_quad_time = Column(Numeric)
    uris_hall_time = Column(Numeric)
    transit_score = Column(Numeric)
    amenities_score = Column(Numeric)
    overallsafetyrating = Column(Numeric)
    overallsafetyratingpct = Column(Numeric)
    hasvalidcertificateofoccupancy = Column(Boolean)
    meetsminimumrequirements = Column(Boolean)
    exceedsrequirements = Column(Boolean)
    hasfireresistantconstructiontype = Column(Boolean)
    satisfiesapplicablecode = Column(Boolean)
    certificateexpirationdate = Column(String)
    sar_residuals = Column(Numeric)
    spatial_lag = Column(Numeric)
    predictedrent = Column(Numeric)
    differenceinfairvalue = Column(Numeric)

Base.metadata.create_all(bind=engine)
