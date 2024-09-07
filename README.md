# Labour Force Dashboard

This project is a Labour Force Dashboard built using Python and Dash. The dashboard provides insights into labour force data, including various metrics for different age groups.

## Features

- Dropdown menus to select datasets and columns.
- Visualization of labour force data.
- Download options for processed data.
- Linear regression model, Prophet & XGBoost for data analysis.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/labour-force-dashboard.git
    cd labour-force-dashboard
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On macOS/Linux
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:8050/` to view the dashboard.

## Project Structure

- `app.py`: The main application file that initializes the Dash app, sets up the layout, and defines the callbacks for interactivity.
- `DashboardManager.py`: Contains the logic for managing the dashboard components, including dropdowns and data processing functions.
- `FileHandler.py`: Handles the path and dynamically edit the path during run-time based on the dropdown selection.
- `LabourSurveyDataPrep`: This is responsible for getting the processed data from the raw data.
- `LabourForecastModels`: This is responsible for the forecasting the data with different timeseries algorithm
- `Models/`: This folder contains the different model implementations and the basemodel.
- `PlotManager.Py`: This is responsible for reusing the code of the plot for different pots.
- `requirements.txt`: A list of required Python packages for the project.
- `input/`: A directory to store input data files (e.g., Excel files).
- `processed/`: A directory for storing processed data files
- `README.md`: This file, providing an overview and documentation for the project.

### Detailed File Descriptions

#### `app.py`
This is the main entry point of the application. It:
- Initializes the Dash app.
- Sets up the layout of the dashboard, including dropdowns and graphs.
- Defines the callbacks that handle user interactions and update the dashboard components.

#### `DashboardManager.py`
This file contains the core logic for managing the dashboard. It includes:
- Functions to read and process the input data.
- Functions to handle dropdown selections and update the dashboard accordingly.
- Data processing functions such as `calculate_dates` to compute start and end dates from dataset identifiers.

#### `requirements.txt`
This file lists all the Python packages required to run the project. It includes:
- `dash`: The web application framework used to build the dashboard.
- `pandas`: For data manipulation and analysis.
- `dateutil`: For parsing dates.
- `autopep8`: For code formatting.

#### `input/`
This directory is intended to store raw input data files.

#### `processed/`
This directory is used for storing the processed data files.

#### `model_results/`
This directory is used for saving the model results.

#### `README.md`
This file provides an overview of the project, installation instructions, usage details, project structure, code formatting guidelines, contribution instructions, license information, and acknowledgements.

## Code Formatting

To format the code according to PEP 8 standards, use `autopep8`:
```sh
autopep8 --in-place --aggressive --aggressive DashboardManager.py
