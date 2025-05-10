from fastapi import FastAPI
from fastapi.responses import JSONResponse
from shapely.geometry import Polygon
import geopandas as gpd
import pandas as pd
import os
import numpy as np
import ast
from shapely.geometry import mapping

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "TompkinsCountyData.csv")

def geometry_to_polygon(geom):
    geom = ast.literal_eval(geom)
    if geom and "rings" in geom:
        return Polygon(geom.get("rings")[0])
    return None

def load_and_prepare_data():
    """
    Get Data from CSV and Convert coordinate systems
    """
    df = pd.read_csv(DATA_PATH)
    df["geometry"] = df["geometry"].apply(geometry_to_polygon)
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:3857")
    gdf = gdf.to_crs("EPSG:4326")

    gdf["ValuePerAcre"] = gdf["ASMT"] / gdf["CALCACRES"]
    gdf["RedevelopmentIndex"] = gdf["LAND"]/gdf["ASMT"]

    return gdf

def filter_ithaca_lots(gdf):
    """
    Get Lots only in Ithaca
    """
    ithaca_munis = ["CITY OF ITHACA", "VILLAGE OF CAYUGA HEIGHTS", "VILLAGE OF DRYDEN"]
    return gdf[gdf["MUNI"].isin(ithaca_munis)].copy()

def add_zoning_metadata(gdf):
    """
    Convert zoning codes to zoning categories
    """
    zoning_dict = {
        "R-1a": "Residential", "R-1b": "Residential", "R-2a": "Residential",
        "R-2b": "Residential", "R-2c": "Residential", "R-3a": "Residential",
        "R-3aa": "Residential", "R-3b": "Residential", "R-U": "Residential",
        "MH-1": "Residential-Mobile Home", "B-1a": "Restricted Business",
        "B-1b": "Restricted Business", "B-2a": "General Business",
        "B-2b": "General Business", "B-2c": "General Business",
        "B-2d": "General Business", "B-4": "Service Business",
        "B-5": "Service Business", "CBD": "Central Business",
        "CBD-50": "Central Business", "CBD-60": "Central Business",
        "I-1": "Industrial", "P-1": "Public and Institutional",
        "C-SU": "Courthouse Special Use", "U-1": "West End Development",
        "WEDZ-1": "West End Development", "SW-1": "Southwest",
        "CR-1": "Collegetown Residential 1", "CR-2": "Collegetown Residential 2",
        "CR-3": "Collegetown Residential 3", "CR-4": "Collegetown Residential 4",
        "MU-1": "Mixed Use 1", "MU-2": "Mixed Use 2",
        "WE/WFD": "West End/Waterfront District", "CSD": "Cherry Street District",
        "ND": "Newman District", "MD": "Market District",
        "SHOD": "South Hill Overlay District", " ": "Not Zoned"
    }

    zoning_segment_dict = {
        "R-1a": "Residential", "R-1b": "Residential", "R-2a": "Residential",
        "R-2b": "Residential", "R-2c": "Residential", "R-3a": "Residential",
        "R-3aa": "Residential", "R-3b": "Residential", "R-U": "Residential",
        "MH-1": "Residential", "B-1a": "Business", "B-1b": "Business",
        "B-2a": "Business", "B-2b": "Business", "B-2c": "Business",
        "B-2d": "Business", "B-4": "Business", "B-5": "Business",
        "CBD": "Business", "CBD-50": "Business", "CBD-60": "Business",
        "I-1": "Industrial", "P-1": "Government", "C-SU": "Government",
        "U-1": "Residential", "WEDZ-1": "Residential", "SW-1": "Southwest",
        "CR-1": "Residential", "CR-2": "Residential", "CR-3": "Residential",
        "CR-4": "Residential", "MU-1": "Mixed Use", "MU-2": "Mixed Use",
        "WE/WFD": "Government", "CSD": "Mixed Use", "ND": "Residential",
        "MD": "Business", "SHOD": "Residential", " ": "Not Zoned"
    }

    gdf["ZoningCode"] = gdf["ZONING"].map(zoning_dict)
    gdf["ZoningCategory"] = gdf["ZONING"].map(zoning_segment_dict)
    return gdf


def sanitize_for_json(df: pd.DataFrame) -> list[dict]:
    """
    Remove nans, infinities, etc for JSON Dumping
    """
    df["geometry"] = df["geometry"].apply(lambda geom: mapping(geom) if geom else None)
    cleaned = df.replace([np.nan, np.inf, -np.inf], None)
    return cleaned.to_dict(orient="records")