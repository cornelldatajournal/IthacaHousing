import pandas as pd
from .fetch_housing_data import *
from .calculate_amenity_score import *
from .calculate_driving_distance import *
from .calculate_transit_score import *
from .data_preprocessing import *
from .extract_safety_features import *


DATA_PATH = "./latest_processed_listings.csv"

def housing_data_pipeline():
    """
    Call the Pipeline for Data Preprocessing for Apache Airflow
    """
    apartments_for_rent = housing_data_preprocessing()
    
    apartments_for_rent = run_travel_time_calculations(apartments_for_rent)
    apartments_for_rent = calculate_transit_score(apartments_for_rent)
    # apartments_for_rent = calculate_amenity_score(apartments_for_rent)
    apartments_for_rent = calculate_safety_score(apartments_for_rent)
    apartments_for_rent = median_mode_imputation(apartments_for_rent)
    apartments_for_rent = outlier_imputation(apartments_for_rent)

    apartments_for_rent.to_csv(DATA_PATH, index=False)
    return apartments_for_rent