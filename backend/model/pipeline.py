import pandas as pd
from .fetch_housing_data import *
from .calculate_amenity_score import *
from .calculate_travel_times_distance import *
from .calculate_transit_score import *
from .data_preprocessing import *
from .extract_safety_features import *
from .model_training import *
from .spatial_regression import *


DATA_PATH = "./insert_into_postgres.csv"

def housing_data_pipeline():
    """
    Call the Pipeline for Data Preprocessing for Apache Airflow
    """
    apartments_for_rent = housing_data_preprocessing()
    
    apartments_for_rent = run_travel_time_calculations(apartments_for_rent)
    apartments_for_rent = calculate_transit_score(apartments_for_rent)
    apartments_for_rent = calculate_amenity_score(apartments_for_rent)
    apartments_for_rent = calculate_safety_score(apartments_for_rent)

    X, y = define_X_Y_variables(apartments_for_rent)

    X = median_mode_imputation(X)
    X = outlier_imputation(X)

    y = log_transform_prices(y)
    X = spatial_regression(X, y, apartments_for_rent)

    apartments_for_rent = train_model(X, y, apartments_for_rent)

    apartments_for_rent.replace({r"\s+": " "}, inplace=True, regex=True)
    apartments_for_rent.to_csv(DATA_PATH, index=False)
    return apartments_for_rent