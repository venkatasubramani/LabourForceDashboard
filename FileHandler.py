import os
import pandas as pd

class FileHandler:
    """
    Class to handle file operations, such as loading data from CSV files.
    """
    def __init__(self, processed_dir, model_results_dir):
        self.processed_dir = processed_dir
        self.model_results_dir = model_results_dir

    def list_files(self):
        """
        List all relevant files in the processed directory.

        Returns:
        --------
        list of str
            List of filenames in the processed directory.
        """
        return [f for f in os.listdir(self.processed_dir) if f.endswith('.csv')]

    def load_file(self, directory, filename):
        """
        Load a CSV file into a pandas DataFrame.

        Parameters:
        -----------
        directory : str
            The directory where the file is located.
        filename : str
            The name of the file to load.

        Returns:
        --------
        pd.DataFrame
            The loaded data as a pandas DataFrame.
        """
        file_path = os.path.join(directory, filename)
        return pd.read_csv(file_path)

    def list_model_files(self, base_name, model_name, column_name):
        """
        List all files matching a specific base name, model name, and column.

        Parameters:
        -----------
        base_name : str
            The base file name (e.g., "sixteen_and_over").
        model_name : str
            The model name (e.g., "linear_regression").
        column_name : str
            The column name (e.g., "Employment rate").

        Returns:
        --------
        str
            The filename that matches the criteria or None if no match is found.
        """
        # Replace spaces with underscores for the column name in the filename
        # column_name_formatted = column_name.replace(' ', '_')
        pattern = f"{base_name}_{model_name}_{column_name}_forecast.csv"
        print(f"Searching for file with pattern: {pattern}")
        # Search for the file in the model_results_dir
        for f in os.listdir(self.model_results_dir):
            if f == pattern:
                return f  # Return the filename if found
        return None  # Return None if no file is found
