import config.button as button
import config.text as text
import netCDF4 as nc
import os
import pandas as pd
from utils.file_handlers import read_table_file
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QLineEdit, QSpacerItem, QSizePolicy, QComboBox
)
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from config.colors import *
import config.menu_style as menu_style

class ExportPlotSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # Guardamos la referencia del padre
        layout = QVBoxLayout(self)

        self.title_section = QLabel(
            f"<span style='font-size:{text.text_subtitle}px;'><b> Export Your Plot </b></span><br>"
            f"<span style='font-size:{text.text_normal}px;'>Save your plot in PNG, JPEG, PDF or SVG format to share or use in reports. </span><br><br>"
            f"<span style='font-size:{text.text_normal}px;'> Choose file name </span>"
        )
        self.title_section.setWordWrap(True)
        self.title_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.title_section)

        # Campo de texto para mostrar el nombre del archivo
        self.file_name = QLineEdit()
        self.file_name.setPlaceholderText("Enter file name")
        self.file_name.setStyleSheet(menu_style.file_input_style)
        layout.addWidget(self.file_name)

        # Menú desplegable para elegir el formato de exportación
        self.format_section = QLabel(
            f"<span style='font-size:{text.text_normal}px;'> Choose export format: </span>"
        )
        self.format_option = QComboBox()
        self.format_option.addItems(["PNG", "JPEG", "PDF", "SVG"])
        self.format_option.setFont(text.qfont_small)
        self.format_option.setStyleSheet(menu_style.menu)
        layout.addWidget(self.format_section)
        layout.addWidget(self.format_option)

        self.directory_section = QLabel(
            f"<span style='font-size:{text.text_normal}px;'> Select the directory where you want to save the plot </span>"
        )
        layout.addWidget(self.directory_section)

        # Sección para seleccionar directorio
        dir_layout = QHBoxLayout()
        self.dir_path = QLineEdit()
        self.dir_path.setPlaceholderText("Select directory")
        self.dir_path.setReadOnly(True)
        self.dir_path.setStyleSheet(menu_style.file_input_style)

        btn_browse = QPushButton("Browse dir")
        btn_browse.setStyleSheet(button.export_plot)
        btn_browse.clicked.connect(self.select_directory)
        dir_layout.addWidget(self.dir_path)
        dir_layout.addWidget(btn_browse)
        layout.addLayout(dir_layout)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Botón Export Plot
        self.btn_export = QPushButton("Export Plot")
        self.btn_export.clicked.connect(parent.export_plot)
        self.btn_export.setStyleSheet(button.next)
        layout.addWidget(self.btn_export)

        # Botón Back para regresar a la sección anterior
        self.btn_back = QPushButton("Back")
        self.btn_back.setStyleSheet(button.back)
        self.btn_back.clicked.connect(parent.previous_section)
        layout.addWidget(self.btn_back)

        # Boton para volver a la sección de carga
        self.btn_back = QPushButton("Back to Load Section")
        self.btn_back.clicked.connect(lambda: parent.stacked_widget.setCurrentWidget(parent.page_load))
        self.btn_back.setStyleSheet(button.back_load)
        layout.addWidget(self.btn_back)

    
    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.dir_path.setText(directory)

class ExportWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, fig, file_name, export_format):
        super().__init__()
        self.fig = fig
        self.file_name = file_name
        self.export_format = export_format

    def run(self):
        try:
            if self.export_format in ["png", "jpeg", "pdf", "svg"]:
                self.fig.write_image(self.file_name)
            else:
                self.fig.write_html(self.file_name)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))