from models.BaseForecastModel import BaseForecastModel
from statsmodels.tsa.arima.model import ARIMA

class ARIMAModel(BaseForecastModel):
    """
    ARIMA model for time series forecasting.

    Methods:
    --------
    fit(X, y):
        Fit the ARIMA model to the data.
    predict(X):
        Predict future values using the ARIMA model.
    """

    def __init__(self, order=(5, 1, 0)):  # ARIMA(p,d,q)
        self.order = order
        self.model = None

    def fit(self, X, y):
        self.model = ARIMA(y, order=self.order).fit()
        return self.model

    def predict(self, X):
        steps = len(X)
        forecast = self.model.forecast(steps=steps) # type: ignore
        return forecast