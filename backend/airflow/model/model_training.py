import numpy as np
import statsmodels.api as sm
import pandas as pd
from spreg import ML_Lag
from libpysal.weights import KNN

def define_X_Y_variables(apartments_for_rent):
    X = apartments_for_rent[["LengthAvailable", "Pets", "combined_bedrooms_bathrooms", "avg_walking_time", "transit_score", "amenities_score", "OverallSafetyRating"]]
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

def ml_durbin_model(X, y, apartments_for_rent):
    """
    Defines X and Y Variables, scales variables throughto RobustScaler
    Log Transform Rental Prices, perform Spatial Regression on Coordinates, calculate residuals
    Trains Spatial Durbin Model
    Args:
        apartments_for_rent: dataframe with housing data
    """
    coords = apartments_for_rent[["latitude", "longitude"]].values
    knn_weights = KNN.from_array(coords, k=5)

    sdm_model = ML_Lag(
        y,
        X,
        w=knn_weights,
        name_y="Log RentAmount",
        name_x=X.columns.tolist(),
        slx_lags=1
    )

    y_pred = sdm_model.predy
    
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