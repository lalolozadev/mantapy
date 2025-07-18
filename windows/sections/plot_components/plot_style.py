from PyQt6.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton, QHBoxLayout
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

        # Layout horizontal para los botones
        button_layout = QHBoxLayout()

        # Botón: Show grid
        self.button_grid = QPushButton("Show grid")
        self.button_grid.setCheckable(True)
        self.button_grid.setChecked(False)
        self.button_grid.setFont(text.qfont_small)
        button_layout.addWidget(self.button_grid)

        # Botón: Show legend
        self.button_legend = QPushButton("Show legend")
        self.button_legend.setCheckable(True)
        self.button_legend.setChecked(False)
        self.button_legend.setFont(text.qfont_small)
        button_layout.addWidget(self.button_legend)

        layout.addLayout(button_layout)

        self.sq_legend = QLineEdit()
        self.sq_legend.setPlaceholderText("Type legend name")
        self.sq_legend.setStyleSheet(button.file_input)
        self.sq_legend.hide()
        layout.addWidget(self.sq_legend)

    def notify_change(self):
        """Use plot_section reference to update settings"""
        if self.plot_section:
            self.plot_section.update_plot_settings()

    def connect_signals(self):
        """Connect all signals to notify change and toggle legend input"""
        self.button_grid.toggled.connect(self.notify_change)
        self.button_legend.toggled.connect(self.toggle_legend_input)
        self.button_legend.toggled.connect(self.notify_change)
        self.sq_legend.textChanged.connect(self.notify_change)

    def toggle_legend_input(self, checked):
        """Show/hide the legend input based on button state"""
        self.sq_legend.setVisible(checked)
    
    def get_style_settings(self):
        """Return the current style settings"""
        return {
            "grid": self.button_grid.isChecked(),
            "legend": self.button_legend.isChecked(),
            "legend_text": self.sq_legend.text() if self.button_legend.isChecked() else ""
        }

    def restore_settings(self, settings):
        """Restore style settings from a dictionary"""
        self.button_grid.setChecked(settings.get("grid", False))
        self.button_legend.setChecked(settings.get("legend", False))
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