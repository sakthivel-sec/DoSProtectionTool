import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog, QComboBox
from PyQt5.QtCore import QTimer
import subprocess
import psutil

class DoSProtectionTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.snort_process = None  # Initialize snort_process to None
        self.timer = QTimer()  # Timer to update log output
        self.timer.timeout.connect(self.update_log_output)

    def initUI(self):
        layout = QVBoxLayout()

        # Status label
        self.status_label = QLabel("Snort is not running", self)
        layout.addWidget(self.status_label)
        
        # Log output area
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        # Network interface selector
        self.interface_selector = QComboBox(self)
        self.detect_interfaces()
        layout.addWidget(self.interface_selector)

        # Start Snort button
        self.start_button = QPushButton("Start Snort", self)
        self.start_button.clicked.connect(self.start_snort)
        layout.addWidget(self.start_button)
        
        # Stop Snort button
        self.stop_button = QPushButton("Stop Snort", self)
        self.stop_button.clicked.connect(self.stop_snort)
        layout.addWidget(self.stop_button)

        # Save log button
        self.save_log_button = QPushButton("Save Log", self)
        self.save_log_button.clicked.connect(self.save_log)
        layout.addWidget(self.save_log_button)

        # Reload config button
        self.reload_config_button = QPushButton("Reload Snort Config", self)
        self.reload_config_button.clicked.connect(self.reload_snort_config)
        layout.addWidget(self.reload_config_button)
        
        # Set layout and window title
        self.setLayout(layout)
        self.setWindowTitle("DoS Protection Tool")
        self.show()

    def detect_interfaces(self):
        """Detect available network interfaces."""
        interfaces = psutil.net_if_addrs()
        for interface in interfaces:
            self.interface_selector.addItem(interface)

    def start_snort(self):
        try:
            network_interface = self.interface_selector.currentText()  # Get selected network interface
            # Command to start Snort with a specific configuration file
            snort_command = [
                r'C:\Snort\bin\snort.exe',
                '-A', 'console',
                '-c', r'C:\Snort\etc\snort.conf',
                '-i', network_interface
            ]  # Adjust the config path and interface
            
            # Start Snort in a subprocess, piping output to both stdout and stderr
            self.snort_process = subprocess.Popen(snort_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.status_label.setText("Snort is running...")
            self.timer.start(1000)  # Update every second to fetch Snort output
        except Exception as e:
            self.status_label.setText(f"Error starting Snort: {e}")
            print(f"Failed to start Snort: {e}")

    def update_log_output(self):
        """Update log output in real-time from the Snort process."""
        if self.snort_process:
            output = self.snort_process.stdout.read()  # Read Snort output
            if output:
                self.log_output.append(output)  # Display Snort logs in the GUI
                if "alert" in output.lower():  # Check for alerts in the log
                    self.status_label.setText("Alert: Potential DoS attack detected!")
    
    def stop_snort(self):
        """Stop the running Snort process."""
        try:
            if self.snort_process is not None:  # Check if Snort process exists
                self.snort_process.terminate()  # Stop Snort process
                self.snort_process = None  # Reset to None after stopping
                self.status_label.setText("Snort has stopped")
                self.timer.stop()  # Stop updating logs
            else:
                self.status_label.setText("Snort is not running")
        except Exception as e:
            self.status_label.setText(f"Error stopping Snort: {e}")
            print(f"Failed to stop Snort: {e}")

    def save_log(self):
        """Save the log output to a file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Log File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.log_output.toPlainText())
                self.status_label.setText(f"Log saved to {file_path}")
            except Exception as e:
                self.status_label.setText(f"Error saving log: {e}")

    def reload_snort_config(self):
        """Reload Snort configuration without stopping Snort."""
        if self.snort_process is not None:
            try:
                self.snort_process.send_signal(subprocess.signal.SIGHUP)  # Send signal to reload config
                self.status_label.setText("Snort configuration reloaded")
            except Exception as e:
                self.status_label.setText(f"Error reloading config: {e}")
        else:
            self.status_label.setText("Snort is not running")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tool = DoSProtectionTool()
    sys.exit(app.exec_())
