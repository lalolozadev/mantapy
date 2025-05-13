from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QStackedWidget
)

from windows.sections.load_section import LoadFileSection
from windows.sections.plot_section import PlotSection

class Sidebar(QWidget):
    def __init__(self, parent, content_area):
        super().__init__()
        self.parent = parent
        self.content_area = content_area
        self.init_ui()

    def init_ui(self):
        # Crear layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear el widget apilado para las secciones
        self.stacked_widget = QStackedWidget()
        
        # Crear las secciones
        self.page_load = LoadFileSection(self.parent)
        self.page_plot = PlotSection(self.parent, self.content_area)
        
        # Añadir secciones al widget apilado
        self.stacked_widget.addWidget(self.page_load)
        self.stacked_widget.addWidget(self.page_plot)
        
        # Añadir widget apilado al layout
        layout.addWidget(self.stacked_widget)
        
        self.setLayout(layout)
        
    def show_section(self, index):
        """Cambia a la sección especificada por el índice."""
        self.stacked_widget.setCurrentIndex(index)