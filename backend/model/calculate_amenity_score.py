#@title Amenity Scoring
import requests
import overpy
import geopy.distance
import math
import time

api = overpy.Overpass(url="https://overpass.kumi.systems/api/interpreter")

def fetch_amenities(latitude, longitude, radius=200, max_retries=5, timeout=20):
    """
    Fetches key amenities near a property using OverpassQL with optimized queries and retry handling.
    
    Parameters:
    - latitude, longitude: Coordinates of the rental property.
    - radius: Search radius in meters.
    - max_retries: Maximum retry attempts in case of rate limiting.

    Returns:
    - Dictionary with amenity types and distances.
    """
    
    query = f"""
    [out:json][timeout:100];
    (
        node(around:{radius},{latitude},{longitude})["amenity"];
        node(around:{radius},{latitude},{longitude})["shop"="supermarket"];
        node(around:{radius},{latitude},{longitude})["leisure"="park"];
    );
    out body;
    """

    for attempt in range(max_retries):
        try:
            result = api.query(query, timeout=timeout)
        except overpy.exception.OverpassTooManyRequests:
            wait_time = 2 ** attempt 
            print(f"⚠️ Rate limit hit. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"⚠️ Error fetching amenities: {e}")
            return None  

    amenities = {}
    for node in result.nodes:
        amenity_type = node.tags.get("amenity", node.tags.get("shop", node.tags.get("leisure", "unknown")))
        amenity_coords = (node.lat, node.lon)
        distance = geopy.distance.geodesic((latitude, longitude), amenity_coords).meters

        if amenity_type not in amenities or distance < amenities[amenity_type]:
            amenities[amenity_type] = distance

    return amenities

def compute_amenity_score(latitude, longitude):
    """
    Computes an overall amenity score based on proximity to key locations.

    Parameters:
    - amenities: Dictionary of amenity types and their distances.

    Returns:
    - Final score (1-100).
    """

    amenities = fetch_amenities(latitude, longitude)

    weights = {
        "public_transport": 25, "supermarket": 20, "restaurant": 15, "cafe": 15,
        "school": 15, "university": 15, "hospital": 15, "clinic": 15, "pharmacy": 15,
        "park": 10
    }
    alpha = 1.5

    score = 0
    for amenity, distance in amenities.items():
        if amenity in weights:
            distance_score = weights[amenity] * math.exp(-alpha * (distance / 1000))
            score += distance_score

    return round(score, 2)

def calculate_amenity_score(apartments_for_rent):
    """
    Calculates amenity score for each row
    Args:
        apartments_for_rent: dataframe with housing data
    """
    apartments_for_rent["amenities_score"] = apartments_for_rent.apply(
        lambda row: compute_amenity_score(row["latitude"], row["longitude"]), axis=1
    )

    return apartments_for_rent