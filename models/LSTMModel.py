from models.BaseForecastModel import BaseForecastModel
from darts.models import RNNModel
from darts import TimeSeries
import pandas as pd

class LSTMModel(BaseForecastModel):
    """
    LSTM model for time series forecasting using Darts.

    Methods:
    --------
    fit(X, y):
        Fit the LSTM model to the data.
    predict(X):
        Predict future values using the LSTM model.
    """

    def __init__(self, input_chunk_length=12, output_chunk_length=6, n_epochs=50):
        self.model = RNNModel(
            model="LSTM",
            input_chunk_length=input_chunk_length,
            output_chunk_length=output_chunk_length,
            n_epochs=n_epochs
        )

    def fit(self, X, y):
        # Ensure 'y' is a valid column from the DataFrame, not the values themselves
        if isinstance(y, pd.Series):
            y = y.to_frame()

        # Make sure 'y' has a valid column name and 'Start Date' is in X
        if 'Start Date' not in X.columns:
            raise ValueError("'Start Date' column is missing in the input DataFrame.")

        if y.columns[0] not in X.columns:
            # If 'y' column is not in X, join the two DataFrames
            X = X.join(y)

        # Ensure the time series is correctly constructed
        series = TimeSeries.from_dataframe(X, 'Start Date', y.columns[0])
        
        # Fit the model on the time series
        self.model.fit(series)
        
        
    def predict(self, X):
        forecast = self.model.predict(n=len(X))
        return forecast.values() # type: ignore
