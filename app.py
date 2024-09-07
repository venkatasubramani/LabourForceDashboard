from DashboardManager import DashboardManager
from FileHandler import FileHandler
from PlotManager import PlotManager

if __name__ == "__main__":
    file_handler = FileHandler(
        processed_dir='processed',
        model_results_dir='model_results')
    plot_manager = PlotManager()

    # Set up and run dashboard
    dashboard_manager = DashboardManager(file_handler, plot_manager)
    dashboard_manager.run()