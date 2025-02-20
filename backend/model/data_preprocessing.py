import pandas as pd
import numpy as np

numerical_columns = [
    "LengthAvailable", "Bedrooms", "Bathrooms", "avg_walking_time", "transit_score", "amenities_score", "OverallSafetyRating"
]

categorical_columns = [
    "Pets"
]

def median_mode_imputation(X):
    """
    Median Imputation for Numerical Columns
    Mode imputation for Categorical Columns
    Args:
        X: dataframe with training housing data
    """

    # For Numerical Categories, use Median Imputation
    for col in numerical_columns:
        X[col] = pd.to_numeric(X[col], errors="coerce")
        median = X[col].median()
        X.fillna({col: median}, inplace=True)

    # For Categorical Categories, use Mode Imputation
    for col in categorical_columns:
        mode = X[col].mode()[0]
        X.fillna({col: mode}, inplace=True)
    
    X["Pets"] = X["Pets"].map({"No": 0, "Yes": 1})

    return X

def outlier_imputation(X):
    """
    Median Imputation for Outliers
    Outliers defined by IQR fence (Median - 1.5*QI, Median + 1.5*Q3)
    Args:
        X: dataframe with training housing data
    """
    threshold = 1.5

    q1 = X[numerical_columns].quantile(0.25)
    q3 = X[numerical_columns].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - threshold * iqr
    upper_bound = q3 + threshold * iqr

    for col in numerical_columns:
        median_value = X[col].median()
        X[col] = X[col].mask(
            (X[col] < lower_bound[col]) | (X[col] > upper_bound[col]),
            median_value
        )

    return X


def log_transform_prices(y):
    y = pd.to_numeric(y, errors='coerce')
    y = np.log(y)

    return y