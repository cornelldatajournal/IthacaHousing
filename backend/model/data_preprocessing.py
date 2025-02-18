import pandas as pd

# numerical_columns = [
#     "RentAmount", "Bedrooms", "Bathrooms", "driving_time", "transit_score", "amenities_score",
#     "OverallSafetyRating"
# ]

numerical_columns = [
    "RentAmount", "Bedrooms", "Bathrooms", "driving_time", "transit_score",
    "OverallSafetyRating"
]

categorical_columns = [
    "LengthAvailable", "RentType", "Pets", "HousingType"
]

def median_mode_imputation(apartments_for_rent):
    """
    Median Imputation for Numerical Columns
    Mode imputation for Categorical Columns
    Args:
        apartments_for_rent: dataframe with housing data
    """

    # For Numerical Categories, use Median Imputation
    for col in numerical_columns:
        apartments_for_rent[col] = pd.to_numeric(apartments_for_rent[col], errors="coerce")
        median = apartments_for_rent[col].median()
        apartments_for_rent.fillna({col: median}, inplace=True)

    # For Categorical Categories, use Mode Imputation
    for col in categorical_columns:
        mode = apartments_for_rent[col].mode()[0]
        apartments_for_rent.fillna({col: mode}, inplace=True)
    
    apartments_for_rent["Pets"] = apartments_for_rent["Pets"].map({"No": 0, "Yes": 1})

    return apartments_for_rent

def outlier_imputation(apartments_for_rent):
    """
    Median Imputation for Outliers
    Outliers defined by IQR fence (Median - 1.5*QI, Median + 1.5*Q3)
    Args:
        apartments_for_rent: dataframe with housing data
    """
    threshold = 1.5

    q1 = apartments_for_rent[numerical_columns].quantile(0.25)
    q3 = apartments_for_rent[numerical_columns].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - threshold * iqr
    upper_bound = q3 + threshold * iqr

    for col in numerical_columns:
        median_value = apartments_for_rent[col].median()
        apartments_for_rent[col] = apartments_for_rent[col].mask(
            (apartments_for_rent[col] < lower_bound[col]) | (apartments_for_rent[col] > upper_bound[col]),
            median_value
        )

    return apartments_for_rent