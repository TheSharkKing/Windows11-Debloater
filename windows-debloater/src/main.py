import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.bloatware_removal import safe_remove_bloatware
from utils.onedrive_disabler import disable_onedrive
from utils.performance_optimizer import optimize_performance

def main():
    # Remove bloatware
    print("Removing bloatware...")
    safe_remove_bloatware()

    # Disable OneDrive
    print("Disabling OneDrive...")
    disable_onedrive()

    # Optimize performance
    print("Optimizing system performance...")
    optimize_performance()

    # Launch the UI
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()