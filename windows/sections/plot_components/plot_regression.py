from PyQt6.QtWidgets import QLabel, QCheckBox, QLineEdit, QComboBox, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
import config.text as text
import config.button as button

class PlotRegressionComponent:
    def __init__(self, plot_section, layout):
        self.plot_section = plot_section
        self.layout = layout
        self.setup_regression_widgets()
        self.connect_signals()

    def setup_regression_widgets(self):
        layout = self.layout

        # Regression section title
        self.regression_section = QLabel(
            f"<span style='font-size:{text.text_normal}px;'><br> Regression </span>"
        )
        self.regression_section.setWordWrap(True)
        self.regression_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.regression_section)

        # # Enable regression checkbox
        # self.checkbox_enable_regression = QCheckBox("Enable Regression")
        # self.checkbox_enable_regression.setFont(text.qfont_small)
        # self.checkbox_enable_regression.setChecked(False)
        # layout.addWidget(self.checkbox_enable_regression)

        # Botón toggle para activar regresión
        self.button_enable_regression = QPushButton("Enable Regression")
        self.button_enable_regression.setCheckable(True)
        self.button_enable_regression.setChecked(False)
        self.button_enable_regression.setFont(text.qfont_small)
        layout.addWidget(self.button_enable_regression)


        # Regression type menu
        self.sq_regression_type = QComboBox()
        self.sq_regression_type.addItems(['linear', 'poly2', 'poly3'])
        self.sq_regression_type.setFont(text.qfont_small)
        self.sq_regression_type.hide()
        layout.addWidget(self.sq_regression_type)

    def connect_signals(self):
        # Mostrar/ocultar menú de tipo de regresión
        self.button_enable_regression.toggled.connect(self.toggle_regression_inputs)
        self.button_enable_regression.toggled.connect(self.notify_change)
        self.sq_regression_type.currentTextChanged.connect(self.notify_change)

    def notify_change(self):
        if self.plot_section:
            self.plot_section.update_plot_preview(self.plot_section.plot_option.currentText())

    def toggle_regression_inputs(self, checked):
        self.sq_regression_type.setVisible(checked)

    def get_regression_settings(self):
        """Devuelve el estado actual de la regresión"""
        return {
            "enable_regression": self.button_enable_regression.isChecked(),
            "regression_type": self.sq_regression_type.currentText() if self.button_enable_regression.isChecked() else ""
        }

    def restore_settings(self, settings):
        """Restaura el estado de la regresión desde un diccionario"""
        self.button_enable_regression.setChecked(settings.get("enable_regression", False))
        if settings.get("enable_regression"):
            idx = self.sq_regression_type.findText(settings.get("regression_type", "linear"))
            if idx >= 0:
                self.sq_regression_type.setCurrentIndex(idx)

    # def connect_signals(self):
    #     # Mostrar/ocultar input
    #     self.checkbox_enable_regression.stateChanged.connect(self.toggle_regression_inputs)
    #     # Notificar cambio de regresión
    #     self.checkbox_enable_regression.stateChanged.connect(self.notify_change)
    #     self.sq_regression_type.currentTextChanged.connect(self.notify_change)
    
    # def notify_change(self):
    #     if self.plot_section:
    #         self.plot_section.update_plot_preview(self.plot_section.plot_option.currentText())
    # def toggle_regression_inputs(self):
    #     is_checked = self.checkbox_enable_regression.isChecked()
    #     self.sq_regression_type.setVisible(is_checked)
    #     self.plot_section.regression_type = self.sq_regression_type.currentText()