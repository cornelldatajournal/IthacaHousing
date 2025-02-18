import openrouteservice
import pandas as pd
from datetime import datetime

api_key = "5b3ce3597851110001cf62480add9e6cc09a45b782be5f6b39437111"
client = openrouteservice.Client(key=api_key)

def batch_travel_times(origins, destination, mode="driving-car"):
    """
    Fetch travel times for multiple origins to a single destination using ORS Matrix API.

    - origins: List of (lat, lon) tuples.
    - destination: Single (lat, lon) tuple.
    - mode: Travel mode ("driving-car", "foot-walking", etc.).

    Returns a dictionary {ListingAddress: travel_time}.
    """
    try:
        response = client.distance_matrix(
            locations=[list(origin[::-1]) for origin in origins] + [list(destination[::-1])],
            profile=mode,
            metrics=["duration"],
            sources=list(range(len(origins))),
            destinations=[len(origins)]
        )

        travel_times = response["durations"][:-1]
        return {origins[i]: travel_times[i][0] for i in range(len(origins)-1)}

    except openrouteservice.exceptions.ApiError as e:
        print(f"⚠️ ORS API Error: {e}")
        return {}

def run_travel_time_calculations(apartments_for_rent):
    """
    Runs the travel time location query call
    Adds a new column for driving time (sec)
    Args:
        apartment_for_rent: input dataframe with housing data
    """
    rental_locations = list(zip(apartments_for_rent["latitude"], apartments_for_rent["longitude"]))

    destination = (42.4471938, -76.4822012)
    travel_times_dict = batch_travel_times(rental_locations, destination)

    apartments_for_rent["driving_time"] = apartments_for_rent.apply(
        lambda row: travel_times_dict.get((row["latitude"], row["longitude"]), None), axis=1
    )

    return apartments_for_rent