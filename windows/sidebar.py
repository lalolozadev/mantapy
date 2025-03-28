from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QSpacerItem, QSizePolicy,
                            QComboBox
                            )
from PyQt6.QtCore import Qt
import config.button as button
import config.text as text
import netCDF4 as nc
import os
import pandas as pd

# class LoadFileSection(QWidget):
#     def __init__(self, parent):
#         super().__init__()
#         self.parent = parent  # Guardamos la referencia del padre
#         layout = QVBoxLayout(self)

#         self.title_section = QLabel(
#             f"<span style='font-size:{text.text_subtitle}px;'><b> Load file </b></span><br>"
#             f"<span style='font-size:{text.text_normal}px;'> Select a file from your device to proceed. </span><br>"
#             f"<span style='font-size:{text.text_normal}px;'> Supported formats include .csv, .txt, and .nc. </span><br><br>"
#             f"<span style='font-size:{text.text_normal}px;'> Click the button below to browse. </span><br>"
#         )

#         self.title_section.setWordWrap(True)
#         self.title_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
#         layout.addWidget(self.title_section)

#         # Botón Load File
#         self.btn_load = QPushButton("Load File")
#         self.btn_load.clicked.connect(parent.select_file)
#         self.btn_load.setFixedSize(button.nav_size[0], button.nav_size[1])
#         self.btn_load.setStyleSheet(button.next)
#         layout.addWidget(self.btn_load)

#         # Campo de texto para mostrar la ruta del archivo
#         self.file_path = QLineEdit()
#         self.file_path.setPlaceholderText("Load a file")
#         self.file_path.setFixedSize(button.nav_size[0], button.nav_size[1])
#         self.file_path.setStyleSheet(button.file_input)
#         layout.addWidget(self.file_path)

#         self.file_path.textChanged.connect(self.analyze_file_type)

#         # Menús desplegables (inicialmente ocultos)
#         self.variable_section = QLabel(
#             f"<span style='font-size:{text.text_subtitle}px;'><br><b> Variables  </b></span><br>"
#             f"<span style='font-size:{text.text_normal}px;'> Choose the variables you want to include </span><br>"
#             f"<span style='font-size:{text.text_normal}px;'> in your plot. </span><br>"
#         )
#         self.label_select1 = QLabel(f"<span style='font-size:{text.text_normal}px;'> Select first variable (x axis): </span>")
#         self.label_select2 = QLabel(f"<span style='font-size:{text.text_normal}px;'> Select second variable (y axis): </span>")
#         self.label_select3 = QLabel(f"<span style='font-size:{text.text_normal}px;'> (Optional) Select third variable (z axis): </span>")
#         self.combo_select1 = QComboBox()
#         self.combo_select2 = QComboBox()
#         self.combo_select3 = QComboBox()
#         self.variable_section.hide()
#         self.label_select1.hide()
#         self.label_select2.hide()
#         self.label_select3.hide()
#         self.combo_select1.hide()
#         self.combo_select2.hide()
#         self.combo_select3.hide()
#         layout.addWidget(self.variable_section)
#         layout.addWidget(self.label_select1)
#         layout.addWidget(self.combo_select1)
#         layout.addWidget(self.label_select2)
#         layout.addWidget(self.combo_select2)
#         layout.addWidget(self.label_select3)
#         layout.addWidget(self.combo_select3)

#         layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

#         # Botón Next
#         self.btn_next = QPushButton("Next")
#         self.btn_next.clicked.connect(parent.next_section)
#         self.btn_next.setFixedSize(button.nav_size[0], button.nav_size[1])
#         self.btn_next.setStyleSheet(button.next)
#         layout.addWidget(self.btn_next)

#         self.setLayout(layout)

#         # Diccionario de funciones para manejar diferentes tipos de archivos
#         self.file_handlers = {
#             '.csv': self.handle_csv_txt,
#             '.txt': self.handle_csv_txt,
#             '.nc': self.handle_netcdf,
#             '.netcdf': self.handle_netcdf
#         }

#     def analyze_file_type(self):
#         file_path = self.file_path.text().strip()
#         if not file_path:
#             self.parent.update_content_text("No file selected.")
#             return

#         _, file_extension = os.path.splitext(file_path)
#         file_extension = file_extension.lower()

#         handler = self.file_handlers.get(file_extension, self.handle_unknown)
#         handler(file_path)

#     def handle_csv_txt(self, file_path):
#         try:
#             df = pd.read_csv(file_path, engine='python', sep=None)
#             if len(df.columns) == 1:
#                 delimiters = [',', ';', '\t', '|', ' || ', ' | ']
#                 for delimiter in delimiters:
#                     try:
#                         test_df = pd.read_csv(file_path, sep=delimiter, engine='python')
#                         if len(test_df.columns) > 1:
#                             df = test_df
#                             break
#                     except:
#                         continue
#             self.parent.update_content_text(df)
#             self.populate_column_selection(df)
#         except Exception as e:
#             self.parent.update_content_text(f"Error reading file: {str(e)}")

#     def handle_netcdf(self, file_path):
#         try:
#             dataset = nc.Dataset(file_path, 'r')
#             variables = list(dataset.variables.keys())
#             message = f"NetCDF file loaded. Variables: {', '.join(variables)}"
#             dataset.close()
#             self.parent.update_content_text(message)
#         except Exception as e:
#             self.parent.update_content_text(f"Error reading NetCDF file: {str(e)}")

