import config.button as button
import config.text as text
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

        # Update plot with all settings
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
            self.plot_settings["color"]  # Usar el color guardado en plot_settings
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


# import config.button as button
# import config.text as text
# import matplotlib.colors as mcolors
# from PyQt6.QtCore import Qt
# from PyQt6.QtWidgets import (
#     QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
#     QSpacerItem, QSizePolicy, QComboBox, QCheckBox, QScrollArea
# )
# from PyQt6.QtGui import QPixmap, QPainter, QColor, QIcon


# class PlotSection(QWidget):
#     def __init__(self, parent, content_area):
#         super().__init__()
#         self.parent = parent
#         self.content_area = content_area
        
#         # Crear un área de scroll
#         scroll_area = QScrollArea(self)
#         scroll_area.setWidgetResizable(True)

#         # Apply a custom stylesheet to remove the border
#         scroll_area.setStyleSheet("""
#             QScrollArea {
#                 border: none;  /* Remove the border */
#                 background: transparent;  /* Optional: Make the background transparent */
#             }
#             QScrollBar:vertical {
#                 width: 10px;  /* Customize the width of the vertical scrollbar */
#                 background: #f0f0f0;  /* Background color of the scrollbar */
#                 border: none;  /* Remove the border around the scrollbar */
#             }
#             QScrollBar::handle:vertical {
#                 background: #c0c0c0;  /* Color of the scrollbar handle */
#                 border-radius: 5px;  /* Rounded corners for the scrollbar handle */
#             }
#             QScrollBar::handle:vertical:hover {
#                 background: #a0a0a0;  /* Darker color when hovering over the scrollbar handle */
#             }
#             QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
#                 height: 0px;  /* Remove the up and down arrows */
#             }
#         """)

#         # Contenedor para el contenido de la sección
#         content_widget = QWidget()
#         layout = QVBoxLayout(content_widget)

#         self.title_section = QLabel(
#             f"<span style='font-size:{text.text_subtitle}px;'><b> Make your plot </b></span><br>"
#             f"<span style='font-size:{text.text_normal}px;'>Select your preferred plot type and customize its appearance to best showcase your insights.</span><br>"
#         )
#         self.title_section.setWordWrap(True)
#         self.title_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
#         layout.addWidget(self.title_section)

#         # Plot type selection
#         self.plot_type = QLabel(
#             f"<span style='font-size:{text.text_normal}px;'> Plot type </span>"
#         )
#         self.plot_type.setWordWrap(True)
#         self.plot_type.setAlignment(Qt.AlignmentFlag.AlignLeft)
#         layout.addWidget(self.plot_type)

#         self.plot_option = QComboBox()
#         self.plot_option.addItems(["Line", "Scatter", "Bar"])
#         #self.plot_option.setFixedSize(button.nav_size[0], button.nav_size[1])
#         self.plot_option.currentTextChanged.connect(self.update_plot_preview)
#         layout.addWidget(self.plot_option)

#         # Color selection
#         self.color_title = QLabel(
#             f"<span style='font-size:{text.text_normal}px;'><br> Color </span>"
#         )
#         self.color_title.setWordWrap(True)
#         self.color_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
#         layout.addWidget(self.color_title)

#         self.color_menu = QComboBox()
#         # Obtener colores y nombres
#         color_dict = mcolors.TABLEAU_COLORS
#         for full_name in color_dict:
#             color_name = full_name.replace('tab:', '')
#             color_hex = color_dict[full_name]

#             # Crear ícono de color (un círculo o rectángulo)
#             pixmap = QPixmap(20, 20)
#             pixmap.fill(QColor("transparent"))

#             painter = QPainter(pixmap)
#             painter.setBrush(QColor(color_hex))
#             painter.setPen(QColor(color_hex))
#             painter.drawEllipse(3, 3, 14, 14)  # dibujar círculo
#             painter.end()

#             icon = QIcon(pixmap)
#             self.color_menu.addItem(icon, color_name)
#         self.color_menu.currentTextChanged.connect(self.update_plot_preview)
#         layout.addWidget(self.color_menu)


