from models.BaseForecastModel import BaseForecastModel
from statsmodels.tsa.statespace.sarimax import SARIMAX

class SARIMAModel(BaseForecastModel):
    """
    SARIMA model for time series forecasting.

    Methods:
    --------
    fit(X, y):
        Fit the SARIMA model to the data.
    predict(X):
        Predict future values using the SARIMA model.
    """

    def __init__(self, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)):  # ARIMA(p,d,q) and seasonal_order(P,D,Q,s)
        self.order = order
        self.seasonal_order = seasonal_order
        self.model = None

    def fit(self, X, y):
        self.model = SARIMAX(y, order=self.order, seasonal_order=self.seasonal_order).fit()
        return self.model

    def predict(self, X):
        steps = len(X)
        forecast = self.model.forecast(steps=steps) # type: ignore
        return forecast
