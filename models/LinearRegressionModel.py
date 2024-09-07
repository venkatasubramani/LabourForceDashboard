from sklearn.linear_model import LinearRegression
from models.BaseForecastModel import BaseForecastModel

class LinearRegressionModel(BaseForecastModel):
    """
    Linear Regression model for forecasting.

    Methods:
    --------
    fit(X, y):
        Fit the linear regression model to the data.
    predict(X):
        Predict future values using the linear regression model.
    """

    def __init__(self):
        self.model = LinearRegression()

    def fit(self, X, y):
        return self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)
