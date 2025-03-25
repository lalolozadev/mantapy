from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QFileDialog, QLineEdit, QFrame, QStackedWidget, QComboBox, QLabel
)
import config.button as button

# Clases de cada sección
class LoadFileSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.btn_load = QPushButton("Load File")
        self.btn_load.clicked.connect(parent.select_file)
        self.btn_load.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.btn_load.setStyleSheet(button.next)
        self.file_path = QLineEdit()

        layout.addWidget(self.btn_load)
        layout.addWidget(self.file_path)
        
        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(parent.next_section)
        self.btn_next.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.btn_next.setStyleSheet(button.next)
        layout.addWidget(self.btn_next)
        
        self.setLayout(layout)

class VariablesSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Variables Section"))
        
        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(parent.next_section)
        self.btn_next.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.btn_next.setStyleSheet(button.next)

        self.btn_back = QPushButton("Back")
        self.btn_back.clicked.connect(parent.previous_section)
        self.btn_back.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.btn_back.setStyleSheet(button.back)

        layout.addWidget(self.btn_next)
        layout.addWidget(self.btn_back)
        self.setLayout(layout)

class PlotSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Plot Section"))
        
        self.btn_back = QPushButton("Back")
        self.btn_back.clicked.connect(parent.previous_section)
        self.btn_back.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.btn_back.setStyleSheet(button.back)
        
        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(parent.next_section)
        self.btn_next.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.btn_next.setStyleSheet(button.next)

        layout.addWidget(self.btn_next)
        layout.addWidget(self.btn_back)
        self.setLayout(layout)

class ExportSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Export Section"))
        
        self.btn_back = QPushButton("Back")
        self.btn_back.clicked.connect(parent.previous_section)
        self.btn_back.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.btn_back.setStyleSheet(button.back)
        
        layout.addWidget(self.btn_back)
        self.setLayout(layout)