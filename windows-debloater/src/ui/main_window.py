from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel,
    QTabWidget, QCheckBox, QScrollArea, QGroupBox, QHBoxLayout, QFrame,
    QGridLayout, QMessageBox, QProgressBar, QStyleFactory, QSplashScreen,
    QProgressDialog
)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor, QFont

class MainWindow(QMainWindow):
    # Define signals for each debloating task
    remove_bloatware_signal = pyqtSignal()
    disable_onedrive_signal = pyqtSignal()
    optimize_performance_signal = pyqtSignal()
    manage_registry_signal = pyqtSignal()  # Signal for registry management
    remove_selected_apps_signal = pyqtSignal(list)  # Signal for custom app removal
    run_minimal_preset_signal = pyqtSignal()  # New signal for minimal preset
    run_full_clean_preset_signal = pyqtSignal()  # New signal for full clean preset
    
    # Constants for styling
    ACCENT_COLOR = "#0078D7"  # Windows blue
    LIGHT_ACCENT_COLOR = "#E1F0FF"
    HOVER_COLOR = "#005A9E"
    BACKGROUND_COLOR = "#F0F0F0"
    TEXT_COLOR = "#333333"
    SECONDARY_TEXT_COLOR = "#666666"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows 11 Debloater")
        self.setGeometry(100, 100, 900, 650)  # Slightly larger window
        self.bloatware_checkboxes = {}  # Store references to checkboxes
        self.operation_in_progress = False
        self.progress_dialog = None
        
        # Apply modern theme
        self.apply_theme()
        
        # Minimal preset bloatware list - apps that are rarely used and safe to remove
        self.minimal_bloatware_list = [
            "Microsoft.3DBuilder",
            "Microsoft.BingNews",
            "Microsoft.BingWeather",
            "Microsoft.BingFinance",
            "Microsoft.BingSports",
            "Microsoft.GetHelp",
            "Microsoft.Getstarted",
            "Microsoft.MicrosoftSolitaireCollection",
            "Microsoft.ZuneMusic",
            "Microsoft.ZuneVideo",
            "Microsoft.People",
            "Microsoft.WindowsFeedbackHub",
            "Microsoft.YourPhone",
            "Microsoft.MixedReality.Portal",
            "Microsoft.Xbox.TCUI",
            "Microsoft.XboxApp",
            "Microsoft.XboxGameOverlay",
            "Microsoft.XboxGamingOverlay",
            "Microsoft.XboxIdentityProvider",
            "Microsoft.XboxSpeechToTextOverlay"
        ]
        
        # Expanded list of bloatware apps to display in the custom removal tab
        self.bloatware_list = [
            # Base Microsoft Apps
            "Microsoft.3DBuilder",
            "Microsoft.549981C3F5F10",  # Cortana
            "Microsoft.Appconnector",
            "Microsoft.BingFinance",
            "Microsoft.BingNews",
            "Microsoft.BingSports",
            "Microsoft.BingTranslator",
            "Microsoft.BingWeather",
            "Microsoft.CommsPhone",
            "Microsoft.ConnectivityStore",
            "Microsoft.DesktopAppInstaller",
            "Microsoft.FreshPaint",
            "Microsoft.GetHelp",
            "Microsoft.Getstarted",
            "Microsoft.Messaging",
            "Microsoft.Microsoft3DViewer",
            "Microsoft.MicrosoftOfficeHub",
            "Microsoft.MicrosoftPowerBIForWindows",
            "Microsoft.MicrosoftSolitaireCollection",
            "Microsoft.MicrosoftStickyNotes",
            "Microsoft.MinecraftUWP",
            "Microsoft.MixedReality.Portal",
            "Microsoft.NetworkSpeedTest",
            "Microsoft.News",
            "Microsoft.Office.OneNote",
            "Microsoft.Office.Sway",
            "Microsoft.OneConnect",
            "Microsoft.People",
            "Microsoft.Print3D",
            "Microsoft.RemoteDesktop",
            "Microsoft.SkypeApp",
            "Microsoft.StorePurchaseApp",
            "Microsoft.Todos",
            "Microsoft.Wallet",
            "Microsoft.WebMediaExtensions",
            "Microsoft.Whiteboard",
            "Microsoft.WindowsAlarms",
            "Microsoft.WindowsCamera",
            "Microsoft.windowscommunicationsapps",  # Mail and Calendar
            "Microsoft.WindowsFeedbackHub",
            "Microsoft.WindowsMaps",
            "Microsoft.WindowsPhone",
            "Microsoft.WindowsReadingList",
            "Microsoft.WindowsSoundRecorder",
            "Microsoft.WindowsStore",
            "Microsoft.Xbox.TCUI",
            "Microsoft.XboxApp",
            "Microsoft.XboxGameCallableUI",
            "Microsoft.XboxGameOverlay",
            "Microsoft.XboxGamingOverlay",
            "Microsoft.XboxIdentityProvider",
            "Microsoft.XboxSpeechToTextOverlay",
            "Microsoft.YourPhone",
            "Microsoft.ZuneMusic",
            "Microsoft.ZuneVideo",
            
            # Windows 11 Specific
            "MicrosoftCorporationII.MicrosoftFamily",
            "MicrosoftCorporationII.QuickAssist",
            "MicrosoftTeams",
            "Microsoft.GamingApp",
            "Microsoft.MicrosoftEdge",
            "Microsoft.MicrosoftEdge.Stable",
            "Microsoft.PowerAutomateDesktop",
            "Microsoft.HEIFImageExtension",
            "Microsoft.VP9VideoExtensions",
            "Microsoft.WebpImageExtension",
            "Microsoft.WindowsNotepad",
            "Microsoft.Windows.DevHome",
            "Microsoft.WindowsTerminal",
            "Microsoft.Clipchamp",
            "Microsoft.HEVCVideoExtension",
            
            # Third Party
            "FACEBOOK.FACEBOOK",
            "FACEBOOK.INSTAGRAM",
            "FACEBOOK.MESSENGER",
            "Clipchamp.Clipchamp",
            "SpotifyAB.SpotifyMusic",
            "Disney.37853FC22B2CE",  # Disney+
            "AmazonVideo.PrimeVideo",
            "BytedancePte.Ltd.TikTok",
            "46928bounde.EclipseManager",
            "ActiproSoftwareLLC.562882FEEB491",
            "AdobeSystemsIncorporated.AdobePhotoshopExpress",
            "Dolby.DolbyAccess",
            "Duolingo-LearnLanguagesforFree.Duolingo-LearnLanguagesforFree",
            "PandoraMediaInc.29680B314EFC2",
            "ShazamEntertainmentLtd.Shazam",
            "king.com.CandyCrushSaga",
            "king.com.CandyCrushSodaSaga",
            "king.com.BubbleWitch3Saga"
        ]
        
        self.initUI()

    def apply_theme(self):
        """Apply modern theme to the application"""
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {self.BACKGROUND_COLOR};
            }}
            QLabel {{
                color: {self.TEXT_COLOR};
            }}
            QPushButton {{
                background-color: {self.ACCENT_COLOR};
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 120px;
                margin: 2px;
            }}
            QPushButton:hover {{
                background-color: {self.HOVER_COLOR};
            }}
            QPushButton:pressed {{
                background-color: #004275;
            }}
            QPushButton:disabled {{
                background-color: #CCCCCC;
                color: #666666;
            }}
            QTabWidget::pane {{
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                top: -1px;
            }}
            QTabBar::tab {{
                background: {self.LIGHT_ACCENT_COLOR};
                color: {self.TEXT_COLOR};
                padding: 8px 16px;
                border: 1px solid #CCCCCC;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background: {self.ACCENT_COLOR};
                color: white;
            }}
            QTabBar::tab:hover:!selected {{
                background: #D0E6FF;
            }}
            QCheckBox {{
                spacing: 8px;
                color: {self.TEXT_COLOR};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
            }}
            QCheckBox::indicator:unchecked {{
                border: 1px solid #AAAAAA;
                background: white;
                border-radius: 3px;
            }}
            QCheckBox::indicator:checked {{
                border: 1px solid {self.ACCENT_COLOR};
                background: {self.ACCENT_COLOR};
                border-radius: 3px;
            }}
            QScrollArea {{
                border: 1px solid #CCCCCC;
                border-radius: 5px;
            }}
            QFrame[frameShape="4"] {{ /* HLine */
                color: #CCCCCC;
                height: 1px;
                margin: 10px 0px;
            }}
        """)
        
        # Apply modern style to the application
        if QStyleFactory.keys():  # Check available styles
            if "Fusion" in QStyleFactory.keys():
                QApplication.setStyle(QStyleFactory.create("Fusion"))
            elif "Windows" in QStyleFactory.keys():
                QApplication.setStyle(QStyleFactory.create("Windows"))

    def initUI(self):
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create main tab (original controls)
        main_tab = QWidget()
        main_layout = QVBoxLayout()
        
        title = QLabel("Windows Debloater Application")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        main_layout.addWidget(title)
        
        # Add preset section
        preset_label = QLabel("Debloating Presets:")
        preset_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        main_layout.addWidget(preset_label)
        
        # Preset buttons
        preset_layout = QHBoxLayout()
        
        self.minimal_preset_button = QPushButton("Minimal Cleanup")
        self.minimal_preset_button.setToolTip("Remove commonly unused apps while keeping most functionality")
        self.minimal_preset_button.clicked.connect(self.run_minimal_preset)
        preset_layout.addWidget(self.minimal_preset_button)
        
        self.full_clean_preset_button = QPushButton("Full System Clean")
        self.full_clean_preset_button.setToolTip("Remove all bloatware, disable OneDrive, and optimize performance")
        self.full_clean_preset_button.clicked.connect(self.confirm_full_clean)
        preset_layout.addWidget(self.full_clean_preset_button)
        
        main_layout.addLayout(preset_layout)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # Individual actions label
        actions_label = QLabel("Individual Actions:")
        actions_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        main_layout.addWidget(actions_label)

        # Individual buttons (original controls)
        self.remove_bloatware_button = QPushButton("Remove Bloatware")
        self.remove_bloatware_button.clicked.connect(self.remove_bloatware_signal.emit)
        main_layout.addWidget(self.remove_bloatware_button)

        self.manage_registry_button = QPushButton("Manage Registry Keys")
        self.manage_registry_button.clicked.connect(self.manage_registry_signal.emit)
        main_layout.addWidget(self.manage_registry_button)

        self.disable_onedrive_button = QPushButton("Disable OneDrive")
        self.disable_onedrive_button.clicked.connect(self.disable_onedrive_signal.emit)
        main_layout.addWidget(self.disable_onedrive_button)

        self.optimize_performance_button = QPushButton("Optimize Performance")
        self.optimize_performance_button.clicked.connect(self.optimize_performance_signal.emit)
        main_layout.addWidget(self.optimize_performance_button)
        
        main_layout.addStretch()
        main_tab.setLayout(main_layout)
        
        # Create custom app removal tab
        app_removal_tab = self.create_app_removal_tab()
        
        # Add tabs
        self.tabs.addTab(main_tab, "Main")
        self.tabs.addTab(app_removal_tab, "Custom App Removal")
        
        # Set tab widget as central widget
        self.setCentralWidget(self.tabs)
    
    def create_app_removal_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Create title and instructions
        title = QLabel("Custom App Removal")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 5px;")
        instructions = QLabel("Select the applications you want to uninstall:")
        instructions.setStyleSheet("margin-bottom: 15px;")
        
        layout.addWidget(title)
        layout.addWidget(instructions)
        
        # Create frame with scroll area for app checkboxes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QGridLayout(scroll_content)
        
        # Create checkboxes for each bloatware app
        row = 0
        col = 0
        for app in self.bloatware_list:
            checkbox = QCheckBox(app)
            self.bloatware_checkboxes[app] = checkbox
            scroll_layout.addWidget(checkbox, row, col)
            
            # Arrange in 2 columns
            if col == 1:
                col = 0
                row += 1
            else:
                col += 1
        
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        # Create buttons layout
        buttons_layout = QHBoxLayout()
        
        # Select All button
        select_all_button = QPushButton("Select All")
        select_all_button.clicked.connect(self.select_all_apps)
        buttons_layout.addWidget(select_all_button)
        
        # Deselect All button
        deselect_all_button = QPushButton("Deselect All")
        deselect_all_button.clicked.connect(self.deselect_all_apps)
        buttons_layout.addWidget(deselect_all_button)
        
        # Remove Selected button
        remove_selected_button = QPushButton("Remove Selected Apps")
        remove_selected_button.clicked.connect(self.remove_selected_apps)
        buttons_layout.addWidget(remove_selected_button)
        
        layout.addLayout(buttons_layout)
        tab.setLayout(layout)
        
        return tab
    
    def select_all_apps(self):
        """Select all app checkboxes"""
        for checkbox in self.bloatware_checkboxes.values():
            checkbox.setChecked(True)
    
    def deselect_all_apps(self):
        """Deselect all app checkboxes"""
        for checkbox in self.bloatware_checkboxes.values():
            checkbox.setChecked(False)
    
    def show_operation_progress(self, title, operation_name):
        """Show progress dialog for operations"""
        if self.operation_in_progress:
            return
            
        self.operation_in_progress = True
        
        # Create progress dialog
        self.progress_dialog = QProgressDialog(f"{operation_name} in progress...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowTitle(title)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)
        self.progress_dialog.setMinimumDuration(0)  # Show immediately
        
        # Set the style for the progress bar
        progress_bar = self.progress_dialog.findChild(QProgressBar)
        if progress_bar:
            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 1px solid #CCCCCC;
                    border-radius: 5px;
                    text-align: center;
                    height: 20px;
                }}
                QProgressBar::chunk {{
                    background-color: {self.ACCENT_COLOR};
                    border-radius: 5px;
                }}
            """)

        # Setup progress simulation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0
        self.timer.start(100)  # Update every 100ms
        
        # Show the progress dialog
        self.progress_dialog.show()
    
    def update_progress(self):
        """Update the progress bar value"""
        if not self.progress_dialog or not self.operation_in_progress:
            self.timer.stop()
            return
            
        self.progress_value += 1
        if self.progress_value <= 100:
            self.progress_dialog.setValue(self.progress_value)
        else:
            self.timer.stop()
            self.operation_in_progress = False
            self.progress_dialog = None
    
    def remove_selected_apps(self):
        """Get list of selected apps and emit signal to remove them"""
        selected_apps = []
        for app_name, checkbox in self.bloatware_checkboxes.items():
            if checkbox.isChecked():
                selected_apps.append(app_name)
        
        if selected_apps:
            # Show progress dialog
            self.show_operation_progress("App Removal", "Removing selected applications")
            
            # Emit signal to remove selected apps
            self.remove_selected_apps_signal.emit(selected_apps)
    
    def run_minimal_preset(self):
        """Run the minimal preset cleanup"""
        # Pre-select the minimal list of apps in the Custom App Removal tab
        for app_name, checkbox in self.bloatware_checkboxes.items():
            checkbox.setChecked(app_name in self.minimal_bloatware_list)
        
        # Switch to the Custom App Removal tab to show what will be removed
        self.tabs.setCurrentIndex(1)
        
        # Show progress dialog
        self.show_operation_progress("Minimal Cleanup", "Removing minimal bloatware")
        
        # Emit signal to run minimal preset
        self.run_minimal_preset_signal.emit()
    
    def confirm_full_clean(self):
        """Show confirmation dialog before running full clean preset"""
        confirm_box = QMessageBox()
        confirm_box.setIcon(QMessageBox.Warning)
        confirm_box.setWindowTitle("Confirm Full System Clean")
        confirm_box.setText("This will remove ALL bloatware apps, disable OneDrive, and optimize system performance.")
        confirm_box.setInformativeText("These changes cannot be easily undone. Are you sure you want to continue?")
        confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_box.setDefaultButton(QMessageBox.No)
        
        # Apply custom styling to the message box
        confirm_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {self.BACKGROUND_COLOR};
            }}
            QPushButton {{
                background-color: {self.ACCENT_COLOR};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {self.HOVER_COLOR};
            }}
        """)
        
        result = confirm_box.exec_()
        
        if result == QMessageBox.Yes:
            # Select all apps in the Custom App Removal tab
            self.select_all_apps()
            
            # Switch to the Custom App Removal tab to show what will be removed
            self.tabs.setCurrentIndex(1)
            
            # Show progress dialog
            self.show_operation_progress("Full System Clean", "Performing full system cleanup")
            
            # Emit signal to run full clean preset
            self.run_full_clean_preset_signal.emit()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())