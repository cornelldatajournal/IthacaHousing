import os
import pandas as pd
from sqlalchemy import create_engine, text

def psql_insert_copy(df):
    DB_USER = os.getenv("DB_USER")
    DB_PWD = os.getenv("DB_PWD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w]", "", regex=True)  
        .str.replace("_pct", "pct")
    )
    with engine.begin() as conn: 
        conn.execute(text("TRUNCATE TABLE housing_listings RESTART IDENTITY CASCADE;"))
        df.to_sql("housing_listings", con=conn, if_exists="append", index=False)  

    print("✅ Data inserted successfully using to_sql")

def confirmation():
    print("Confirmed Pipeline Complete!")