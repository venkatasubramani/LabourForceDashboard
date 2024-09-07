from DashboardManager import DashboardManager
from FileHandler import FileHandler
from PlotManager import PlotManager

# Initialize the handlers
file_handler = FileHandler(processed_dir='processed', model_results_dir='model_results')
plot_manager = PlotManager()

# Create an instance of the dashboard manager
dashboard_manager = DashboardManager(file_handler, plot_manager)

# Expose the server for deployment platforms
server = dashboard_manager.server

if __name__ == "__main__":
    # Run the Dash app locally
    dashboard_manager.run(port=8050)