from abc import ABC, abstractmethod

class BaseForecastModel(ABC):
    """
    Abstract base class for all forecasting models.

    Methods:
    --------
    fit(X, y):
        Fit the model to the data.
    predict(X):
        Predict future values.
    """

    @abstractmethod
    def fit(self, X, y):
        pass

    @abstractmethod
    def predict(self, X):
        pass