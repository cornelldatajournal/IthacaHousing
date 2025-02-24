#@title Transit Scoring
import geopy.distance
import pandas as pd
import math
import requests

def find_nearest_stop(lat, lon, stops_df):
    """
    Finds the nearest bus stop based on latitude and longitude.

    Returns:
    - stop_name: Name of the closest bus stop.
    - distance_meters: Distance to the stop.
    """
    stops_df["distance_meters"] = stops_df.apply(
        lambda row: geopy.distance.geodesic((lat, lon), (row["lat"], row["long"])).meters, axis=1
    )

    nearest_stop = stops_df.loc[stops_df["distance_meters"].idxmin()]
    return {
        "stop_name": nearest_stop["name"],
        "distance_meters": nearest_stop["distance_meters"]
    }


def compute_transit_score(lat, lon, stops_df):
    """
    Computes a public transit accessibility score based on:
    - Distance to nearest stop
    - Real-time bus frequency
    - Active bus count
    - Delay penalties

    Returns a score from 1-100.
    """
    nearest = find_nearest_stop(lat, lon, stops_df)
    distance = nearest["distance_meters"]

    distance_score = 100 * math.exp(-1.5 * (distance / 1000))

    return round(distance_score, 2)

def fetch_bus_stops_in_ithaca():
    """
    Fetches Ithaca Bus Stops from Transit-Backend (credit: AppDev)
    Returns a dataframe with bus stop data
    """
    url = "https://transit-backend.cornellappdev.com/api/v1/allStops"
    response = requests.get(url)
    data = response.json()

    bus_stops = pd.DataFrame(data["data"])
    return bus_stops

def calculate_transit_score(apartments_for_rent):
    """
    Calls fetch_bus_stops_in_ithaca to get bus stops
    Calls compute_transit_score to calculate transit score for each address
    Args:
        apartments_for_rent: dataframe with housing data
    """
    bus_stops = fetch_bus_stops_in_ithaca()
    apartments_for_rent["transit_score"] = apartments_for_rent.apply(
        lambda row: compute_transit_score(row["latitude"], row["longitude"], bus_stops), axis=1
    )
    return apartments_for_rent