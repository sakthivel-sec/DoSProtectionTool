import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import subprocess

class DoSProtectionTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.snort_process = None  # Initialize snort_process to None

    def initUI(self):
        layout = QVBoxLayout()
        
        self.status_label = QLabel("Snort is not running", self)
        layout.addWidget(self.status_label)
        
        self.start_button = QPushButton("Start Snort", self)
        self.start_button.clicked.connect(self.start_snort)
        layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Snort", self)
        self.stop_button.clicked.connect(self.stop_snort)
        layout.addWidget(self.stop_button)
        
        self.setLayout(layout)
        self.setWindowTitle("DoS Protection Tool")
        self.show()

    def start_snort(self):
        try:
            network_interface = '1'  # Replace with the correct network interface
            # Command to start Snort with a specific configuration file
            snort_command = [
                r'C:\Snort\bin\snort.exe',
                '-A', 'console',
                '-c', r'C:\Snort\etc\snort.conf',
                '-i', network_interface
            ]  # Adjust the config path and interface
            
            # Start Snort in a subprocess
            self.snort_process = subprocess.Popen(snort_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.status_label.setText("Snort is running...")
        except Exception as e:
            self.status_label.setText(f"Error starting Snort: {e}")
            print(f"Failed to start Snort: {e}")

    def stop_snort(self):
        try:
            if self.snort_process is not None:  # Check if Snort process exists
                self.snort_process.terminate()  # Stop Snort process
                self.snort_process = None  # Reset to None after stopping
                self.status_label.setText("Snort has stopped")
            else:
                self.status_label.setText("Snort is not running")
        except Exception as e:
            self.status_label.setText(f"Error stopping Snort: {e}")
            print(f"Failed to stop Snort: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tool = DoSProtectionTool()
    sys.exit(app.exec_())
