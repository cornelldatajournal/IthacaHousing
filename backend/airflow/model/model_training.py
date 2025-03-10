import numpy as np
import statsmodels.api as sm
import pandas as pd

def define_X_Y_variables(apartments_for_rent):
    X = apartments_for_rent[["LengthAvailable", "Pets", "Bedrooms", "Bathrooms", "avg_walking_time", "transit_score", "amenities_score", "OverallSafetyRating"]]
    y = apartments_for_rent["RentAmount"]

    return X, y

def train_model(X, y, apartments_for_rent):
    """
    Defines X and Y Variables, scales variables throughto RobustScaler
    Log Transform Rental Prices, perform Spatial Regression on Coordinates, calculate residuals
    Trains Linear Regression Model
    Args:
        apartments_for_rent: dataframe with housing data
    """
    X = sm.add_constant(X)
    ols_model = sm.OLS(y, X).fit()

    y_pred = ols_model.predict(X)
    
    apartments_for_rent = find_residual_rental_amounts(y_pred, apartments_for_rent)

    return apartments_for_rent

def find_residual_rental_amounts(y_pred, apartments_for_rent):
    """
    Predicts rental value based on SAR and Hedonic Regression Model
    Args:
        ols_model: fitted Model
        apartments_for_rent: dataframe with housing data
    """
    apartments_for_rent["PredictedRent"] = np.exp(y_pred)
    apartments_for_rent["DifferenceinFairValue"] = apartments_for_rent["RentAmount"] - apartments_for_rent["PredictedRent"]

    return apartments_for_rent