from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QSpacerItem, QSizePolicy,
                            QTableWidget, QTableWidgetItem
                            )
from PyQt6.QtCore import Qt
import config.button as button
import config.text as text
import os
import pandas as pd

class LoadFileSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # Guardamos la referencia del padre
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

    # def analyze_file_type(self):
    #     file_path = self.file_path.text().strip()

    #     if not file_path:
    #         self.parent.update_content_text("No file selected.")
    #         return

    #     _, file_extension = os.path.splitext(file_path)
    #     file_extension = file_extension.lower()

    #     if file_extension in ['.csv']:
    #         try:
    #             # Read the file with pandas
    #             df = pd.read_csv(file_path, sep=r'[,\s;|]+', engine='python')
    #             # Convert DataFrame to HTML table with styling
    #             html_table = df.to_html(
    #                 index=False,
    #                 border=1
    #             )
    #             styled_table = html_table.replace('<table', f'<table style="border-collapse: collapse; width: 100%; font-size: {text.text_normal}px; font-family: Arial, sans-serif;"') \
    #                                     .replace('<th', '<th style="background-color: #4f81bd; color: white; font-weight: bold; border: 1px solid #2f4f6f; padding: 8px;"') \
    #                                     .replace('<td', '<td style="border: 1px solid #ddd; padding: 8px; text-align: left;"') \
    #                                     .replace('<tr', '<tr style="border-bottom: 1px solid #ddd;"') \
    #                                     .replace('<tr style="border-bottom: 1px solid #ddd;"><th', '<tr style="border-bottom: 2px solid #4f81bd;"><th')
    #             self.parent.update_content_text(styled_table, as_notebook=True)
    #         except Exception as e:
    #             self.parent.update_content_text(f"Error reading file: {str(e)}")
    #         except Exception as e:
    #             self.parent.update_content_text(f"Error reading file: {str(e)}")
    #     # elif file_extension in ['.csv']:
    #     #     message = "The file is a CSV file."
    #     #    self.parent.update_content_text(message)
    #     elif file_extension in ['.nc', '.netcdf']:
    #         message = "The file is a NetCDF file."
    #         self.parent.update_content_text(message)
    #     else:
    #         message = "Unknown file type."
    #         self.parent.update_content_text(message)

    def analyze_file_type(self):
        file_path = self.file_path.text().strip()

        if not file_path:
            self.parent.update_content_text("No file selected.")
            return

        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        if file_extension in ['.csv', '.txt']:
            try:
                # Try to read the file with pandas' automatic delimiter detection
                df = pd.read_csv(file_path, engine='python', sep=None)
                
                # If that fails, try specific delimiters
                if len(df.columns) == 1:
                    delimiters = [',', ';', '\t', '|', ' || ', ' | ']
                    for delimiter in delimiters:
                        try:
                            test_df = pd.read_csv(file_path, sep=delimiter, engine='python')
                            if len(test_df.columns) > 1:
                                df = test_df
                                break
                        except:
                            continue

                self.parent.update_content_text(df)
                
            except Exception as e:
                self.parent.update_content_text(f"Error reading file: {str(e)}")
        elif file_extension in ['.nc', '.netcdf']:
            message = "The file is a NetCDF file."
            self.parent.update_content_text(message)
        else:
            message = "Unknown file type."
            self.parent.update_content_text(message)

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