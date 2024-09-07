from prophet import Prophet
from models.BaseForecastModel import BaseForecastModel

class ProphetModel(BaseForecastModel):
    """
    Prophet model for forecasting.

    Methods:
    --------
    fit(X, y):
        Fit the Prophet model to the data.
    predict(X):
        Predict future values using the Prophet model.
    """

    def __init__(self):
        self.model = Prophet()

    def fit(self, df):
        return self.model.fit(df)

    def predict(self, future):
        return self.model.predict(future)


