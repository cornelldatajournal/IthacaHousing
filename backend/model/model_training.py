from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import libpysal
from libpysal.weights import KNN
from spreg import ML_Lag
from sklearn.preprocessing import RobustScaler
import statsmodels.api as sm
import os
import psycopg2 
import io
import csv
from io import StringIO


"""PostgreSQL Variables"""
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

def train_model():
    """
    Defines X and Y Variables, scales variables throughto RobustScaler
    Log Transform Rental Prices, perform Spatial Regression on Coordinates, calculate residuals
    Trains Linear Regression Model
    Args:
        apartments_for_rent: dataframe with housing data
    """
    apartments_for_rent = pd.read_csv("./latest_processed_listings.csv")

    # X = apartments_for_rent[["LengthAvailable", "Pets", "Bedrooms", "Bathrooms", "driving_time", "transit_score", "amenities_score", "OverallSafetyRating"]]
    X = apartments_for_rent[["LengthAvailable", "Pets", "Bedrooms", "Bathrooms", "driving_time", "transit_score", "OverallSafetyRating"]]
    y = apartments_for_rent["RentAmount"]

    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(X)

    y = np.log(apartments_for_rent["RentAmount"].values)

    coords = apartments_for_rent[["latitude", "longitude"]].values
    knn_weights = KNN.from_array(coords, k=5) 

    sar_model = ML_Lag(y, X_scaled, w=knn_weights, name_y="Log RentAmount", name_x=X.columns.tolist())
    sar_residuals = sar_model.u  

    apartments_for_rent["SAR_Residuals"] = sar_residuals
    X["SAR_Residuals"] = sar_residuals 

    X = sm.add_constant(X)
    ols_model = sm.OLS(y, X).fit()

    y_pred = ols_model.predict(X)
    
    apartments_for_rent = find_residual_rental_amounts(y_pred, apartments_for_rent)

    psql_insert_copy(conn, apartments_for_rent)

    return apartments_for_rent

def find_residual_rental_amounts(y_pred, apartments_for_rent):
    """
    Predicts rental value based on SAR and Hedonic Regression Model
    Args:
        ols_model: fitted Model
        apartments_for_rent: dataframe with housing data
    """
    apartments_for_rent["PredictedRent"] = np.exp(y_pred)
    apartments_for_rent["DifferenceinFairValue"] = apartments_for_rent["PredictedRent"] - apartments_for_rent["RentAmount"]

    return apartments_for_rent

def psql_insert_copy(conn, apartments_for_rent):
    """
    Efficiently inserts data into PostgreSQL using COPY for performance optimization.
    """
    cursor = conn.cursor()
    
    # ADD amenities_score NUMERIC,
    create_table_query = """
    CREATE TABLE IF NOT EXISTS housing_listings (
        ListingId INTEGER,
        accountId INTEGER,
        DateAvailable TEXT,
        LengthAvailable TEXT,
        ListingAddress TEXT,
        UnitNumber TEXT,
        ListingCity TEXT,
        ListingZip TEXT,
        ShortDescription TEXT,
        LongDescription TEXT,
        RentAmount NUMERIC,
        RentType TEXT,
        Pets TEXT,
        Amenities TEXT,
        GenderPreference TEXT,
        Bedrooms NUMERIC,
        Bathrooms NUMERIC,
        ListingTypes TEXT,
        HousingType TEXT,
        GmapLatitude NUMERIC,
        GmapLongitude NUMERIC,
        Coordinates TEXT,
        LocationConfirmed BOOLEAN,
        ListingExpirationDate TEXT,
        Active BOOLEAN,
        ListingWithinCity TEXT,
        CreateDate TEXT,
        LastUpdated TEXT,
        safetyRatingAddress TEXT,
        ListingPhotos TEXT,
        SafetyRatings TEXT,
        latitude NUMERIC,
        longitude NUMERIC,
        driving_time NUMERIC,
        transit_score NUMERIC,
        OverallSafetyRating NUMERIC,
        OverallSafetyRatingPct NUMERIC,
        HasValidCertificateOfOccupancy NUMERIC,
        MeetsMinimumRequirements NUMERIC,
        ExceedsRequirements NUMERIC,
        HasFireResistantConstructionType NUMERIC,
        SatisfiesApplicableCode NUMERIC,
        CertificateExpirationDate TEXT,
        DateLastUpdated TEXT,
        FireProtection TEXT,
        NotificationSystems TEXT,
        EmergencyEgress TEXT,
        ApplicableCode TEXT,
        FireExtinguishers TEXT,
        ConstructionType TEXT,
        ValidCertificateOfCompliance NUMERIC,
        FireProtectionPct NUMERIC,
        NotificationSystemsPct NUMERIC,
        EmergencyEgressPct NUMERIC,
        ApplicableCodePct NUMERIC,
        FireExtinguishersPct NUMERIC,
        ConstructionTypePct NUMERIC,
        ValidCertificateOfCompliancePct NUMERIC,
        SAR_Residuals NUMERIC,
        PredictedRent NUMERIC,
        DifferenceinFairValue NUMERIC
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    
    apartments_for_rent.to_csv("./insert_into_postgres.csv", index=False, header=True, sep=",")

    try:
        with open("./insert_into_postgres.csv", "r") as f:
            cursor.copy_expert("COPY housing_listings FROM STDIN WITH CSV HEADER", f)
        conn.commit()
        print("✅ Data inserted successfully!")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error inserting data: {e}")

    cursor.close()
    conn.close()
