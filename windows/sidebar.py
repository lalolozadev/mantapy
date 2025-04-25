import config.button as button
import config.text as text
import netCDF4 as nc
import os
import pandas as pd
from utils.file_handlers import read_table_file
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QSpacerItem, QSizePolicy,
                            QComboBox, QCheckBox, QScrollArea
                            )

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
        self.variable_section.hide()

        self.label_select1 = QLabel(f"<span style='font-size:{text.text_normal}px;'> Select first variable (x axis): </span>")
        self.label_select1.hide()

        self.label_select2 = QLabel(f"<span style='font-size:{text.text_normal}px;'> Select second variable (y axis): </span>")
        self.label_select2.hide()

        self.label_select3 = QLabel(f"<span style='font-size:{text.text_normal}px;'> (Optional) Select third variable (z axis): </span>")
        self.label_select3.hide()

        self.combo_select1 = QComboBox()
        self.combo_select1.hide()

        self.combo_select2 = QComboBox()
        self.combo_select2.hide()

        self.combo_select3 = QComboBox()
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
        self.label_select3.show()
        self.combo_select1.show()
        self.combo_select2.show()
        self.combo_select3.show()

    #--------------------------------------------

    def reload_file(self):
        """ Vuelve a cargar el archivo con la nueva opción de encabezado. """
        file_path = self.file_path.text().strip()
        if file_path:
            self.handle_csv_txt(file_path)

#--------------------------------------------

class PlotSection(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
        # Crear un área de scroll
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Apply a custom stylesheet to remove the border
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;  /* Remove the border */
                background: transparent;  /* Optional: Make the background transparent */
            }
            QScrollBar:vertical {
                width: 10px;  /* Customize the width of the vertical scrollbar */
                background: #f0f0f0;  /* Background color of the scrollbar */
                border: none;  /* Remove the border around the scrollbar */
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;  /* Color of the scrollbar handle */
                border-radius: 5px;  /* Rounded corners for the scrollbar handle */
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;  /* Darker color when hovering over the scrollbar handle */
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;  /* Remove the up and down arrows */
            }
        """)

        # Contenedor para el contenido de la sección
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        self.title_section = QLabel(
            f"<span style='font-size:{text.text_subtitle}px;'><b> Make your plot </b></span><br>"
            f"<span style='font-size:{text.text_normal}px;'>Select your preferred plot type and customize its appearance to best showcase your insights.</span><br>"
        )
        self.title_section.setWordWrap(True)
        self.title_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.title_section)

        self.plot_type = QLabel(
            f"<span style='font-size:{text.text_normal}px;'> Plot type </span>"
        )
        self.plot_type.setWordWrap(True)
        self.plot_type.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.plot_type)

        self.plot_option = QComboBox()
        self.plot_option.addItems(["Line", "Scatter", "Bar"])
        self.plot_option.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.plot_option.currentTextChanged.connect(self.update_plot_preview)
        layout.addWidget(self.plot_option)

        self.plot_labels = QLabel(
            f"<span style='font-size:{text.text_normal}px;'><br> Labels </span>"
        )
        self.plot_labels.setWordWrap(True)
        self.plot_labels.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.plot_labels)

        self.checkbox_title = QCheckBox("Set title")
        self.checkbox_title.stateChanged.connect(self.toggle_title_input)
        layout.addWidget(self.checkbox_title)

        self.sq_title = QLineEdit()
        self.sq_title.setPlaceholderText("Type title name")
        self.sq_title.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.sq_title.setStyleSheet(button.file_input)
        self.sq_title.hide()
        layout.addWidget(self.sq_title)

        # Crear checkbox con texto
        self.checkbox_xlabel = QCheckBox("Set x label")
        self.checkbox_xlabel.stateChanged.connect(self.toggle_xlabel_input)
        layout.addWidget(self.checkbox_xlabel)

        self.sq_xlabel = QLineEdit()
        self.sq_xlabel.setPlaceholderText("Type x label name")
        self.sq_xlabel.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.sq_xlabel.setStyleSheet(button.file_input)
        self.sq_xlabel.hide()
        layout.addWidget(self.sq_xlabel)

        self.checkbox_ylabel = QCheckBox("Set y label")
        self.checkbox_ylabel.stateChanged.connect(self.toggle_ylabel_input)
        layout.addWidget(self.checkbox_ylabel)

        self.sq_ylabel = QLineEdit()
        self.sq_ylabel.setPlaceholderText("Type y label name")
        self.sq_ylabel.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.sq_ylabel.setStyleSheet(button.file_input)
        self.sq_ylabel.hide()
        layout.addWidget(self.sq_ylabel)

        self.style_section = QLabel(
            f"<span style='font-size:{text.text_normal}px;'><br> Style </span>"
        )
        self.style_section.setWordWrap(True)
        self.style_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.style_section)

        self.checkbox_grid = QCheckBox("Show grid")
        self.checkbox_grid.setChecked(True)
        layout.addWidget(self.checkbox_grid)

        self.checkbox_legend = QCheckBox("Show legend")
        self.checkbox_legend.setChecked(False)
        layout.addWidget(self.checkbox_legend)

        self.sq_legend = QLineEdit()
        self.sq_legend.setPlaceholderText("Type legend name")
        self.sq_legend.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.sq_legend.setStyleSheet(button.file_input)
        self.sq_legend.hide()
        self.checkbox_legend.stateChanged.connect(self.toggle_legend_input)
        layout.addWidget(self.sq_legend)
        
        self.btn_back = QPushButton("Back")
        self.btn_back.clicked.connect(parent.previous_section)
        self.btn_back.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.btn_back.setStyleSheet(button.back)
        
        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(parent.next_section)
        self.btn_next.setFixedSize(button.nav_size[0], button.nav_size[1])
        self.btn_next.setStyleSheet(button.next)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(self.btn_next)
        layout.addWidget(self.btn_back)

        # Configurar el área de scroll
        scroll_area.setWidget(content_widget)

        # Layout principal de la sección
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
    
    #----------------------------------------

    def toggle_title_input(self, state):
        """Show or hide the title input based on the checkbox state."""
        if state == 2:
            self.sq_title.show()
        else:
            self.sq_title.hide()

    def toggle_xlabel_input(self, state):
        """Show or hide the x label input based on the checkbox state."""
        if state == 2:
            self.sq_xlabel.show()
        else:
            self.sq_xlabel.hide()

    def toggle_ylabel_input(self, state):
        """Show or hide the y label input based on the checkbox state."""
        if state == 2:
            self.sq_ylabel.show()
        else:
            self.sq_ylabel.hide()
    
    def toggle_legend_input(self, state):
        """Show or hide the legend input based on the checkbox state."""
        if state == 2:
            self.sq_legend.show()
        else:
            self.sq_legend.hide()

        #----------------------------------------

    def update_plot_preview(self, plot_type):
        """Updates the plot preview in the content area."""
        # Get selected columns from the Load File section
        x_column = self.parent.page_load.combo_select1.currentText()
        y_column = self.parent.page_load.combo_select2.currentText()
        z_column = self.parent.page_load.combo_select3.currentText()

        # Get the loaded DataFrame
        df = self.parent.loaded_dataframe

        # Validate that the DataFrame and selected columns exist
        if df is None or x_column not in df.columns or y_column not in df.columns:
            self.parent.update_content_text("Please select valid columns and load a dataset.")
            return

        # Extract data for the plot
        x_data = df[x_column]
        y_data = df[y_column]
        z_data = df[z_column] if z_column != "None" else None

        # Update the plot in the content area
        self.parent.update_content_plot(plot_type, x_data, y_data, z_data)

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