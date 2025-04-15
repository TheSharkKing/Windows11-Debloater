import sys
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow
from utils.bloatware_removal import safe_remove_bloatware
from utils.onedrive_disabler import disable_onedrive
from utils.performance_optimizer import optimize_performance
from utils.registry_manager import manage_registry_keys
from utils.uac_elevation import run_as_admin, is_admin
from utils.logger import setup_logger

# Setup global logger
logger = setup_logger()

def main():
    # Check for admin privileges first
    if not is_admin():
        logger.warning("Application not running with admin privileges. Requesting elevation...")
        run_as_admin()
        # If run_as_admin returns (doesn't exit), it failed
        logger.error("Failed to obtain administrator privileges. Exiting.")
        show_error_message("Administrator privileges are required to run this application.")
        return
    
    logger.info("Application started with administrator privileges")
    
    try:
        # Launch the UI
        app = QApplication(sys.argv)
        window = MainWindow()

        # Connect UI buttons to debloating functions
        window.remove_bloatware_signal.connect(lambda: execute_with_logging(safe_remove_bloatware, "Bloatware removal"))
        window.disable_onedrive_signal.connect(lambda: execute_with_logging(disable_onedrive, "OneDrive disabling"))
        window.optimize_performance_signal.connect(lambda: execute_with_logging(optimize_performance, "Performance optimization"))
        window.manage_registry_signal.connect(lambda: execute_with_logging(manage_registry_keys, "Registry management"))

        # Show the UI
        window.show()
        logger.info("Application UI initialized successfully")
        
        sys.exit(app.exec_())
    except Exception as e:
        # Log any unexpected exceptions
        logger.critical(f"Critical error in main application: {str(e)}")
        logger.critical(traceback.format_exc())
        show_error_message(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

def execute_with_logging(func, operation_name):
    """Wrapper to execute functions with proper logging and error handling."""
    try:
        logger.info(f"Starting {operation_name} operation")
        func()
        logger.info(f"{operation_name} completed successfully")
    except Exception as e:
        logger.error(f"Error during {operation_name}: {str(e)}")
        logger.error(traceback.format_exc())
        show_error_message(f"Error during {operation_name}: {str(e)}")

def show_error_message(message):
    """Display error message in a dialog box."""
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Critical)
    error_box.setWindowTitle("Error")
    error_box.setText(message)
    error_box.exec_()

if __name__ == "__main__":
    main()