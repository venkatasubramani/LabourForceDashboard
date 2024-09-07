import pandas as pd
from dateutil import parser
import calendar
from datetime import datetime


class LabourSurveyDataPrep:
    def __init__(self, file_path, sheet_name, output_folder):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.output_folder = output_folder
        self.data = None
        self.sixteen_and_over = None
        self.sixteen_and_sixty_four = None

    def load_data(self):
        """Load the Excel file and drop any rows with missing values."""
        self.data = pd.read_excel(
            self.file_path,
            sheet_name=self.sheet_name,
            skiprows=7,
            header=0)
        self.data = self.data.dropna()  # type: ignore

    @staticmethod
    def calculate_dates(identifier):
        """
        Calculate the start and end dates based on the identifier.

        Args:
            identifier (str): The identifier string in the format 'MMM-MMM YYYY'.

        Returns:
            tuple: A tuple containing the start date and end date as datetime objects.
        """
        # Split the identifier
        months, year = identifier.split(' ')
        start_month, end_month = months.split('-')

        # Get the end month and year
        end_date_str = f"01 {end_month} {year}"
        end_date = datetime.strptime(end_date_str, "%d %b %Y")

        # Calculate the last day of the end month
        last_day = calendar.monthrange(end_date.year, end_date.month)[1]
        end_date = end_date.replace(day=last_day)

        # Calculate the start date (first day of the start month 3 months
        # earlier)
        start_month_number = (end_date.month - 2) % 12 or 12
        start_year = end_date.year if start_month_number <= end_date.month else end_date.year - 1
        start_date = datetime(start_year, start_month_number, 1)

        return start_date, end_date

    def process_data(self):
        """Process the data to calculate the start and end dates and prepare two new DataFrames."""
        # Apply the function to create new columns
        self.data['Start Date'], self.data['End Date'] = zip(  # type: ignore
            *self.data['Dataset identifier code'].apply(self.calculate_dates))  # type: ignore

        # Sort the DataFrame by 'Start Date'
        self.data = self.data.sort_values(['Start Date'])  # type: ignore

        # Create a new DataFrame for all aged 16 & over
        self.sixteen_and_over = self.data[['Dataset identifier code',
                                           'Start Date',
                                           'End Date',
                                           'MGSL',
                                           'MGSF',
                                           'MGRZ',
                                           'MGSC',
                                           'MGSI',
                                           'MGWG',
                                           'MGSR',
                                           'MGSX',
                                           'YBTC']]
        self.sixteen_and_over.columns = [
            'Dataset identifier code',
            'Start Date',
            'End Date',
            'All aged 16 & over level',
            'Total economically active level',
            'Total in employment level',
            'Unemployed level',
            'Economically inactive level',
            'Economic activity rate',
            'Employment rate',
            'Unemployment rate',
            'Economic inactivity rate']

        # Create a new DataFrame for all aged 16 to 64
        self.sixteen_and_sixty_four = self.data[['Dataset identifier code',
                                                 'Start Date',
                                                 'End Date',
                                                 'LF2O',
                                                 'LF2K',
                                                 'LF2G',
                                                 'LF2I',
                                                 'LF2M',
                                                 'LF22',
                                                 'LF24',
                                                 'LF2Q',
                                                 'LF2S']]
        self.sixteen_and_sixty_four.columns = [
            'Dataset identifier code',
            'Start Date',
            'End Date',
            'All aged 16 to 64 level',
            'Total economically active level',
            'Total in employment level',
            'Unemployed level',
            'Economically inactive level',
            'Economic activity rate',
            'Employment rate',
            'Unemployment rate',
            'Economic inactivity rate']

    def save_to_csv(self):
        """Save the processed DataFrames to CSV files."""
        self.sixteen_and_over.to_csv(  # type: ignore
            f"{self.output_folder}/sixteen_and_over.csv",
            index=False)  # type: ignore
        self.sixteen_and_sixty_four.to_csv(  # type: ignore
            f"{self.output_folder}/sixteen_and_sixty_four.csv",
            index=False)  # type: ignore

    def run(self):
        """Run the entire data preparation process."""
        self.load_data()
        self.process_data()
        self.save_to_csv()


# Example usage:
data_prep = LabourSurveyDataPrep(file_path='input/a01aug2024.xls',
                                 sheet_name='1', output_folder='processed')
data_prep.run()
