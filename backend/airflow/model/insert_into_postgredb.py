import os
import psycopg2 

def psql_insert_copy():
    """
    Completely replaces the existing housing_listings table with new data.
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

    # Ensure table exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS housing_listings (
        ListingId INTEGER PRIMARY KEY,
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
        SAR_Residuals NUMERIC,
        Spatial_Lag NUMERIC,
        PredictedRent NUMERIC,
        DifferenceinFairValue NUMERIC
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

    try:
        cursor.execute("TRUNCATE TABLE housing_listings RESTART IDENTITY CASCADE;")
        conn.commit()

        with open("./insert_into_postgres.csv", "r") as f:
            cursor.copy_expert("COPY housing_listings FROM STDIN WITH CSV HEADER", f)

        conn.commit()
        print("✅ Data replaced successfully!")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error replacing data: {e}")

    cursor.close()
    conn.close()
