from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel,
    QTabWidget, QCheckBox, QScrollArea, QGroupBox, QHBoxLayout, QFrame,
    QGridLayout
)
from PyQt5.QtCore import pyqtSignal

class MainWindow(QMainWindow):
    # Define signals for each debloating task
    remove_bloatware_signal = pyqtSignal()
    disable_onedrive_signal = pyqtSignal()
    optimize_performance_signal = pyqtSignal()
    manage_registry_signal = pyqtSignal()  # Signal for registry management
    remove_selected_apps_signal = pyqtSignal(list)  # New signal for custom app removal

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows 11 Debloater")
        self.setGeometry(100, 100, 800, 600)
        self.bloatware_checkboxes = {}  # Store references to checkboxes
        
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

    def initUI(self):
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create main tab (original controls)
        main_tab = QWidget()
        main_layout = QVBoxLayout()
        
        title = QLabel("Windows Debloater Application")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        main_layout.addWidget(title)

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
    
    def remove_selected_apps(self):
        """Get list of selected apps and emit signal to remove them"""
        selected_apps = []
        for app_name, checkbox in self.bloatware_checkboxes.items():
            if checkbox.isChecked():
                selected_apps.append(app_name)
        
        if selected_apps:
            self.remove_selected_apps_signal.emit(selected_apps)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())