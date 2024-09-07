from models.BaseForecastModel import BaseForecastModel
import xgboost as xgb

class XGBoostModel(BaseForecastModel):
    """
    XGBoost model for time series forecasting.

    Methods:
    --------
    fit(X, y):
        Fit the XGBoost model to the data.
    predict(X):
        Predict future values using the XGBoost model.
    """

    def __init__(self):
        self.model = xgb.XGBRegressor()

    def fit(self, X, y):
        return self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)