#         # Plot labels
#         self.plot_labels = QLabel(
#             f"<span style='font-size:{text.text_normal}px;'><br> Labels </span>"
#         )
#         self.plot_labels.setWordWrap(True)
#         self.plot_labels.setAlignment(Qt.AlignmentFlag.AlignLeft)
#         layout.addWidget(self.plot_labels)

#         self.checkbox_title = QCheckBox("Set title")
#         self.checkbox_title.stateChanged.connect(self.toggle_title_input)
#         self.checkbox_title.stateChanged.connect(self.update_plot_settings)
#         layout.addWidget(self.checkbox_title)

#         self.sq_title = QLineEdit()
#         self.sq_title.setPlaceholderText("Type title name")
#         #self.sq_title.setFixedSize(button.nav_size[0], button.nav_size[1])
#         self.sq_title.setStyleSheet(button.file_input)
#         self.sq_title.textChanged.connect(self.update_plot_settings)
#         self.sq_title.hide()
#         layout.addWidget(self.sq_title)

#         # Crear checkbox con texto
#         self.checkbox_xlabel = QCheckBox("Set x label")
#         self.checkbox_xlabel.stateChanged.connect(self.toggle_xlabel_input)
#         self.checkbox_xlabel.stateChanged.connect(self.update_plot_settings)
#         layout.addWidget(self.checkbox_xlabel)

#         self.sq_xlabel = QLineEdit()
#         self.sq_xlabel.setPlaceholderText("Type x label name")
#         #self.sq_xlabel.setFixedSize(button.nav_size[0], button.nav_size[1])
#         self.sq_xlabel.setStyleSheet(button.file_input)
#         self.sq_xlabel.textChanged.connect(self.update_plot_settings)
#         self.sq_xlabel.hide()
#         layout.addWidget(self.sq_xlabel)

#         self.checkbox_ylabel = QCheckBox("Set y label")
#         self.checkbox_ylabel.stateChanged.connect(self.toggle_ylabel_input)
#         self.checkbox_ylabel.stateChanged.connect(self.update_plot_settings)
#         layout.addWidget(self.checkbox_ylabel)

#         self.sq_ylabel = QLineEdit()
#         self.sq_ylabel.setPlaceholderText("Type y label name")
#         self.sq_ylabel.setStyleSheet(button.file_input)
#         self.sq_ylabel.textChanged.connect(self.update_plot_settings)
#         self.sq_ylabel.hide()
#         layout.addWidget(self.sq_ylabel)

#         # Style options
#         self.style_section = QLabel(
#             f"<span style='font-size:{text.text_normal}px;'><br> Style </span>"
#         )
#         self.style_section.setWordWrap(True)
#         self.style_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
#         layout.addWidget(self.style_section)

#         self.checkbox_grid = QCheckBox("Show grid")
#         self.checkbox_grid.setChecked(False)
#         self.checkbox_grid.stateChanged.connect(self.update_plot_settings)
#         layout.addWidget(self.checkbox_grid)

#         self.checkbox_legend = QCheckBox("Show legend")
#         self.checkbox_legend.setChecked(False)
#         self.checkbox_legend.stateChanged.connect(self.update_plot_settings)
#         layout.addWidget(self.checkbox_legend)

#         self.sq_legend = QLineEdit()
#         self.sq_legend.setPlaceholderText("Type legend name")
#         #self.sq_legend.setFixedSize(button.nav_size[0], button.nav_size[1])
#         self.sq_legend.setStyleSheet(button.file_input)
#         self.sq_legend.textChanged.connect(self.update_plot_settings)
#         self.sq_legend.hide()
#         self.checkbox_legend.stateChanged.connect(self.toggle_legend_input)
#         layout.addWidget(self.sq_legend)

#         # Limit options
#         self.limit_section = QLabel(
#             f"<span style='font-size:{text.text_normal}px;'><br> Limits </span>"
#         )
#         self.limit_section.setWordWrap(True)
#         self.limit_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
#         layout.addWidget(self.limit_section)

