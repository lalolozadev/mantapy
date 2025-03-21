from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QFileDialog, QLineEdit, QFrame, QStackedWidget, QComboBox, QLabel
)
from PyQt6.QtGui import QScreen
from .sidebar import LoadFileSection, VariablesSection, PlotSection, ExportSection

# Clase principal
class MantapyUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Mantapy - Data Analysis")
        main_layout = QHBoxLayout(self)

        # Barra lateral
        sidebar = QFrame(self)
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(sidebar)

        # Menú desplegable
        self.menu = QComboBox()
        self.menu.addItems(["Load File", "Variables", "Plot", "Export"])
        self.menu.currentIndexChanged.connect(self.change_section)
        sidebar_layout.addWidget(self.menu)

        # StackedWidget para cambiar secciones
        self.stacked_widget = QStackedWidget()

        # Agregar las secciones al stack
        self.page_load = LoadFileSection(self)
        self.page_variables = VariablesSection()
        self.page_plot = PlotSection()
        self.page_export = ExportSection()

        self.stacked_widget.addWidget(self.page_load)
        self.stacked_widget.addWidget(self.page_variables)
        self.stacked_widget.addWidget(self.page_plot)
        self.stacked_widget.addWidget(self.page_export)

        sidebar_layout.addWidget(self.stacked_widget)
        sidebar.setLayout(sidebar_layout)

        # Área de contenido (derecha)
        content_area = QFrame(self)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area)
        self.setLayout(main_layout)

        self.menu.setCurrentIndex(0)
        self.stacked_widget.setCurrentIndex(0)

        # Maximizar ventana
        screen = self.screen().availableGeometry()
        self.setGeometry(screen.x(), screen.y(), screen.width(), screen.height())

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file")
        if file_path:
            self.page_load.file_path.setText(file_path)
            self.menu.setCurrentIndex(1)
            self.stacked_widget.setCurrentIndex(1)

    def change_section(self, index):
        self.stacked_widget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication([])
    window = MantapyUI()
    window.show()
    app.exec()