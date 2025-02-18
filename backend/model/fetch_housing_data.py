import requests
import pandas as pd
import numpy as np
import time
from airflow.models import Variable
from airflow.utils.dates import days_ago
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
    housing_data_df["Coordinates"] = housing_data_df["Coordinates"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    housing_data_df["latitude"] = housing_data_df["Coordinates"].apply(lambda x: x["lat"])
    housing_data_df["longitude"] = housing_data_df["Coordinates"].apply(lambda x: x["lng"])

    housing_data_df.replace({"latitude": "", "longitude": "", "None": np.nan}, inplace=True)
    apartments_for_rent = housing_data_df.dropna(subset=["latitude", "longitude"])

    return apartments_for_rent