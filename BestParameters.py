import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings("ignore")

# Function to calculate RMSE
def calculate_rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

# Load your dataset
def load_data(file_path, column_name):
    data = pd.read_csv(file_path)
    data['Start Date'] = pd.to_datetime(data['Start Date'])
    return data[['Start Date', column_name]].dropna()

# Find best parameters for ARIMA
def find_best_arima_params(data, column_name, p_values, d_values, q_values):
    best_score, best_order = float("inf"), None
    best_model = None
    for p in p_values:
        for d in d_values:
            for q in q_values:
                try:
                    model = ARIMA(data[column_name], order=(p, d, q))
                    model_fit = model.fit()
                    aic = model_fit.aic
                    if aic < best_score:
                        best_score, best_order = aic, (p, d, q)
                        best_model = model_fit
                    print(f'ARIMA {p,d,q} AIC={aic}')
                except:
                    continue
    print(f'Best ARIMA Order: {best_order} AIC={best_score}')
    return best_order, best_model

# Find best parameters for SARIMA
def find_best_sarima_params(data, column_name, p_values, d_values, q_values, P_values, D_values, Q_values, m_values):
    best_score, best_order, best_seasonal_order = float("inf"), None, None
    best_model = None
    for p in p_values:
        for d in d_values:
            for q in q_values:
                for P in P_values:
                    for D in D_values:
                        for Q in Q_values:
                            for m in m_values:
                                try:
                                    order = (p, d, q)
                                    seasonal_order = (P, D, Q, m)
                                    model = SARIMAX(data[column_name], order=order, seasonal_order=seasonal_order)
                                    model_fit = model.fit()
                                    aic = model_fit.aic # type: ignore
                                    if aic < best_score:
                                        best_score = aic
                                        best_order = order
                                        best_seasonal_order = seasonal_order
                                        best_model = model_fit
                                    print(f'SARIMA {order} x {seasonal_order} AIC={aic}')
                                except:
                                    continue
    print(f'Best SARIMA Order: {best_order} x {best_seasonal_order} AIC={best_score}')
    return best_order, best_seasonal_order, best_model

# Find best parameters for Holt-Winters (Exponential Smoothing)
def find_best_holtwinters_params(data, column_name, seasonal_periods, trend_options, seasonal_options):
    best_score, best_params = float("inf"), None
    best_model = None
    for trend in trend_options:
        for seasonal in seasonal_options:
            try:
                model = ExponentialSmoothing(data[column_name], trend=trend, seasonal=seasonal, seasonal_periods=seasonal_periods)
                model_fit = model.fit()
                aic = model_fit.aic
                if aic < best_score:
                    best_score = aic
                    best_params = (trend, seasonal)
                    best_model = model_fit
                print(f'Holt-Winters {trend} {seasonal} AIC={aic}')
            except:
                continue
    print(f'Best Holt-Winters Trend: {best_params[0]} Seasonal: {best_params[1]} AIC={best_score}') # type: ignore
    return best_params, best_model

# Example Usage
if __name__ == "__main__":
    # Load your dataset
    file_path = 'processed/sixteen_and_over.csv'
    column_name = 'Total in employment level'
    
    data = load_data(file_path, column_name)
    
    # Define ARIMA parameters ranges
    p_values = [0, 1, 2, 3, 4]
    d_values = [0, 1, 2]
    q_values = [0, 1, 2]
    
    print("Finding best ARIMA parameters...")
    best_arima_order, best_arima_model = find_best_arima_params(data, column_name, p_values, d_values, q_values)
    
    # Define SARIMA parameters ranges
    P_values = [0, 1, 2]
    D_values = [0, 1]
    Q_values = [0, 1, 2]
    m_values = [12]  # Seasonal period (e.g., 12 for monthly data)
    
    print("\nFinding best SARIMA parameters...")
    best_sarima_order, best_seasonal_order, best_sarima_model = find_best_sarima_params(data, column_name, p_values, d_values, q_values, P_values, D_values, Q_values, m_values)
    
    # Define Holt-Winters parameters ranges
    seasonal_periods = 12  # Seasonal period (e.g., 12 for monthly data)
    trend_options = ['add', 'mul', None]  # Additive, multiplicative, or None
    seasonal_options = ['add', 'mul', None]
    
    print("\nFinding best Holt-Winters parameters...")
    best_hw_params, best_hw_model = find_best_holtwinters_params(data, column_name, seasonal_periods, trend_options, seasonal_options)

    print("Best ARIMA parameter:")
    print(best_arima_order)
    print("Best SARIMA parameter:")
    print(best_sarima_order, best_seasonal_order)
    print("Best Holt-Winters parameter:")
    print(best_hw_params)
    
    