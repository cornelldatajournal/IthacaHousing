import os
import pandas as pd
from sqlalchemy import create_engine, text
from shapely import LineString

def psql_insert_copy(df):
    DB_USER = os.getenv("DB_USER")
    DB_PWD = os.getenv("DB_PWD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_pre_ping=True,
        pool_recycle=1800, 
        connect_args={
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5
        }
    )

    for col in ["walk_routes", "bike_routes", "drive_routes"]:
        df[col] = df[col].apply(
            lambda x: x.wkt if isinstance(x, LineString) else x
        )

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w]", "", regex=True)  
        .str.replace("_pct", "pct")
    )
    with engine.begin() as conn: 
        df.head(0).to_sql("housing_listings", con=conn, if_exists="append", index=False)
        conn.execute(text("TRUNCATE TABLE housing_listings RESTART IDENTITY CASCADE;"))
        df.to_sql("housing_listings", con=conn, if_exists="append", index=False)  

    print("✅ Data inserted successfully using to_sql")

def confirmation():
    print("Confirmed Pipeline Complete!")