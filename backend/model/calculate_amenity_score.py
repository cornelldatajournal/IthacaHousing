#@title Amenity Scoring
import requests
import overpy
import geopy.distance
import math
import time
import os
import psycopg2 

import pandas as pd

api = overpy.Overpass(url="https://overpass.kumi.systems/api/interpreter")

def fetch_amenities(latitude, longitude, radius=500):
    """
    Fetches key amenities near a property using OverpassQL.
    Iterates through result nodes and finds the (amenity, distance) as a key-value pair
    Adds key-value pair to amenities dictionary if amenity type is not in dictionary or the distance is closer than distance


    Parameters:
    - latitude, longitude: Coordinates of the rental property.
    - radius: Search radius in meters.

    Returns:
    - Dictionary with amenity types and distances.
    """
    query = f"""
    [out:json][timeout:25];
    (
        node(around:{radius},{latitude},{longitude})["public_transport"];
        node(around:{radius},{latitude},{longitude})["shop"="supermarket"];
        node(around:{radius},{latitude},{longitude})["amenity"="restaurant"];
        node(around:{radius},{latitude},{longitude})["amenity"="cafe"];
        node(around:{radius},{latitude},{longitude})["amenity"="school"];
        node(around:{radius},{latitude},{longitude})["amenity"="university"];
        node(around:{radius},{latitude},{longitude})["amenity"="hospital"];
        node(around:{radius},{latitude},{longitude})["amenity"="clinic"];
        node(around:{radius},{latitude},{longitude})["amenity"="pharmacy"];
        node(around:{radius},{latitude},{longitude})["leisure"="park"];
    );
    out body;
    """
    try:
        result = api.query(query)
    except Exception as e:
        raise AmenitiesFetchingFailedError(f"Error fetching amenities: {e}")

    amenities = {}
    for node in result.nodes:
        amenity_type = node.tags.get("amenity", node.tags.get("shop", node.tags.get("leisure", "unknown")))
        amenity_coords = (node.lat, node.lon)
        distance = geopy.distance.geodesic((latitude, longitude), amenity_coords).meters

        if amenity_type not in amenities or distance < amenities[amenity_type]:
            amenities[amenity_type] = distance

    return amenities

def compute_amenity_score(listing_id, latitude, longitude):
    """
    Computes an overall amenity score based on proximity to key locations.

    Parameters:
    - amenities: Dictionary of amenity types and their distances.

    Returns:
    - Final score (1-100).
    """
    try:
        amenities = fetch_amenities(latitude, longitude)
    except Exception as e:
        print(f"Overpass API Error: {e}")
        fetched_score = postgresql_amenities_backup(listing_id)
        return fetched_score

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
        lambda row: compute_amenity_score(row["ListingId"], row["latitude"], row["longitude"]), axis=1
        # lambda row: postgresql_amenities_backup(row["ListingId"]), axis=1
    )
    # apartments_for_rent["amenities_score"] = amenity_scores

    return apartments_for_rent


def postgresql_amenities_backup(listing_id):
    """
    Fetches amenity score from database in case Turbo.ai fails

    Args:
        listing_id: the id of the listing from the database
    """
    DB_USER=os.getenv("DB_USER")
    DB_PWD=os.getenv("DB_PWD")
    DB_HOST=os.getenv("DB_HOST")
    DB_PORT=os.getenv("DB_PORT")
    DB_NAME=os.getenv("DB_NAME")

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PWD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    
    with conn:
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    amenities_score
                FROM housing_listings
                WHERE
                    listingid = %s
            """
            cursor.execute(query, (listing_id,))
            rows = cursor.fetchall()
    
    if not rows:
        return None 
    
    for row in rows:
        amenity_score = row[0]
        return amenity_score


def AmenitiesFetchingFailedError(BaseException):
    """
    Custom exception class if Amenity Fetching Fails.
    """
    pass

