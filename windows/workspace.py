from PyQt6.QtCore import Qt
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QFileDialog, QFrame, QStackedWidget,
    QProgressDialog, QApplication, QMessageBox
)
import config.text as text
import pandas as pd
import os
from .sidebar import Sidebar
from windows.sections.load_section import LoadFileSection
from windows.sections.plot_section import PlotSection
from windows.sections.export_section import ExportPlotSection, ExportWorker
from .content_area import ContentSection
from config.colors import *

# Clase principal
class MantapyUI(QWidget):
    def __init__(self):
        super().__init__()
        self.loaded_dataframe = None
        self.init_ui()
        self.setWindowTitle("Workspace - Mantapy")
        self.setStyleSheet(f"background-color: {blanco1};")

    #--------------------------------------------

    def init_ui(self):
        self.setWindowTitle("Mantapy - Data Analysis")
        main_layout = QHBoxLayout(self)

        # Barra lateral
        sidebar = QFrame(self)
        #sidebar.setFixedWidth(350)
        sidebar_layout = QVBoxLayout(sidebar)

        # StackedWidget para cambiar secciones
        self.stacked_widget = QStackedWidget()

        # Agregar las secciones al stack
        self.page_load = LoadFileSection(self)
        self.stacked_widget.addWidget(self.page_load)

        # Área de contenido (derecha)
        self.content_area = ContentSection(text)
        sidebar_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_area)

        self.page_plot = PlotSection(self, self.content_area)
        self.page_plot.restore_plot_settings()
        self.stacked_widget.addWidget(self.page_plot)

        self.export_plot = ExportPlotSection(self)
        self.stacked_widget.addWidget(self.export_plot)

        sidebar_layout.addWidget(self.stacked_widget)
        sidebar.setLayout(sidebar_layout)

        # --- Aquí está el truco: ---
        main_layout.setStretch(0, 1)  # Sidebar: 1 parte
        main_layout.setStretch(1, 2)  # ContentArea: 2 partes

        self.setLayout(main_layout)

        # Maximizar ventana
        screen = self.screen().availableGeometry()
        self.setGeometry(screen.x(), screen.y(), screen.width(), screen.height())

        # Mostrar la primera sección
        self.stacked_widget.setCurrentIndex(0)
    
    #--------------------------------------------
    
    def update_content_text(self, text, as_notebook=False):
        if isinstance(text, pd.DataFrame):
            self.loaded_dataframe = text
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
        next_index = current_index + 1

        if next_index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(next_index)

            if isinstance(self.stacked_widget.widget(next_index), PlotSection):
                self.page_plot.restore_plot_settings()
                plot_section = self.stacked_widget.widget(next_index)
                first_plot_type = plot_section.plot_option.itemText(0)

                x_column = self.page_load.combo_select1.currentText()
                y_column = self.page_load.combo_select2.currentText()

                if self.loaded_dataframe is not None and x_column in self.loaded_dataframe.columns and y_column in self.loaded_dataframe.columns:
                    x_data = self.loaded_dataframe[x_column]
                    y_data = self.loaded_dataframe[y_column]

                    # Render the first plot
                    self.update_content_plot(first_plot_type, x_data, y_data)

                    # <-- Aplica la configuración estética guardada
                    self.page_plot.update_plot_settings()

    #--------------------------------------------

    def previous_section(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)

    #--------------------------------------------

    def update_content_plot(
        self,
        plot_type,
        x_data,
        y_data,
        z_data=None,
        xlim=None,
        ylim=None,
        legend=None,
        title=None,
        xlabel=None,
        ylabel=None,
        grid=None,
        legend_text=None,
        color=None,
        enable_regression=False,      # <--- agrega esto
        regression_type=None          # <--- y esto
    ):
        
        """Pass all plot settings to content_area"""
        self.content_area.update_content_plot(
            plot_type,
            x_data,
            y_data,
            z_data,
            xlim,
            ylim,
            legend,
            title,
            xlabel,
            ylabel,
            grid,
            legend_text,
            color,
            enable_regression,         # <--- y pásalos aquí
            regression_type
        )
    #--------------------------------------------

    def export_plot(self):
        fig = getattr(self.content_area, "current_figure", None)
        if fig is None:
            print("No plot to export.")
            return

        file_name = self.export_plot.file_name.text().strip()
        export_format = self.export_plot.format_option.currentText().lower()

        if not file_name:
            print("Please enter a file name.")
            return

        dir_path = self.export_plot.dir_path.text().strip()
        file_name = self.export_plot.file_name.text().strip() + f".{export_format}"
        if dir_path and file_name:
            full_path = os.path.join(dir_path, file_name)
        else:
            full_path = file_name

        # Barra de progreso modal sobre la ventana principal
        self.progress = QProgressDialog("Exporting plot...", None, 0, 0, self)
        self.progress.setWindowTitle("Please wait")
        self.progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress.setMinimumDuration(0)
        self.progress.show()

        # Crear y lanzar el worker en un hilo
        self.export_thread = QThread()
        self.export_worker = ExportWorker(fig, full_path, export_format)
        self.export_worker.moveToThread(self.export_thread)
        self.export_thread.started.connect(self.export_worker.run)
        self.export_worker.finished.connect(self.export_thread.quit)
        self.export_worker.finished.connect(self.progress.close)
        self.export_worker.finished.connect(lambda: print(f"Plot exported as {full_path}"))
        self.export_worker.error.connect(self.export_thread.quit)
        self.export_worker.error.connect(self.progress.close)
        self.export_worker.error.connect(lambda msg: print(f"Error exporting plot: {msg}"))
        self.export_thread.start()