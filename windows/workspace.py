from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel

class MantapyUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Mantapy - Select File")
        self.setGeometry(100, 100, 600, 200)
        
        layout = QVBoxLayout()
        
        self.btn_browse = QPushButton("Browse")
        self.btn_browse.clicked.connect(self.select_file)
        layout.addWidget(self.btn_browse)
        
        self.file_path = QLineEdit(self)
        layout.addWidget(self.file_path)
        
        self.setLayout(layout)
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file")
        if file_path:
            self.file_path.setText(file_path)