#         self.checkbox_change_limits = QCheckBox("Set limits")
#         self.checkbox_change_limits.setChecked(False)
#         self.checkbox_change_limits.stateChanged.connect(self.toggle_limits_inputs)
#         self.checkbox_change_limits.stateChanged.connect(self.update_plot_settings)
#         layout.addWidget(self.checkbox_change_limits)

#         self.label_xmin = QLabel(f"<span style='font-size:{text.text_normal}px;'> Set x min limit: </span>")
#         self.label_xmin.setWordWrap(True)
#         self.label_xmin.setAlignment(Qt.AlignmentFlag.AlignLeft)
#         self.label_xmin.hide()
#         layout.addWidget(self.label_xmin)

#         self.sq_xmin = QLineEdit()
#         self.sq_xmin.setPlaceholderText("Type x min limit")
#         self.sq_xmin.setStyleSheet(button.file_input)
#         self.sq_xmin.textChanged.connect(self.update_plot_settings)
#         self.sq_xmin.hide()
#         layout.addWidget(self.sq_xmin)

#         self.label_xmax = QLabel(f"<span style='font-size:{text.text_normal}px;'> Set x max limit: </span>")
#         self.label_xmax.setWordWrap(True)
#         self.label_xmax.setAlignment(Qt.AlignmentFlag.AlignLeft)
#         self.label_xmax.hide()
#         layout.addWidget(self.label_xmax)

#         self.sq_xmax = QLineEdit()
#         self.sq_xmax.setPlaceholderText("Type x max limit")
#         self.sq_xmax.setStyleSheet(button.file_input)
#         self.sq_xmax.textChanged.connect(self.update_plot_settings)
#         self.sq_xmax.hide()
#         layout.addWidget(self.sq_xmax)

#         self.label_ymin = QLabel(f"<span style='font-size:{text.text_normal}px;'> Set y min limit: </span>")
#         self.label_ymin.setWordWrap(True)
#         self.label_ymin.setAlignment(Qt.AlignmentFlag.AlignLeft)
#         self.label_ymin.hide()
#         layout.addWidget(self.label_ymin)

#         self.sq_ymin = QLineEdit()
#         self.sq_ymin.setPlaceholderText("Type y min limit")
#         self.sq_ymin.setStyleSheet(button.file_input)
#         self.sq_ymin.textChanged.connect(self.update_plot_settings)
#         self.sq_ymin.hide()
#         layout.addWidget(self.sq_ymin)

#         self.label_ymax = QLabel(f"<span style='font-size:{text.text_normal}px;'> Set y max limit: </span>")
#         self.label_ymax.setWordWrap(True)
#         self.label_ymax.setAlignment(Qt.AlignmentFlag.AlignLeft)
#         self.label_ymax.hide()
#         layout.addWidget(self.label_ymax)

#         self.sq_ymax = QLineEdit()
#         self.sq_ymax.setPlaceholderText("Type y max limit")
#         self.sq_ymax.setStyleSheet(button.file_input)
#         self.sq_ymax.textChanged.connect(self.update_plot_settings)
#         self.sq_ymax.hide()
#         layout.addWidget(self.sq_ymax)
        
#         # Navigation buttons
#         self.btn_back = QPushButton("Back")
#         self.btn_back.clicked.connect(parent.previous_section)
#         self.btn_back.setStyleSheet(button.back)
        
#         self.btn_next = QPushButton("Next")
#         self.btn_next.clicked.connect(parent.next_section)
#         #self.btn_next.setFixedSize(button.nav_size[0], button.nav_size[1])
#         self.btn_next.setStyleSheet(button.next)

#         layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
#         layout.addWidget(self.btn_next)
#         layout.addWidget(self.btn_back)

#         # Configurar el área de scroll
#         scroll_area.setWidget(content_widget)

#         # Layout principal de la sección
#         main_layout = QVBoxLayout(self)
#         main_layout.addWidget(scroll_area)
#         self.setLayout(main_layout)

