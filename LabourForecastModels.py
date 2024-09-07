import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.metrics import mean_squared_error, mean_absolute_error
import random
import os
from models.ARIMAModel import ARIMAModel
from models.LinearRegressionModel import LinearRegressionModel
from models.ProphetModel import ProphetModel
from models.XGBoostModel import XGBoostModel
from models.HoltWintersModel import HoltWintersModel
from models.SARIMAModel import SARIMAModel
from models.LSTMModel import LSTMModel


class ForecastingManager:
    """
    Manager class for handling multiple forecasting models.

    Attributes:
    -----------
    models : dict
        A dictionary of forecasting models.
    output_folder : str
        Path to the output folder where results will be saved.

    Methods:
    --------
    add_model(name, model):
        Add a forecasting model to the manager.
    load_data(file_path):
        Load data from a CSV file.
    forecast_column(model, data, column_name, periods):
        Forecast a specific column using the provided model.
    calculate_metrics(y_true, y_pred):
        Calculate forecast error metrics.
    save_forecast(df, output_file):
        Save the forecast data to a CSV file.
    run_forecast(file_paths, periods):
        Run the forecasting process for all models and save results.
    """

    def __init__(self, output_folder='output'):
        self.models = {}
        self.output_folder = output_folder
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def add_model(self, name, model):
        """
        Add a forecasting model to the manager.

        Parameters:
        -----------
        name : str
            The name of the model.
        model : BaseForecastModel
            An instance of a class that inherits from BaseForecastModel.
        """
        self.models[name] = model

    @staticmethod
    def load_data(file_path):
        """
        Load data from a CSV file.

        Parameters:
        -----------
        file_path : str
            The path to the CSV file.

        Returns:
        --------
        pd.DataFrame
            The loaded data as a pandas DataFrame.
        """
        return pd.read_csv(file_path)



    def forecast_column(self, model, data, column_name, periods=60):
        """
        Forecast a specific column using the provided model.

        Parameters:
        -----------
        model : BaseForecastModel
            The forecasting model to use.
        data : pd.DataFrame
            The data to forecast on.
        column_name : str
            The name of the column to forecast.
        periods : int, optional
            The number of periods to forecast, default is 60.

        Returns:
        --------
        pd.DataFrame
            The forecasted data with actual values.
        """
        # Prepare the data: convert 'Start Date' to datetime and create the series
        data['Start Date'] = pd.to_datetime(data['Start Date'])
        X = data[['Start Date']]
        y = data[column_name]

        # Check for Prophet model
        if isinstance(model, ProphetModel):
            prophet_model = ProphetModel()
            df = data[['Start Date', column_name]].rename(
                columns={'Start Date': 'ds', column_name: 'y'})
            df['ds'] = pd.to_datetime(df['ds'])
            prophet_model.fit(df)

            future = prophet_model.model.make_future_dataframe(periods=periods, freq='ME')
            forecast = prophet_model.predict(future)
            forecast = forecast.rename(columns={'ds': 'Start Date'})
            forecast = forecast[['Start Date', 'yhat', 'yhat_lower', 'yhat_upper']]

            # Align the actual values with forecast
            actual_values = df['y'].tolist()
            forecast['Actual'] = actual_values + [None] * (forecast.shape[0] - len(actual_values))

            return forecast

        # For Darts-based models: LSTM
        elif isinstance(model, (LSTMModel)):
            # Convert the data to a TimeSeries object (required for Darts models)
            # series = TimeSeries.from_dataframe(data, 'Start Date', column_name)

            # Fit the model on historical data#
            
            fit_model = model.fit(X, y)

            # Forecast future values for the specified number of periods
            future_dates = pd.date_range(start=data['Start Date'].max(), periods=periods + 1, freq='ME')[1:]
            
            # Generate predictions for the future
            forecast_series = model.predict(future_dates)
            predictions = forecast_series
            
            if len(predictions.shape) > 1 and predictions.shape[1] == 1:
                # Flatten 2D arrays (like LSTM) to 1D
                predictions = predictions.flatten()
            
            for i in range(len(predictions)):
                predictions[i] = predictions[i]*random.uniform(0.995, 1.005)
            # Prepare DataFrame with future dates and predictions
            forecast_df = pd.DataFrame({
                'Start Date': future_dates,
                'Prediction': predictions
            })
            
            historical_predictions = model.predict(X)
            if len(historical_predictions.shape) > 1 and historical_predictions.shape[1] == 1:
                # Flatten 2D arrays (like LSTM) to 1D
                historical_predictions = historical_predictions.flatten()
                
            # Add historical data to the DataFrame (combine with actual values)
            historical_df = pd.DataFrame({
                'Start Date': data['Start Date'],
                'Prediction': historical_predictions, # type: ignore
                'Actual': y
            })

            # Concatenate historical data and forecast
            combined_df = pd.concat([historical_df, forecast_df], ignore_index=True)

            return combined_df

        # Other traditional models like Linear Regression
        else:
            X = np.array(pd.to_datetime(data['Start Date']).map(datetime.toordinal)).reshape(-1, 1)
            y = data[column_name].values
            fit_model = model.fit(X, y)

            # Use the same future dates as Prophet's future dates
            last_date = data['Start Date'].max()
            future_dates = pd.date_range(start=last_date, periods=periods + 1, freq='ME')[1:]
            future_X = np.array(future_dates.map(datetime.toordinal)).reshape(-1, 1)
            predictions = model.predict(future_X)
            print('---------------------------------')
            print(fit_model.__class__.__name__)
            # Create DataFrame for future dates and predictions
            if isinstance(model, LinearRegressionModel)==False:
                for i in range(len(predictions)):
                    predictions[i] = predictions[i]*random.uniform(0.995, 1.005)
                    
            forecast_df = pd.DataFrame({
                'Start Date': future_dates,
                'Prediction': predictions
            })
            
            if isinstance(model, LinearRegressionModel)==True or isinstance(model, XGBoostModel)==True:
                predictions = model.predict(X)
            else:
                predictions = fit_model.fittedvalues
                

            # Add historical data to the same DataFrame (combine with actual values)
            historical_df = pd.DataFrame({
                'Start Date': data['Start Date'],
                'Prediction': predictions,
                'Actual': y
            })

            # Concatenate historical data and forecast
            combined_df = pd.concat([historical_df, forecast_df], ignore_index=True)

            return combined_df



    @staticmethod
    def calculate_metrics(y_true, y_pred):
        """
        Calculate forecast error metrics.

        Parameters:
        -----------
        y_true : array-like
            The actual values.
        y_pred : array-like
            The predicted values.

        Returns:
        --------
        dict
            A dictionary containing RMSE, MAE, and MAPE.
        """
        metrics = {
            'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
            'MAE': mean_absolute_error(y_true, y_pred),
            'MAPE': np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        }
        return metrics

    def save_forecast(self, df, output_file):
        """
        Save the forecast data to a CSV file.

        Parameters:
        -----------
        df : pd.DataFrame
            The forecast data.
        output_file : str
            The path to the output CSV file.
        """
        df.to_csv(output_file, index=False)

    def run_forecast(self, file_paths, periods=60):
        """
        Run the forecasting process for all models and save results.

        Parameters:
        -----------
        file_paths : list of str
            List of file paths to load the data from.
        periods : int, optional
            The number of periods to forecast, default is 60.
        """
        metrics_comparison = []

        for file_path in file_paths:
            data = self.load_data(file_path)
            base_name = os.path.basename(file_path).split('.')[0]

            for model_name, model in self.models.items():
                # Assuming first three columns are identifiers (Start Date,
                # etc.)
                for column in data.columns[3:]:
                    forecast_df = self.forecast_column(
                        model, data, column, periods)
                    output_file = os.path.join(
                        self.output_folder, f"{base_name}_{model_name}_{column}_forecast.csv")
                    self.save_forecast(forecast_df, output_file)

                    # Calculate metrics only for actual vs predicted part
                    y_true = forecast_df['Actual'].dropna().values
                    y_pred = forecast_df['yhat'].dropna(
                    ).values if 'yhat' in forecast_df else forecast_df['Prediction'].dropna().values

                    # Align lengths
                    if len(y_true) > len(y_pred):
                        y_true = y_true[-len(y_pred):]
                    elif len(y_pred) > len(y_true):
                        y_pred = y_pred[-len(y_true):]

                    metrics = self.calculate_metrics(y_true, y_pred)
                    metrics['Model'] = model_name
                    metrics['Column'] = column
                    metrics_comparison.append(metrics)

        # Save the metrics comparison
        metrics_df = pd.DataFrame(metrics_comparison)
        metrics_df.to_csv(
            os.path.join(
                self.output_folder,
                "metrics_comparison.csv"),
            index=False)


# Example usage:
manager = ForecastingManager(output_folder='model_results')
manager.add_model('linear_regression', LinearRegressionModel())
manager.add_model('prophet', ProphetModel())
manager.add_model('arima', ARIMAModel(order=(2, 0, 2)))
manager.add_model('sarima', SARIMAModel(order=(3, 0, 0), seasonal_order=(0, 1, 0, 12)))
manager.add_model('holt_winters', HoltWintersModel(trend='add'))
manager.add_model('xgboost', XGBoostModel())
manager.add_model('lstm', LSTMModel(input_chunk_length=12, output_chunk_length=6, n_epochs=1))

manager.run_forecast(['processed/sixteen_and_over.csv',
                     'processed/sixteen_and_sixty_four.csv'], periods=60)
