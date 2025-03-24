import pandas as pd
import fetch_housing_data
import calculate_amenity_score
import calculate_travel_times_distance
import calculate_transit_score
import data_preprocessing
import extract_safety_features
import model_training
import spatial_regression
import insert_into_postgredb


DATA_PATH = "./insert_into_postgres.csv"

def housing_data_pipeline():
    """
    Call the Pipeline for Data Preprocessing for Apache Airflow
    """
    apartments_for_rent = fetch_housing_data.housing_data_preprocessing()
    
    apartments_for_rent = calculate_travel_times_distance.run_travel_time_calculations(apartments_for_rent)
    apartments_for_rent = calculate_transit_score.calculate_transit_score(apartments_for_rent)
    apartments_for_rent = calculate_amenity_score.calculate_amenity_score(apartments_for_rent)
    apartments_for_rent = extract_safety_features.calculate_safety_score(apartments_for_rent)

    X, y = model_training.define_X_Y_variables(apartments_for_rent)

    # X = data_preprocessing.median_mode_imputation(X)
    # X = data_preprocessing.outlier_imputation(X)

    y = data_preprocessing.log_transform_prices(y)
    # X = spatial_regression.spatial_regression(X, y, apartments_for_rent)

    apartments_for_rent = model_training.ml_durbin_model(X, y, apartments_for_rent)
    insert_into_postgredb.psql_insert_copy(apartments_for_rent)

    # apartments_for_rent.replace({r"\s+": " "}, inplace=True, regex=True)
    # apartments_for_rent.to_csv(DATA_PATH, index=False)
    return apartments_for_rent