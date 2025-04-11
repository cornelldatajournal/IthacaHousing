import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import numpy as np
import os
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent  
sys.path.append(str(BASE_DIR))

from main import app
from db import get_db, HousingListing

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_get_db():
    """
    Creates a mock object to use for each test case, overrides dependency function 
    """
    db = MagicMock()
    app.dependency_overrides[get_db] = lambda: db
    yield db
    app.dependency_overrides.clear()

def mock_listing(**kwargs):
    """
    Mock test setup
    """
    return HousingListing(
        listingid=1,
        rentamount=1000,
        predictedrent=950,
        rentamountadjusted=1000,
        latitude=42.44,
        longitude=-76.5,
        bedrooms=2,
        bathrooms=1.5,
        pets="Yes",
        avg_walking_time=10,
        transit_score=75,
        housingtype="Rent",
        **kwargs
    )

def mock_listings():
    """
    Returns a list of 10 mock HousingListing objects for test cases
    """
    return [
        mock_listing(listingid=1, bedrooms=1, bathrooms=1.0, pets="Yes", avg_walking_time=8, transit_score=70, housingtype="Rent"),
        mock_listing(listingid=2, bedrooms=2, bathrooms=1.5, pets="No", avg_walking_time=12, transit_score=60, housingtype="Room to Rent"),
        mock_listing(listingid=3, bedrooms=3, bathrooms=2.0, pets="Yes", avg_walking_time=15, transit_score=80, housingtype="Shared"),
        mock_listing(listingid=4, bedrooms=1, bathrooms=1.0, pets="No", avg_walking_time=9, transit_score=85, housingtype="Rent"),
        mock_listing(listingid=5, bedrooms=4, bathrooms=3.0, pets="Yes", avg_walking_time=5, transit_score=90, housingtype="Rent"),
        mock_listing(listingid=6, bedrooms=2, bathrooms=1.0, pets="No", avg_walking_time=18, transit_score=55, housingtype="Shared"),
        mock_listing(listingid=7, bedrooms=5, bathrooms=3.5, pets="Yes", avg_walking_time=7, transit_score=95, housingtype="Room to Rent"),
        mock_listing(listingid=8, bedrooms=3, bathrooms=2.5, pets="Yes", avg_walking_time=11, transit_score=65, housingtype="Rent"),
        mock_listing(listingid=9, bedrooms=1, bathrooms=1.0, pets="No", avg_walking_time=20, transit_score=50, housingtype="Shared"),
        mock_listing(listingid=10, bedrooms=2, bathrooms=1.5, pets="Yes", avg_walking_time=10, transit_score=75, housingtype="Rent"),
    ]


def test_get_listings(override_get_db):
    """
    Test case for getting all listings
    """
    override_get_db.query().all.return_value = mock_listings()
    res = client.get("/listings/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_top_ten_listings(override_get_db):
    """
    Test case for getting top 10 listings
    """
    override_get_db.query().order_by().limit().all.return_value = mock_listings()
    res = client.get("/top-ten-listings/")
    assert res.status_code == 200

def test_get_listing_beds(override_get_db):
    """
    Test case for getting all listing with n number of beds
    """
    override_get_db.query().filter().all.return_value = mock_listings()
    res = client.get("/listing/beds/2")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert data[0]["bedrooms"] == 2

def test_get_listing_baths(override_get_db):
    """
    Test case for getting all listing with n number of baths
    """
    override_get_db.query().filter().all.return_value = mock_listings()
    res = client.get("/listing/baths/3")  # 3/2 = 1.5
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert data[0]["bathrooms"] == 1.5

def test_get_listing_walk(override_get_db):
    """
    Test case for getting all listing with walkability score
    """
    override_get_db.query().filter().all.return_value = mock_listings()
    override_get_db.query().scalar.return_value = 15
    res = client.get("/listing/walks")
    assert res.status_code == 200
    data = res.json()
    assert all(listing["avg_walking_time"] < 15 for listing in data)


def test_get_listing_transit(override_get_db):
    """
    Test case for getting all listing with transit score
    """
    override_get_db.query().filter().all.return_value = mock_listings()
    override_get_db.query().scalar.return_value = 60
    res = client.get("/listing/transit")
    assert res.status_code == 200
    data = res.json()
    assert all(listing["transit_score"] > 60 for listing in data)

def test_get_listing_pet(override_get_db):
    """
    Test case for getting all listing with pet score
    """
    override_get_db.query().filter().all.return_value = mock_listings()
    res = client.get("/listing/pets")
    assert res.status_code == 200
    data = res.json()
    assert all(listing["pets"] == "Yes" for listing in data)


def test_get_listing_by_id(override_get_db):
    """
    Test case for getting a listing by its id
    """
    override_get_db.query().filter().first.return_value = mock_listings()
    res = client.get("/listing/1")
    assert res.status_code == 200
    data = res.json()
    assert data[0]["listingid"] == 1

def test_get_cluster_neighborhoods(override_get_db):
    """
    Test case for clustering neighborhoods
    """
    override_get_db.query().all.return_value = mock_listings()
    res = client.get("/clusters/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_heatmap_neighborhoods(override_get_db):
    """
    Test case for heatmap of neighborhoods
    """
    override_get_db.query().all.return_value = mock_listings()
    res = client.get("/heatmap/")
    assert res.status_code == 200
    assert "heat_data" in res.json()

def test_metrics_endpoint(override_get_db):
    """
    Test case for metrics for Prometheus/Grafana
    """
    override_get_db.query().all.return_value = mock_listings()
    res = client.get("/metrics")
    assert res.status_code == 200
    assert b"prediction_error" in res.content
