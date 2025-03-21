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
        self.setLayout(layout)

class VariablesSection(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Variables Section"))
        self.setLayout(layout)

class PlotSection(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Plot Section"))
        self.setLayout(layout)

class ExportSection(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Export Section"))
        self.setLayout(layout)