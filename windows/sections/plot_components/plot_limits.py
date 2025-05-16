from PyQt6.QtWidgets import QLabel, QCheckBox, QLineEdit
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

        # X limits checkbox and inputs
        self.checkbox_change_xlimits = QCheckBox("Change X limits")
        self.checkbox_change_xlimits.setFont(text.qfont_small)
        self.checkbox_change_xlimits.setChecked(False)
        layout.addWidget(self.checkbox_change_xlimits)

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

        # Y limits checkbox and inputs
        self.checkbox_change_ylimits = QCheckBox("Change Y limits")
        self.checkbox_change_ylimits.setFont(text.qfont_small)
        self.checkbox_change_ylimits.setChecked(False)
        layout.addWidget(self.checkbox_change_ylimits)

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

    def toggle_xlimit_inputs(self, state):
        is_visible = state == Qt.CheckState.Checked.value
        self.sq_xmin.setVisible(is_visible)
        self.sq_xmax.setVisible(is_visible)

    def toggle_ylimit_inputs(self, state):
        is_visible = state == Qt.CheckState.Checked.value
        self.sq_ymin.setVisible(is_visible)
        self.sq_ymax.setVisible(is_visible)

    def get_limit_settings(self):
        """Return the current limit settings"""
        xlim = None
        ylim = None

        if self.checkbox_change_xlimits.isChecked():
            try:
                xlim = (float(self.sq_xmin.text()), float(self.sq_xmax.text()))
            except ValueError:
                xlim = None

        if self.checkbox_change_ylimits.isChecked():
            try:
                ylim = (float(self.sq_ymin.text()), float(self.sq_ymax.text()))
            except ValueError:
                ylim = None

        return {"xlim": xlim, "ylim": ylim}

    def restore_settings(self, settings):
        if settings.get("xlim"):
            self.checkbox_change_xlimits.setChecked(True)
            xlim = settings["xlim"]
            self.sq_xmin.setText(str(xlim[0]))
            self.sq_xmax.setText(str(xlim[1]))
        if settings.get("ylim"):
            self.checkbox_change_ylimits.setChecked(True)
            ylim = settings["ylim"]
            self.sq_ymin.setText(str(ylim[0]))
            self.sq_ymax.setText(str(ylim[1]))

    def connect_signals(self):
        # X limits
        self.checkbox_change_xlimits.stateChanged.connect(self.notify_change)
        self.checkbox_change_xlimits.stateChanged.connect(self.toggle_xlimit_inputs)
        self.sq_xmin.textChanged.connect(self.notify_change)
        self.sq_xmax.textChanged.connect(self.notify_change)
        # Y limits
        self.checkbox_change_ylimits.stateChanged.connect(self.notify_change)
        self.checkbox_change_ylimits.stateChanged.connect(self.toggle_ylimit_inputs)
        self.sq_ymin.textChanged.connect(self.notify_change)
        self.sq_ymax.textChanged.connect(self.notify_change)