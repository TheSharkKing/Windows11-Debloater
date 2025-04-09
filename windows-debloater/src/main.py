import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.bloatware_removal import safe_remove_bloatware
from utils.onedrive_disabler import disable_onedrive
from utils.performance_optimizer import optimize_performance

def main():
    # Launch the UI
    app = QApplication(sys.argv)
    window = MainWindow()

    # Connect UI buttons to debloating functions
    window.remove_bloatware_signal.connect(safe_remove_bloatware)
    window.disable_onedrive_signal.connect(disable_onedrive)
    window.optimize_performance_signal.connect(optimize_performance)

    # Show the UI
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()