import webbrowser
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel
from .workspace import MantapyUI

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Welcome to Mantapy")
        self.setGeometry(100, 100, 600, 200)
        
        layout = QVBoxLayout()
        
        self.label_welcome = QLabel("*** Welcome to Mantapy ***\nCreated by: Eduardo Loza\nOpen-source project for oceanographic data analysis.\n\n→ Select an option:")
        layout.addWidget(self.label_welcome)
        
        self.btn_start = QPushButton("Start")
        self.btn_start.clicked.connect(self.open_main_window)
        layout.addWidget(self.btn_start)
        
        self.btn_doc = QPushButton("Read Documentation")
        self.btn_doc.clicked.connect(self.open_documentation)
        layout.addWidget(self.btn_doc)
        
        self.setLayout(layout)
    
    def open_main_window(self):
        self.main_window = MantapyUI()
        self.main_window.show()
        self.close()
    
    def open_documentation(self):
        webbrowser.open("https://github.com/lalolozadev/mantapy")