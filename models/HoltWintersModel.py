from statsmodels.tsa.holtwinters import ExponentialSmoothing
from models.BaseForecastModel import BaseForecastModel

class HoltWintersModel(BaseForecastModel):
    """
    Holt-Winters (Triple Exponential Smoothing) model for time series forecasting.

    Methods:
    --------
    fit(X, y):
        Fit the Holt-Winters model to the data.
    predict(X):
        Predict future values using the Holt-Winters model.
    """

    def __init__(self, seasonal_periods=12, trend='add', seasonal='add'):
        self.seasonal_periods = seasonal_periods
        self.trend = trend
        self.seasonal = seasonal
        self.model = None

    def fit(self, X, y):
        self.model = ExponentialSmoothing(y, seasonal_periods=self.seasonal_periods,
                                          trend=self.trend, seasonal=self.seasonal).fit()
        return self.model

    def predict(self, X):
        steps = len(X)
        forecast = self.model.forecast(steps=steps) # type: ignore
        return forecast
