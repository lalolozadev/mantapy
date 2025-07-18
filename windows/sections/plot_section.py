import config.button as button
import config.text as text
import config.menu_style as menu_style
import matplotlib.colors as mcolors
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QSpacerItem, QSizePolicy, QComboBox, QScrollArea
)
from PyQt6.QtGui import QPixmap, QPainter, QColor, QIcon

from .plot_components.plot_labels import PlotLabelsComponent
from .plot_components.plot_style import PlotStyleComponent
from .plot_components.plot_limits import PlotLimitsComponent
from .plot_components.plot_regression import PlotRegressionComponent

from config.colors import *
from config.scroll_style import scroll_style

class PlotSection(QWidget):
    def __init__(self, parent, content_area):
        super().__init__()
        self.parent = parent
        self.content_area = content_area
        self.init_ui()

    def init_ui(self):
        # Crear un área de scroll
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(scroll_style)

        # Contenedor para el contenido de la sección
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        # Título de la sección
        self.title_section = QLabel(
            f"<span style='font-size:{text.text_subtitle}px;'><b> Make your plot </b></span><br>"
            f"<span style='font-size:{text.text_normal}px;'>Select your preferred plot type and customize its appearance to best showcase your insights.</span><br>"
        )
        self.title_section.setWordWrap(True)
        self.title_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.title_section)

        # Plot type selection
        self.setup_plot_type(layout)
        
        # Color selection
        self.setup_color_selection(layout)
        
        # Añadir componentes
        self.labels_component = PlotLabelsComponent(self, layout)
        self.style_component = PlotStyleComponent(self, layout)
        self.limits_component = PlotLimitsComponent(self,layout)
        self.regression_component = PlotRegressionComponent(self, layout)

        # Navigation buttons
        self.setup_navigation_buttons(layout)

        # Configurar el área de scroll
        scroll_area.setWidget(content_widget)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Estado persistente
        self.plot_settings = {
            "title": "",
            "xlabel": "",
            "ylabel": "",
            "grid": False,
            "legend": False,
            "legend_text": "",
            "xlim": None,
            "ylim": None,
            "color": None
        }

    def setup_plot_type(self, layout):
        self.plot_type = QLabel(
            f"<span style='font-size:{text.text_normal}px;'> Plot type </span>"
        )
        self.plot_type.setWordWrap(True)
        self.plot_type.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.plot_type)

        self.plot_option = QComboBox()
        self.plot_option.addItems(["Line", "Scatter", "Bar"])
        self.plot_option.setFont(text.qfont_small)
        self.plot_option.setStyleSheet(menu_style.menu)
        self.plot_option.currentTextChanged.connect(self.update_plot_preview)
        layout.addWidget(self.plot_option)

    def setup_color_selection(self, layout):
        # Color selection
        self.color_title = QLabel(
            f"<span style='font-size:{text.text_normal}px;'><br> Color </span>"
        )
        self.color_title.setWordWrap(True)
        self.color_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.color_title)

        self.color_menu = QComboBox()
        self.color_menu.setFont(text.qfont_small)
        self.color_menu.setStyleSheet(menu_style.menu)
        # Obtener colores y nombres
        color_dict = mcolors.TABLEAU_COLORS
        for full_name in color_dict:
            color_name = full_name.replace('tab:', '')
            color_hex = color_dict[full_name]

            # Crear ícono de color
            pixmap = QPixmap(20, 20)
            pixmap.fill(QColor("transparent"))

            painter = QPainter(pixmap)
            painter.setBrush(QColor(color_hex))
            painter.setPen(QColor(color_hex))
            painter.drawEllipse(3, 3, 14, 14)
            painter.end()

            icon = QIcon(pixmap)
            self.color_menu.addItem(icon, color_name)
        
        # Conectar a un método específico para manejar cambios de color
        self.color_menu.currentTextChanged.connect(self.on_color_changed)
        layout.addWidget(self.color_menu)

    def on_color_changed(self, color_name):
        """Handle color selection changes"""
        color_hex = mcolors.TABLEAU_COLORS[f'tab:{color_name}']
        self.plot_settings["color"] = color_hex
        self.update_plot_preview(self.plot_option.currentText())

    def setup_navigation_buttons(self, layout):
        self.btn_back = QPushButton("Back")
        self.btn_back.clicked.connect(self.parent.previous_section)
        self.btn_back.setStyleSheet(button.back)
        
        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(self.parent.next_section)
        self.btn_next.setStyleSheet(button.next)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(self.btn_next)
        layout.addWidget(self.btn_back)

    def update_plot_preview(self, plot_type):
        # Get selected columns and data
        x_column = self.parent.page_load.combo_select1.currentText()
        y_column = self.parent.page_load.combo_select2.currentText()
        z_column = self.parent.page_load.combo_select3.currentText()

        df = self.parent.loaded_dataframe
        if df is None or x_column not in df.columns or y_column not in df.columns:
            self.parent.update_content_text("Please select valid columns and load a dataset.")
            return

        # Get settings from components
        label_settings = self.labels_component.get_label_settings()
        style_settings = self.style_component.get_style_settings()
        limit_settings = self.limits_component.get_limit_settings()

        # ...existing code...
        self.parent.update_content_plot(
            plot_type,
            df[x_column],
            df[y_column],
            df[z_column] if z_column != "None" else None,
            limit_settings["xlim"],
            limit_settings["ylim"],
            style_settings["legend"],
            label_settings["title"],
            label_settings["xlabel"],
            label_settings["ylabel"],
            style_settings["grid"],
            style_settings["legend_text"],
            self.plot_settings["color"],  # color
            self.regression_component.button_enable_regression.isChecked(),  # enable_regression
            self.regression_component.sq_regression_type.currentText()     # regression_type
        )

    def restore_plot_settings(self):
        self.labels_component.restore_settings(self.plot_settings)
        self.style_component.restore_settings(self.plot_settings)
        self.limits_component.restore_settings(self.plot_settings)
        self.update_plot_preview(self.plot_option.currentText())

    def update_plot_settings(self):
        """Update plot settings from all components and refresh the plot"""
        # Get settings from all components
        label_settings = self.labels_component.get_label_settings()
        style_settings = self.style_component.get_style_settings()
        limit_settings = self.limits_component.get_limit_settings()
        
        # Update plot_settings dictionary with all settings
        self.plot_settings.update({
            "title": label_settings["title"],
            "xlabel": label_settings["xlabel"],
            "ylabel": label_settings["ylabel"],
            "grid": style_settings["grid"],
            "legend": style_settings["legend"],
            "legend_text": style_settings["legend_text"],
            "xlim": limit_settings["xlim"],
            "ylim": limit_settings["ylim"]
        })

        # Actualizar el color si existe
        if self.color_menu.currentText():
            color_hex = mcolors.TABLEAU_COLORS[f'tab:{self.color_menu.currentText()}']
            self.plot_settings["color"] = color_hex

        # La clave es llamar a update_plot_preview DESPUÉS de actualizar todos los settings
        self.update_plot_preview(self.plot_option.currentText())
