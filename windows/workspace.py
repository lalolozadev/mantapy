from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QFileDialog, QFrame, QStackedWidget
    
)
import config.text as text
import pandas as pd
from .sidebar import LoadFileSection, VariablesSection, PlotSection, ExportSection
from .content_area import ContentSection

# Clase principal
class MantapyUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    #--------------------------------------------

    def init_ui(self):
        self.setWindowTitle("Mantapy - Data Analysis")
        main_layout = QHBoxLayout(self)

        # Barra lateral
        sidebar = QFrame(self)
        sidebar.setFixedWidth(350)
        sidebar_layout = QVBoxLayout(sidebar)

        # StackedWidget para cambiar secciones
        self.stacked_widget = QStackedWidget()

        # Agregar las secciones al stack
        self.page_load = LoadFileSection(self)
        self.stacked_widget.addWidget(self.page_load)

        self.page_variables = VariablesSection(self)
        self.stacked_widget.addWidget(self.page_variables)

        self.page_plot = PlotSection(self)
        self.stacked_widget.addWidget(self.page_plot)

        self.page_export = ExportSection(self)
        self.stacked_widget.addWidget(self.page_export)

        sidebar_layout.addWidget(self.stacked_widget)
        sidebar.setLayout(sidebar_layout)

        # Área de contenido (derecha)
        self.content_area = ContentSection(text)
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_area)

        self.setLayout(main_layout)

        # Maximizar ventana
        screen = self.screen().availableGeometry()
        self.setGeometry(screen.x(), screen.y(), screen.width(), screen.height())

        # Mostrar la primera sección
        self.stacked_widget.setCurrentIndex(0)
    
    #--------------------------------------------
    
    def update_content_text(self, text, as_notebook=False):
        if isinstance(text, pd.DataFrame):
            self.content_area.update_content_table(text)
        else:
            self.content_area.update_content_text(text)
    
    #--------------------------------------------

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file")
        if file_path:
            self.page_load.file_path.setText(file_path)

    #--------------------------------------------

    def next_section(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(current_index + 1)
    
    #--------------------------------------------

    def previous_section(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)
