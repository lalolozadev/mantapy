import config.button as button
import config.text as text
import config.menu_style as menu_style
import netCDF4 as nc
import os
import pandas as pd
from utils.file_handlers import read_table_file
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QLineEdit, QSpacerItem, QSizePolicy, QComboBox,
    QHBoxLayout
)
from config.colors import *

class LoadFileSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # Guardamos la referencia del padre
        layout = QVBoxLayout(self)

        self.title_section = QLabel(
            f"<span style='font-size:{text.text_subtitle}px;'><b> Load Your Data </b></span><br>"
            f"<span style='font-size:{text.text_normal}px;'>Upload your dataset to kickstart your analysis journey. </span>"
            f"<span style='font-size:{text.text_normal}px;'>We support popular formats like <b>.csv</b>, <b>.txt</b>, and <b>.nc</b>, making it easy to get started. </span><br><br>"
            f"<span style='font-size:{text.text_normal}px;'> Click the button below to browse your files. </span><br>"
        )
        self.title_section.setWordWrap(True)
        self.title_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.title_section)

        # Botón Load File

        # Campo de texto para mostrar la ruta del archivo
        dir_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Load a file")
        self.file_path.setStyleSheet(button.file_input)
        self.file_path.setStyleSheet(menu_style.file_input_style)
        dir_layout.addWidget(self.file_path)

        self.btn_load = QPushButton("Load File")
        self.btn_load.clicked.connect(parent.select_file)
        self.btn_load.setStyleSheet(button.load_file)
        dir_layout.addWidget(self.btn_load)
        layout.addLayout(dir_layout)

        self.file_path.textChanged.connect(self.analyze_file_type)

        # Menú desplegable para elegir si la tabla tiene encabezados o no
        self.header_section = QLabel(
            f"<span style='font-size:{text.text_normal}px;'> Does the table have headers? </span>"
        )
        self.header_option = QComboBox()
        self.header_option.addItems(["Has Headers", "No Headers"])
        self.header_option.setFont(text.qfont_small)
        self.header_option.setStyleSheet(menu_style.menu)
        self.header_section.hide()
        self.header_option.hide()
        layout.addWidget(self.header_section)
        layout.addWidget(self.header_option)

        # Menús desplegables (inicialmente ocultos)
        self.variable_section = QLabel(
            f"<span style='font-size:{text.text_subtitle}px;'><br><b> Variables  </b></span><br>"
            f"<span style='font-size:{text.text_normal}px;'> Choose the variables you want to include </span><br>"
            f"<span style='font-size:{text.text_normal}px;'> in your plot. </span><br>"
        )
        self.variable_section.hide()

        self.label_select1 = QLabel(f"<span style='font-size:{text.text_normal}px;'> Select first variable (x axis): </span>")
        self.label_select1.hide()

        self.label_select2 = QLabel(f"<span style='font-size:{text.text_normal}px;'> Select second variable (y axis): </span>")
        self.label_select2.hide()

        self.label_select3 = QLabel(f"<span style='font-size:{text.text_normal}px;'> (Optional) Select third variable (z axis): </span>")
        self.label_select3.hide()

        self.combo_select1 = QComboBox()
        self.combo_select1.setFont(text.qfont_small)
        self.combo_select1.setStyleSheet(menu_style.menu)
        self.combo_select1.hide()

        self.combo_select2 = QComboBox()
        self.combo_select2.setFont(text.qfont_small)
        self.combo_select2.setStyleSheet(menu_style.menu)  
        self.combo_select2.hide()

        self.combo_select3 = QComboBox()
        self.combo_select3.setFont(text.qfont_small)
        self.combo_select3.hide()

        layout.addWidget(self.variable_section)
        layout.addWidget(self.label_select1)
        layout.addWidget(self.combo_select1)
        layout.addWidget(self.label_select2)
        layout.addWidget(self.combo_select2)
        layout.addWidget(self.label_select3)
        layout.addWidget(self.combo_select3)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Botón Next
        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(parent.next_section)
        #self.btn_next.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.btn_next.setStyleSheet(button.next)
        layout.addWidget(self.btn_next)      

        self.setLayout(layout)

        # Diccionario de funciones para manejar diferentes tipos de archivos
        self.file_handlers = {
            '.csv': self.handle_csv_txt,
            '.txt': self.handle_csv_txt,
            '.xls': self.handle_csv_txt,    # <-- Añade esta línea
            '.xlsx': self.handle_csv_txt,   # <-- Y esta línea
            '.nc': self.handle_netcdf,
            '.netcdf': self.handle_netcdf
        }

        self.header_option.currentIndexChanged.connect(self.reload_file)

    #--------------------------------------------

    def analyze_file_type(self):
        file_path = self.file_path.text().strip()
        if not file_path:
            self.parent.update_content_text("No file selected.")
            return

        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()
        handler = self.file_handlers.get(file_extension, self.handle_unknown)
        handler(file_path)
    
    #--------------------------------------------

    def handle_csv_txt(self, file_path):
        try:
            has_headers = self.header_option.currentText() == "Has Headers"
            df = read_table_file(file_path, has_headers=has_headers)
            self.parent.update_content_text(df)
            self.populate_column_selection(df)
        except Exception as e:
            self.parent.update_content_text(f"Error reading file: {str(e)}")

    #--------------------------------------------

    def handle_netcdf(self, file_path):
        try:
            dataset = nc.Dataset(file_path, 'r')
            variables = list(dataset.variables.keys())
            message = f"NetCDF file loaded. Variables: {', '.join(variables)}"
            dataset.close()
            self.parent.update_content_text(message)
        except Exception as e:
            self.parent.update_content_text(f"Error reading NetCDF file: {str(e)}")
    
    #--------------------------------------------

    def handle_unknown(self, file_path):
        self.parent.update_content_text("Unknown file type.")

    #--------------------------------------------

    def populate_column_selection(self, df):
        self.combo_select1.clear()
        self.combo_select1.addItems(df.columns)

        self.combo_select2.clear()
        self.combo_select2.addItems(df.columns)

        self.combo_select3.clear()
        self.combo_select3.addItems(["None"] + list(df.columns))

        self.header_section.show()
        self.header_option.show()
        self.variable_section.show()
        self.label_select1.show()
        self.label_select2.show()
        #self.label_select3.show()
        self.combo_select1.show()
        self.combo_select2.show()
        #self.combo_select3.show()

    #--------------------------------------------

    def reload_file(self):
        """ Vuelve a cargar el archivo con la nueva opción de encabezado. """
        file_path = self.file_path.text().strip()
        if file_path:
            self.handle_csv_txt(file_path)
