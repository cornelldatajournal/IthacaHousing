import os
import psycopg2 

def psql_insert_copy():
    """
    Efficiently inserts data into PostgreSQL using COPY for performance optimization.
    """    

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
        avg_walking_time NUMERIC,
        ag_quad_time NUMERIC,
        arts_quad_time NUMERIC,
        uris_hall_time NUMERIC,
        transit_score NUMERIC,
        amenities_score NUMERIC,
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
        Spatial_Lag NUMERIC,
        PredictedRent NUMERIC,
        DifferenceinFairValue NUMERIC
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    
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