#         # Estado persistente
#         self.plot_settings = {
#             "title": "",
#             "xlabel": "",
#             "ylabel": "",
#             "grid": False,
#             "legend": False,
#             "legend_text": "",
#             "xlim": None,
#             "ylim": None,
#             "color": None
#         }

#         self.color_menu.currentTextChanged.connect(self.on_color_changed)

#     def on_color_changed(self, color_name):
#         color_hex = mcolors.TABLEAU_COLORS[f'tab:{color_name}']
#         self.plot_settings["color"] = color_hex
#         self.update_plot_preview(self.plot_option.currentText())
    
#     #----------------------------------------

#     def toggle_title_input(self, state):
#         """Show or hide the title input based on the checkbox state."""
#         if state == 2:
#             self.sq_title.show()
#         else:
#             self.sq_title.hide()

#     def toggle_xlabel_input(self, state):
#         """Show or hide the x label input based on the checkbox state."""
#         if state == 2:
#             self.sq_xlabel.show()
#         else:
#             self.sq_xlabel.hide()

#     def toggle_ylabel_input(self, state):
#         """Show or hide the y label input based on the checkbox state."""
#         if state == 2:
#             self.sq_ylabel.show()
#         else:
#             self.sq_ylabel.hide()
    
#     def toggle_legend_input(self, state):
#         """Show or hide the legend input based on the checkbox state."""
#         if state == 2:
#             self.sq_legend.show()
#         else:
#             self.sq_legend.hide()

#     def toggle_limits_inputs(self, state):
#         enabled = state == 2  # 2 es Checked
#         self.sq_xmin.setEnabled(enabled)
#         self.sq_xmax.setEnabled(enabled)
#         self.sq_ymin.setEnabled(enabled)
#         self.sq_ymax.setEnabled(enabled)
#         # Mostrar u ocultar los text boxes según el estado del checkbox
#         if enabled:
#             self.sq_xmin.show()
#             self.label_xmin.show()
#             self.sq_xmax.show()
#             self.label_xmax.show()
#             self.sq_ymin.show()
#             self.label_ymin.show()
#             self.sq_ymax.show()
#             self.label_ymax.show()
#         else:
#             self.sq_xmin.hide()
#             self.label_xmin.hide()
#             self.sq_xmax.hide()
#             self.label_xmax.hide()
#             self.sq_ymin.hide()
#             self.label_ymin.hide()
#             self.sq_ymax.hide()
#             self.label_ymax.hide()

#         #----------------------------------------

#     def update_plot_preview(self, plot_type):
#         # Get selected columns from the Load File section
#         x_column = self.parent.page_load.combo_select1.currentText()
#         y_column = self.parent.page_load.combo_select2.currentText()
#         z_column = self.parent.page_load.combo_select3.currentText()

#         df = self.parent.loaded_dataframe

#         if df is None or x_column not in df.columns or y_column not in df.columns:
#             self.parent.update_content_text("Please select valid columns and load a dataset.")
#             return

#         x_data = df[x_column]
#         y_data = df[y_column]
#         z_data = df[z_column] if z_column != "None" else None

#         # Obtener el color seleccionado
#         selected_color = self.color_menu.currentText()
#         color_dict = mcolors.TABLEAU_COLORS
#         color_hex = color_dict[f'tab:{selected_color}']

#         # Una sola llamada con todos los parámetros
#         self.parent.update_content_plot(
#             plot_type,
#             x_data,
#             y_data,
#             z_data,
#             self.plot_settings["xlim"],
#             self.plot_settings["ylim"],
#             self.plot_settings["legend"],
#             self.plot_settings["title"],
#             self.plot_settings["xlabel"],
#             self.plot_settings["ylabel"],
#             self.plot_settings["grid"],
#             self.plot_settings["legend_text"],
#             color_hex
#         )
        
#     def update_plot_settings(self):
#         """Send updated plot settings to ContentSection."""
#         # Update title based on checkbox and text
#         self.plot_settings["title"] = self.sq_title.text() if self.checkbox_title.isChecked() else ""
        
