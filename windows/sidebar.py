from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QSpacerItem, QSizePolicy
                            )
from PyQt6.QtCore import Qt
import config.button as button
import config.text as text
import os

# Clases de cada sección
class LoadFileSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.title_section = QLabel(
            f"<span style='font-size:{text.text_subtitle}px;'><b> Load file </b></span><br>"
            f"<span style='font-size:{text.text_normal}px;'> Select a file from your device to proceed. </span><br>"
            f"<span style='font-size:{text.text_normal}px;'> Supported formats include .csv and .txt. </span><br><br>"
            f"<span style='font-size:{text.text_normal}px;'> Click the button below to browse. </span><br>"
        )

        # Habilitar ajuste de texto en QLabel
        self.title_section.setWordWrap(True)
        self.title_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.title_section)

        # Botón Load File
        self.btn_load = QPushButton("Load File")
        self.btn_load.clicked.connect(parent.select_file)
        self.btn_load.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.btn_load.setStyleSheet(button.next)
        layout.addWidget(self.btn_load)

        # Campo de texto para mostrar la ruta del archivo
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Load a file")  # Texto de ayuda
        self.file_path.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.file_path.setStyleSheet(button.file_input)
        layout.addWidget(self.file_path)

        # Aquí conectamos el evento para analizar el tipo de archivo automáticamente
        self.file_path.textChanged.connect(self.analyze_file_type)

        # Agregar un espacio entre los elementos superiores y el botón "Next"
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Botón Next (se mantiene en la parte inferior)
        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(parent.next_section)
        self.btn_next.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.btn_next.setStyleSheet(button.next)
        layout.addWidget(self.btn_next)

        self.setLayout(layout)

    def analyze_file_type(self):
            file_path = self.file_path.text().strip()  # Obtener el texto y eliminar espacios

            if not file_path:
                print("No file selected.")
                return

            _, file_extension = os.path.splitext(file_path)  # Extraer la extensión del archivo

            file_extension = file_extension.lower()  # Normalizar la extensión

            if file_extension in ['.txt']:
                print("The file is a TXT file.")
            elif file_extension in ['.csv']:
                print("The file is a CSV file.")
            elif file_extension in ['.nc', '.netcdf']:
                print("The file is a NetCDF file.")
            else:
                print("Unknown file type.")

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