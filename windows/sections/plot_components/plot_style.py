from PyQt6.QtWidgets import QLabel, QCheckBox, QLineEdit
from PyQt6.QtCore import Qt
import config.text as text
import config.button as button

class PlotStyleComponent:
    def __init__(self, plot_section, layout):
        self.plot_section = plot_section
        self.layout = layout
        self.setup_style_widgets()
        self.connect_signals()

    def setup_style_widgets(self):
        layout = self.layout

        # Style section title
        self.style_section = QLabel(
            f"<span style='font-size:{text.text_normal}px;'><br> Style </span>"
        )
        self.style_section.setWordWrap(True)
        self.style_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.style_section)

        # Grid checkbox
        self.checkbox_grid = QCheckBox("Show grid")
        self.checkbox_grid.setChecked(False)
        self.checkbox_grid.setFont(text.qfont_small)
        layout.addWidget(self.checkbox_grid)

        # Legend checkbox and input
        self.checkbox_legend = QCheckBox("Show legend")
        self.checkbox_legend.setChecked(False)
        self.checkbox_legend.setFont(text.qfont_small)
        layout.addWidget(self.checkbox_legend)

        self.sq_legend = QLineEdit()
        self.sq_legend.setPlaceholderText("Type legend name")
        self.sq_legend.setStyleSheet(button.file_input)
        self.sq_legend.hide()
        layout.addWidget(self.sq_legend)

    def notify_change(self):
        """Use plot_section reference to update settings"""
        if self.plot_section:
            self.plot_section.update_plot_settings()

    def toggle_legend_input(self, state):
        """Show/hide the legend input based on checkbox state"""
        self.sq_legend.setVisible(state == Qt.CheckState.Checked.value)

    def get_style_settings(self):
        """Return the current style settings"""
        return {
            "grid": self.checkbox_grid.isChecked(),
            "legend": self.checkbox_legend.isChecked(),
            "legend_text": self.sq_legend.text() if self.checkbox_legend.isChecked() else ""
        }

    def restore_settings(self, settings):
        """Restore style settings from a dictionary"""
        self.checkbox_grid.setChecked(settings.get("grid", False))
        self.checkbox_legend.setChecked(settings.get("legend", False))
        if settings.get("legend"):
            self.sq_legend.setText(settings.get("legend_text", ""))

    def find_plot_section(self, widget):
        """Find the PlotSection instance in the widget hierarchy"""
        current = widget
        while current is not None:
            if hasattr(current, 'update_plot_settings'):
                return current
            current = current.parent()
        return None
    
    def connect_signals(self):
        """Connect all signals to notify change"""
        self.checkbox_grid.stateChanged.connect(self.notify_change)
        self.checkbox_legend.stateChanged.connect(self.notify_change)
        self.sq_legend.textChanged.connect(self.notify_change)
        
        # Toggle visibilidad de la leyenda
        self.checkbox_legend.stateChanged.connect(
            lambda state: self.sq_legend.setVisible(state == Qt.CheckState.Checked.value)
        )