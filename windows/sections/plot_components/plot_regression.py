from PyQt6.QtWidgets import QLabel, QCheckBox, QLineEdit, QComboBox
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

        # Enable regression checkbox
        self.checkbox_enable_regression = QCheckBox("Enable Regression")
        self.checkbox_enable_regression.setFont(text.qfont_small)
        self.checkbox_enable_regression.setChecked(False)
        layout.addWidget(self.checkbox_enable_regression)

        # # Regression type input
        # self.sq_regression_type = QLineEdit()
        # self.sq_regression_type.setPlaceholderText("Regression Type (e.g., linear, polynomial)")
        # self.sq_regression_type.setStyleSheet(button.file_input)
        # self.sq_regression_type.hide()
        # layout.addWidget(self.sq_regression_type)

        # Regression type menu
        self.sq_regression_type = QComboBox()
        self.sq_regression_type.addItems(['linear', 'poly2', 'poly3'])
        self.sq_regression_type.setFont(text.qfont_small)
        self.sq_regression_type.hide()
        layout.addWidget(self.sq_regression_type)

    def connect_signals(self):
        # Mostrar/ocultar input
        self.checkbox_enable_regression.stateChanged.connect(self.toggle_regression_inputs)
        # Notificar cambio de regresión
        self.checkbox_enable_regression.stateChanged.connect(self.notify_change)
        self.sq_regression_type.currentTextChanged.connect(self.notify_change)
    
    def notify_change(self):
        if self.plot_section:
            self.plot_section.update_plot_preview(self.plot_section.plot_option.currentText())
    def toggle_regression_inputs(self):
        is_checked = self.checkbox_enable_regression.isChecked()
        self.sq_regression_type.setVisible(is_checked)
        self.plot_section.regression_type = self.sq_regression_type.currentText()