#         # Update x and y labels based on checkboxes and text
#         self.plot_settings["xlabel"] = self.sq_xlabel.text() if self.checkbox_xlabel.isChecked() else ""
#         self.plot_settings["ylabel"] = self.sq_ylabel.text() if self.checkbox_ylabel.isChecked() else ""
        
#         # Update grid and legend settings
#         self.plot_settings["grid"] = self.checkbox_grid.isChecked()
#         self.plot_settings["legend"] = self.checkbox_legend.isChecked()
#         self.plot_settings["legend_text"] = self.sq_legend.text() if self.checkbox_legend.isChecked() else ""

#         # Handle limits
#         xmin = self.sq_xmin.text().strip()
#         xmax = self.sq_xmax.text().strip()
#         ymin = self.sq_ymin.text().strip()
#         ymax = self.sq_ymax.text().strip()

#         if self.checkbox_change_limits.isChecked() and xmin and xmax:
#             try:
#                 self.plot_settings["xlim"] = (float(xmin), float(xmax))
#             except ValueError:
#                 self.plot_settings["xlim"] = None
#         else:
#             self.plot_settings["xlim"] = None

#         if self.checkbox_change_limits.isChecked() and ymin and ymax:
#             try:
#                 self.plot_settings["ylim"] = (float(ymin), float(ymax))
#             except ValueError:
#                 self.plot_settings["ylim"] = None
#         else:
#             self.plot_settings["ylim"] = None

#         # Obtener el color seleccionado
#         selected_color = self.color_menu.currentText()
#         color_dict = mcolors.TABLEAU_COLORS
#         color_hex = color_dict[f'tab:{selected_color}']
        
#         # Update the plot with all settings
#         self.update_plot_preview(self.plot_option.currentText())


#     def restore_plot_settings(self):
#         self.checkbox_title.setChecked(bool(self.plot_settings["title"]))
#         self.sq_title.setText(self.plot_settings["title"])
#         self.checkbox_xlabel.setChecked(bool(self.plot_settings["xlabel"]))
#         self.sq_xlabel.setText(self.plot_settings["xlabel"])
#         self.checkbox_ylabel.setChecked(bool(self.plot_settings["ylabel"]))
#         self.sq_ylabel.setText(self.plot_settings["ylabel"])
#         self.checkbox_grid.setChecked(self.plot_settings["grid"])
#         self.checkbox_legend.setChecked(self.plot_settings["legend"])
#         self.sq_legend.setText(self.plot_settings["legend_text"])
#         self.sq_xmin.setText(str(self.plot_settings["xlim"][0]) if self.plot_settings["xlim"] else "")
#         self.sq_xmax.setText(str(self.plot_settings["xlim"][1]) if self.plot_settings["xlim"] else "")
#         self.sq_ymin.setText(str(self.plot_settings["ylim"][0]) if self.plot_settings["ylim"] else "")
#         self.sq_ymax.setText(str(self.plot_settings["ylim"][1]) if self.plot_settings["ylim"] else "")
#         self.checkbox_change_limits.setChecked(bool(self.plot_settings["xlim"]) or bool(self.plot_settings["ylim"]))
#         self.sq_xmin.setEnabled(self.checkbox_change_limits.isChecked())
#         self.sq_xmax.setEnabled(self.checkbox_change_limits.isChecked())
#         self.sq_ymin.setEnabled(self.checkbox_change_limits.isChecked())
#         self.sq_ymax.setEnabled(self.checkbox_change_limits.isChecked())

#         # <-- Añade esta línea para actualizar la figura
#         self.update_plot_settings()

# class ExportSection(QWidget):
#     def __init__(self, parent):
#         super().__init__()
#         layout = QVBoxLayout(self)
#         layout.addWidget(QLabel("Export Section"))
        
#         self.btn_back = QPushButton("Back")
#         self.btn_back.clicked.connect(parent.previous_section)
#         #self.btn_back.setFixedSize(button.nav_size[0], button.nav_size[1])
#         self.btn_back.setStyleSheet(button.back)
        
#         layout.addWidget(self.btn_back)
#         self.setLayout(layout)