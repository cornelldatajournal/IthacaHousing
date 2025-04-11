import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import numpy as np
import os
from pathlib import Path
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


BASE_DIR = Path(__file__).resolve().parent.parent  
sys.path.append(str(BASE_DIR))

from main import app
from db import get_db, HousingListing, Base

TEST_DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/test_db"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Create tables once for all tests"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def override_get_db():
    """Override get_db for tests"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture(scope="function")
def client(override_get_db):
    app.dependency_overrides[get_db] = lambda: override_get_db
    return TestClient(app)

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


def test_get_listings(client, override_get_db):
    """
    Test case for getting all listings
    """
    db = override_get_db
    db.add_all(mock_listings())
    db.commit()

    res = client.get("/listings/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_top_ten_listings(client, override_get_db):
    """
    Test case for getting top 10 listings
    """
    db = override_get_db
    db.add_all(mock_listings())
    db.commit()

    res = client.get("/top-ten-listings/")
    assert res.status_code == 200
    data = res.josn()
    assert isinstance(data, list)
    assert len(data) == 10

def test_get_listing_beds(client, override_get_db):
    """
    Test case for getting all listing with n number of beds
    """
    db = override_get_db
    db.add_all(mock_listings())
    db.commit()

    res = client.get("/listing/beds/2")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert all(listing["bedrooms"] == 2 for listing in data)
    

def test_get_listing_baths(client, override_get_db):
    """
    Test case for getting all listing with n number of baths
    """
    db = override_get_db
    db.add_all(mock_listings())
    db.commit()

    res = client.get("/listing/baths/3")  # 3/2 = 1.5
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert data[0]["bathrooms"] == 1.5

def test_get_listing_walk(client, override_get_db):
    """
    Test case for getting all listing with walkability score
    """
    db = override_get_db
    db.add_all(mock_listings())
    db.commit()

    res = client.get("/listing/walks")
    assert res.status_code == 200
    data = res.json()
    assert all(listing["avg_walking_time"] < 15 for listing in data)


def test_get_listing_transit(client, override_get_db):
    """
    Test case for getting all listing with transit score
    """
    db = override_get_db
    db.add_all(mock_listings())
    db.commit()

    res = client.get("/listing/transit")
    assert res.status_code == 200
    data = res.json()
    assert all(listing["transit_score"] > 60 for listing in data)

def test_get_listing_pet(client, override_get_db):
    """
    Test case for getting all listing with pet score
    """
    db = override_get_db
    db.add_all(mock_listings())
    db.commit()

    res = client.get("/listing/pets")
    assert res.status_code == 200
    data = res.json()
    assert all(listing["pets"] == "Yes" for listing in data)


def test_get_listing_by_id(client, override_get_db):
    """
    Test case for getting a listing by its id
    """
    db = override_get_db
    db.add_all(mock_listings())
    db.commit()

    res = client.get("/listing/1")
    assert res.status_code == 200
    data = res.json()
    assert data[0]["listingid"] == 1

def test_get_cluster_neighborhoods(client, override_get_db):
    """
    Test case for clustering neighborhoods
    """
    db = override_get_db
    db.add_all(mock_listings())
    db.commit()

    res = client.get("/clusters/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_heatmap_neighborhoods(client, override_get_db):
    """
    Test case for heatmap of neighborhoods
    """
    db = override_get_db
    db.add_all(mock_listings())
    db.commit()

    res = client.get("/heatmap/")
    assert res.status_code == 200
    assert "heat_data" in res.json()

def test_metrics_endpoint(client, override_get_db):
    """
    Test case for metrics for Prometheus/Grafana
    """
    db = override_get_db
    db.add_all(mock_listings())
    db.commit()

    res = client.get("/metrics")
    assert res.status_code == 200
    assert b"prediction_error" in res.content
