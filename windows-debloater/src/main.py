import sys
import os
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from ui.main_window import MainWindow
from utils.bloatware_removal import safe_remove_bloatware, remove_selected_bloatware
from utils.onedrive_disabler import disable_onedrive
from utils.performance_optimizer import optimize_performance
from utils.registry_manager import manage_registry_keys
from utils.uac_elevation import run_as_admin, is_admin
from utils.logger import setup_logger
from utils.preset_manager import run_minimal_preset, run_full_clean_preset

# Setup global logger
logger = setup_logger()

def main():
    # Ensure the script runs with admin privileges
    if not is_admin():
        logger.warning("Application not running with admin privileges. Requesting elevation...")
        run_as_admin()
        return

    logger.info("Application started with administrator privileges")

    try:
        # Initialize the application and splash screen
        app = QApplication(sys.argv)
        splash = create_splash_screen(app)

        # Initialize the main window
        window = MainWindow()
        connect_signals(window)

        # Finish splash and show the main window
        QTimer.singleShot(1500, lambda: finish_splash(window, splash))
        logger.info("Application UI initialized successfully")

        sys.exit(app.exec_())
    except Exception as e:
        handle_critical_error(e)

def create_splash_screen(app):
    """Create and display the splash screen."""
    splash_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images", "splash.png")
    splash_pix = QPixmap(splash_path) if os.path.exists(splash_path) else QPixmap(500, 300).fill(Qt.white)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.showMessage("Loading Windows 11 Debloater...", Qt.AlignBottom | Qt.AlignCenter, Qt.black)
    splash.show()
    app.processEvents()
    return splash

def connect_signals(window):
    """Connect UI signals to their respective functions."""
    window.remove_bloatware_signal.connect(lambda: execute_with_logging(safe_remove_bloatware, "Bloatware removal"))
    window.disable_onedrive_signal.connect(lambda: execute_with_logging(disable_onedrive, "OneDrive disabling"))
    window.optimize_performance_signal.connect(lambda: execute_with_logging(optimize_performance, "Performance optimization"))
    window.manage_registry_signal.connect(lambda: execute_with_logging(manage_registry_keys, "Registry management"))
    window.remove_selected_apps_signal.connect(lambda apps: execute_with_logging(
        lambda: remove_selected_bloatware(apps), "Custom app removal"
    ))
    window.run_minimal_preset_signal.connect(lambda: execute_with_logging(
        lambda: run_minimal_preset(window.minimal_bloatware_list), "Minimal preset"
    ))
    window.run_full_clean_preset_signal.connect(lambda: execute_with_logging(
        lambda: run_full_clean_preset(window.bloatware_list), "Full system clean preset"
    ))

def finish_splash(window, splash):
    """Close the splash screen and show the main window."""
    window.show()
    splash.finish(window)

def execute_with_logging(func, operation_name):
    """Wrapper to execute functions with proper logging and error handling."""
    try:
        logger.info(f"Starting {operation_name} operation")
        func()
        logger.info(f"{operation_name} completed successfully")
        show_info_message(f"{operation_name} completed successfully!")
    except Exception as e:
        logger.error(f"Error during {operation_name}: {str(e)}")
        logger.error(traceback.format_exc())
        show_error_message(f"Error during {operation_name}: {str(e)}")

def handle_critical_error(e):
    """Handle unexpected critical errors."""
    logger.critical(f"Critical error in main application: {str(e)}")
    logger.critical(traceback.format_exc())
    show_error_message(f"An unexpected error occurred: {str(e)}")
    sys.exit(1)

def show_error_message(message):
    """Display an error message in a dialog box."""
    QMessageBox.critical(None, "Error", message)

def show_info_message(message):
    """Display an information message in a dialog box."""
    QMessageBox.information(None, "Information", message)

if __name__ == "__main__":
    main()