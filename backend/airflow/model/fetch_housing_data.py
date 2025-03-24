import requests
import pandas as pd
import numpy as np
import time
from airflow.models import Variable
from airflow.utils.dates import days_ago
import geocoder
import ast
import json

DATA_PATH = "./latest_listings.csv"

def fetch_active_listings():
    """Fetches Active Listings from Cornell Off-Campus Housing API"""
    url = "https://listings.offcampusliving.cornell.edu/api/activeListings"
    response = requests.get(url)
    data = response.json()
    
    housing_data_df = pd.DataFrame(data)
    housing_data_df["SafetyRatings"] = housing_data_df["SafetyRatings"].apply(
        lambda x: json.dumps(x) if isinstance(x, dict) else x
    )

    housing_data_df.to_csv(DATA_PATH, index=False)
    return housing_data_df

def housing_data_preprocessing():
    """Preprocesses House Data (extracts Lat, Lng)"""
    housing_data_df = pd.read_csv("latest_listings.csv")
    housing_data_df[['latitude', 'longitude']] = housing_data_df.apply(lambda row: pd.Series(geocoder.get_coordinates(row)), axis=1)
    housing_data_df.replace({"latitude": "", "longitude": "", "None": np.nan}, inplace=True)
    apartments_for_rent = housing_data_df.dropna(subset=["latitude", "longitude"])

    apartments_for_rent["Bedrooms"] = (
        apartments_for_rent["Bedrooms"]
        .replace("studio", 1)
        .apply(pd.to_numeric, errors="coerce")
    )
    apartments_for_rent["Bathrooms"] = pd.to_numeric(apartments_for_rent["Bathrooms"], errors='coerce')
    apartments_for_rent["combined_bedrooms_bathrooms"] = 1.5*apartments_for_rent["Bedrooms"]+apartments_for_rent["Bathrooms"]

    return apartments_for_rent