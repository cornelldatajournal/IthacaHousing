import openrouteservice
import pandas as pd
from datetime import datetime
import numpy as np

api_key = "5b3ce3597851110001cf62480add9e6cc09a45b782be5f6b39437111"
client = openrouteservice.Client(key=api_key)

def batch_travel_times(origins, destinations, mode="foot-walking"):
    """
    Fetch travel times for multiple origins to multiple destinations using ORS Matrix API.
    
    Returns a dictionary {(lat, lon): [time_to_AgQuad, time_to_ArtsQuad, time_to_UrisHall]}.
    """
    try:
        response = client.distance_matrix(
            locations=[list(origin[::-1]) for origin in origins] + [list(dest[::-1]) for dest in destinations],
            profile=mode,
            metrics=["duration"],
            sources=list(range(len(origins))),
            destinations=list(range(len(origins), len(origins) + len(destinations)))
        )

        travel_times = response["durations"]

        return {origins[i]: travel_times[i] for i in range(len(origins))}

    except openrouteservice.exceptions.ApiError as e:
        print(f"⚠️ ORS API Error: {e}")
        return {}
    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")
        return {}

def run_travel_time_calculations(apartments_for_rent):
    """
    Runs the travel time location query call
    Adds a new column for walking time (sec)
    Args:
        apartment_for_rent: input dataframe with housing data
    """
    valid_listings = apartments_for_rent.dropna(subset=["latitude", "longitude"])
    rental_locations = list(zip(valid_listings["latitude"], valid_listings["longitude"]))

    campus_destinations = [
        (42.448662, -76.477313),  # Ag Quad
        (42.449163, -76.484725),  # Arts Quad
        (42.4471938, -76.4822012) # Uris Hall
    ]

    travel_times_dict = batch_travel_times(rental_locations, campus_destinations)

    def extract_travel_times(row, index):
        times = travel_times_dict.get((row["latitude"], row["longitude"]), [])
        return times[index] if len(times) > index else None

    for i, label in enumerate(["ag_quad_time", "arts_quad_time", "uris_hall_time"]):
        apartments_for_rent[label] = apartments_for_rent.apply(lambda row: extract_travel_times(row, i), axis=1)

    def get_mean_travel_time(row):
        times = [row["ag_quad_time"], row["arts_quad_time"], row["uris_hall_time"]]
        times = [t for t in times if t is not None] 
        return np.mean(times) if times else None

    apartments_for_rent["avg_walking_time"] = apartments_for_rent.apply(get_mean_travel_time, axis=1)

    return apartments_for_rent