#     def handle_unknown(self, file_path):
#         self.parent.update_content_text("Unknown file type.")

#     def populate_column_selection(self, df):
#         self.combo_select1.clear()
#         self.combo_select2.clear()
#         self.combo_select3.clear()
#         self.combo_select1.addItems(df.columns)
#         self.combo_select2.addItems(df.columns)
#         self.combo_select3.addItems(["None"] + list(df.columns))
#         self.variable_section.show()
#         self.label_select1.show()
#         self.label_select2.show()
#         self.label_select3.show()
#         self.combo_select1.show()
#         self.combo_select2.show()
#         self.combo_select3.show()

class LoadFileSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # Guardamos la referencia del padre
        layout = QVBoxLayout(self)

        self.title_section = QLabel(
            f"<span style='font-size:{text.text_subtitle}px;'><b> Load file </b></span><br>"
            f"<span style='font-size:{text.text_normal}px;'> Select a file from your device to proceed. </span><br>"
            f"<span style='font-size:{text.text_normal}px;'> Supported formats include .csv, .txt, and .nc. </span><br><br>"
            f"<span style='font-size:{text.text_normal}px;'> Click the button below to browse. </span><br>"
        )
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
        self.file_path.setPlaceholderText("Load a file")
        self.file_path.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.file_path.setStyleSheet(button.file_input)
        layout.addWidget(self.file_path)

        self.file_path.textChanged.connect(self.analyze_file_type)

        # Menú desplegable para elegir si la tabla tiene encabezados o no
        self.header_section = QLabel(
            f"<span style='font-size:{text.text_normal}px;'> Does the table have headers? </span>"
        )
        self.header_option = QComboBox()
        self.header_option.addItems(["Has Headers", "No Headers"])
        self.header_option.setFixedSize(button.nav_size[0], button.nav_size[1])
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
        self.label_select1 = QLabel(f"<span style='font-size:{text.text_normal}px;'> Select first variable (x axis): </span>")
        self.label_select2 = QLabel(f"<span style='font-size:{text.text_normal}px;'> Select second variable (y axis): </span>")
        self.label_select3 = QLabel(f"<span style='font-size:{text.text_normal}px;'> (Optional) Select third variable (z axis): </span>")
        self.combo_select1 = QComboBox()
        self.combo_select2 = QComboBox()
        self.combo_select3 = QComboBox()
        self.variable_section.hide()
        self.label_select1.hide()
        self.label_select2.hide()
        self.label_select3.hide()
        self.combo_select1.hide()
        self.combo_select2.hide()
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
        self.btn_next.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.btn_next.setStyleSheet(button.next)
        layout.addWidget(self.btn_next)

        self.setLayout(layout)

        # Diccionario de funciones para manejar diferentes tipos de archivos
        self.file_handlers = {
            '.csv': self.handle_csv_txt,
            '.txt': self.handle_csv_txt,
            '.nc': self.handle_netcdf,
            '.netcdf': self.handle_netcdf
        }

        self.header_option.currentIndexChanged.connect(self.reload_file)

    def analyze_file_type(self):
        file_path = self.file_path.text().strip()
        if not file_path:
            self.parent.update_content_text("No file selected.")
            return

        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        handler = self.file_handlers.get(file_extension, self.handle_unknown)
        handler(file_path)

    def handle_csv_txt(self, file_path):
        try:
            has_headers = self.header_option.currentText() == "Has Headers"
            df = pd.read_csv(file_path, engine='python', sep=None, header=0 if has_headers else None)

            # Si el archivo no tiene encabezados, asignar nombres genéricos
            if not has_headers:
                df.columns = [f"col{i+1}" for i in range(df.shape[1])]

            self.parent.update_content_text(df)
            self.populate_column_selection(df)
        except Exception as e:
            self.parent.update_content_text(f"Error reading file: {str(e)}")

    def handle_netcdf(self, file_path):
        try:
            dataset = nc.Dataset(file_path, 'r')
            variables = list(dataset.variables.keys())
            message = f"NetCDF file loaded. Variables: {', '.join(variables)}"
            dataset.close()
            self.parent.update_content_text(message)
        except Exception as e:
            self.parent.update_content_text(f"Error reading NetCDF file: {str(e)}")

    def handle_unknown(self, file_path):
        self.parent.update_content_text("Unknown file type.")

    def populate_column_selection(self, df):
        self.combo_select1.clear()
        self.combo_select2.clear()
        self.combo_select3.clear()

        self.combo_select1.addItems(df.columns)
        self.combo_select2.addItems(df.columns)
        self.combo_select3.addItems(["None"] + list(df.columns))

        self.header_section.show()
        self.header_option.show()
        
        self.variable_section.show()
        self.label_select1.show()
        self.label_select2.show()
        self.label_select3.show()
        self.combo_select1.show()
        self.combo_select2.show()
        self.combo_select3.show()

    def reload_file(self):
        """ Vuelve a cargar el archivo con la nueva opción de encabezado. """
        file_path = self.file_path.text().strip()
        if file_path:
            self.handle_csv_txt(file_path)




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