from PyQt6.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
import config.text as text
import config.button as button

class PlotLimitsComponent:
    def __init__(self, plot_section, layout):
        self.plot_section = plot_section
        self.layout = layout
        self.setup_limit_widgets()
        self.connect_signals()

    def setup_limit_widgets(self):
        layout = self.layout

        # Limits section title
        self.limits_section = QLabel(
            f"<span style='font-size:{text.text_normal}px;'><br> Limits </span>"
        )
        self.limits_section.setWordWrap(True)
        self.limits_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.limits_section)

        # Layout horizontal para los botones
        button_layout = QHBoxLayout()

        # Botón: Change X limits
        self.button_xlimits = QPushButton("Change X limits")
        self.button_xlimits.setCheckable(True)
        self.button_xlimits.setChecked(False)
        self.button_xlimits.setFont(text.qfont_small)
        self.button_xlimits.setStyleSheet(button.plot_settings)
        button_layout.addWidget(self.button_xlimits)

        # Botón: Change Y limits
        self.button_ylimits = QPushButton("Change Y limits")
        self.button_ylimits.setCheckable(True)
        self.button_ylimits.setChecked(False)
        self.button_ylimits.setFont(text.qfont_small)
        self.button_ylimits.setStyleSheet(button.plot_settings)
        button_layout.addWidget(self.button_ylimits)

        layout.addLayout(button_layout)

        self.sq_xmin = QLineEdit()
        self.sq_xmin.setPlaceholderText("X min")
        self.sq_xmin.setStyleSheet(button.file_input)
        self.sq_xmin.hide()
        layout.addWidget(self.sq_xmin)

        self.sq_xmax = QLineEdit()
        self.sq_xmax.setPlaceholderText("X max")
        self.sq_xmax.setStyleSheet(button.file_input)
        self.sq_xmax.hide()
        layout.addWidget(self.sq_xmax)

        self.sq_ymin = QLineEdit()
        self.sq_ymin.setPlaceholderText("Y min")
        self.sq_ymin.setStyleSheet(button.file_input)
        self.sq_ymin.hide()
        layout.addWidget(self.sq_ymin)

        self.sq_ymax = QLineEdit()
        self.sq_ymax.setPlaceholderText("Y max")
        self.sq_ymax.setStyleSheet(button.file_input)
        self.sq_ymax.hide()
        layout.addWidget(self.sq_ymax)

    def notify_change(self):
        if self.plot_section:
            self.plot_section.update_plot_settings()

    def connect_signals(self):
        # X limits
        self.button_xlimits.toggled.connect(self.toggle_xlimit_inputs)
        self.button_xlimits.toggled.connect(self.notify_change)
        self.sq_xmin.textChanged.connect(self.notify_change)
        self.sq_xmax.textChanged.connect(self.notify_change)
        # Y limits
        self.button_ylimits.toggled.connect(self.toggle_ylimit_inputs)
        self.button_ylimits.toggled.connect(self.notify_change)
        self.sq_ymin.textChanged.connect(self.notify_change)
        self.sq_ymax.textChanged.connect(self.notify_change)

    def toggle_xlimit_inputs(self, checked):
        self.sq_xmin.setVisible(checked)
        self.sq_xmax.setVisible(checked)

    def toggle_ylimit_inputs(self, checked):
        self.sq_ymin.setVisible(checked)
        self.sq_ymax.setVisible(checked)

    def get_limit_settings(self):
        """Return the current limit settings"""
        xlim = None
        ylim = None

        if self.button_xlimits.isChecked():
            try:
                xlim = (float(self.sq_xmin.text()), float(self.sq_xmax.text()))
            except ValueError:
                xlim = None

        if self.button_ylimits.isChecked():
            try:
                ylim = (float(self.sq_ymin.text()), float(self.sq_ymax.text()))
            except ValueError:
                ylim = None

        return {"xlim": xlim, "ylim": ylim}

    def restore_settings(self, settings):
        if settings.get("xlim"):
            self.button_xlimits.setChecked(True)
            xlim = settings["xlim"]
            self.sq_xmin.setText(str(xlim[0]))
            self.sq_xmax.setText(str(xlim[1]))
        if settings.get("ylim"):
            self.button_ylimits.setChecked(True)
            ylim = settings["ylim"]
            self.sq_ymin.setText(str(ylim[0]))
            self.sq_ymax.setText(str(ylim[1]))