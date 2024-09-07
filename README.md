# Labour Force Dashboard

This project is a Labour Force Dashboard built using Python and Dash. The dashboard provides insights into labour force data, including various metrics for different age groups.

## Features

- Dropdown menus to select datasets and columns.
- Visualization of labour force data.
- Download options for processed data.
- Linear regression model for data analysis.

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
- `requirements.txt`: A list of required Python packages for the project.
- `data/`: A directory to store input data files (e.g., Excel files).
- `assets/`: A directory for storing static assets like CSS files for custom styling.
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

#### `data/`
This directory is intended to store input data files, such as Excel files containing labour force data. Ensure that the data files are placed here for the application to read and process.

#### `assets/`
This directory is used to store static assets like CSS files. You can add custom stylesheets here to customize the appearance of the dashboard.

#### `README.md`
This file provides an overview of the project, installation instructions, usage details, project structure, code formatting guidelines, contribution instructions, license information, and acknowledgements.

## Code Formatting

To format the code according to PEP 8 standards, use `autopep8`:
```sh
autopep8 --in-place --aggressive --aggressive DashboardManager.py
