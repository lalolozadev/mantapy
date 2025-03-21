from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QFileDialog, QLineEdit, QFrame, QStackedWidget, QComboBox, QLabel
)

# Clases de cada sección
class LoadFileSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.btn_load = QPushButton("Load File")
        self.btn_load.clicked.connect(parent.select_file)
        self.file_path = QLineEdit()

        layout.addWidget(self.btn_load)
        layout.addWidget(self.file_path)
        
        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(parent.next_section)
        layout.addWidget(self.btn_next)
        
        self.setLayout(layout)

class VariablesSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Variables Section"))
        
        self.btn_back = QPushButton("Back")
        self.btn_back.clicked.connect(parent.previous_section)
        
        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(parent.next_section)

        layout.addWidget(self.btn_back)
        layout.addWidget(self.btn_next)
        self.setLayout(layout)

class PlotSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Plot Section"))
        
        self.btn_back = QPushButton("Back")
        self.btn_back.clicked.connect(parent.previous_section)
        
        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(parent.next_section)

        layout.addWidget(self.btn_back)
        layout.addWidget(self.btn_next)
        self.setLayout(layout)

class ExportSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Export Section"))
        
        self.btn_back = QPushButton("Back")
        self.btn_back.clicked.connect(parent.previous_section)
        
        layout.addWidget(self.btn_back)
        self.setLayout(layout)