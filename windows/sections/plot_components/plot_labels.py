from PyQt6.QtWidgets import QLabel, QCheckBox, QLineEdit, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
import config.text as text
import config.button as button

class PlotLabelsComponent:
    def __init__(self, plot_section, layout):
        self.plot_section = plot_section
        self.layout = layout  # Guarda el layout recibido
        self.setup_label_widgets()
        self.connect_signals()

    def setup_label_widgets(self):
        layout = self.layout
        
        # Title Label
        self.label_section = QLabel(
            f"<span style='font-size:{text.text_normal}px;'><br> Labels </span>"
        )
        self.label_section.setWordWrap(True)
        self.label_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.label_section)

        # Crear un layout horizontal para los botones toggle
        button_layout = QHBoxLayout()

        # Botón: Show title
        self.button_title = QPushButton("Show title")
        self.button_title.setCheckable(True)
        self.button_title.setChecked(False)
        self.button_title.setFont(text.qfont_small)
        self.button_title.setStyleSheet(button.plot_settings)
        button_layout.addWidget(self.button_title)

        # Botón: Show X label
        self.button_xlabel = QPushButton("Show X label")
        self.button_xlabel.setCheckable(True)
        self.button_xlabel.setChecked(False)
        self.button_xlabel.setFont(text.qfont_small)
        self.button_xlabel.setStyleSheet(button.plot_settings)
        button_layout.addWidget(self.button_xlabel)

        # Botón: Show Y label
        self.button_ylabel = QPushButton("Show Y label")
        self.button_ylabel.setCheckable(True)
        self.button_ylabel.setChecked(False)
        self.button_ylabel.setFont(text.qfont_small)
        self.button_ylabel.setStyleSheet(button.plot_settings)
        button_layout.addWidget(self.button_ylabel)

        # Agregar el layout horizontal al layout principal
        layout.addLayout(button_layout)

        # # Title checkbox and input
        # self.checkbox_title = QCheckBox("Show title")
        # self.checkbox_title.setChecked(False)
        # self.checkbox_title.setFont(text.qfont_small)
        # layout.addWidget(self.checkbox_title)

        self.sq_title = QLineEdit()
        self.sq_title.setPlaceholderText("Type title")
        self.sq_title.setStyleSheet(button.file_input)
        self.sq_title.hide()
        layout.addWidget(self.sq_title)

        # # X Label checkbox and input
        # self.checkbox_xlabel = QCheckBox("Show X label")
        # self.checkbox_xlabel.setFont(text.qfont_small)
        # self.checkbox_xlabel.setChecked(False)
        # layout.addWidget(self.checkbox_xlabel)

        self.sq_xlabel = QLineEdit()
        self.sq_xlabel.setPlaceholderText("Type X label")
        self.sq_xlabel.setStyleSheet(button.file_input)
        self.sq_xlabel.hide()
        layout.addWidget(self.sq_xlabel)

        # # Y Label checkbox and input
        # self.checkbox_ylabel = QCheckBox("Show Y label")
        # self.checkbox_ylabel.setFont(text.qfont_small)
        # self.checkbox_ylabel.setChecked(False)
        # layout.addWidget(self.checkbox_ylabel)

        self.sq_ylabel = QLineEdit()
        self.sq_ylabel.setPlaceholderText("Type Y label")
        self.sq_ylabel.setStyleSheet(button.file_input)
        self.sq_ylabel.hide()
        layout.addWidget(self.sq_ylabel)

    def notify_change(self):
        """Use plot_section reference to update settings"""
        if self.plot_section:
            self.plot_section.update_plot_settings()

    def restore_settings(self, settings):
        """Restore label settings from a dictionary"""
        if settings.get("title"):
            self.button_title.setChecked(True)
            self.sq_title.setText(settings["title"])
        
        if settings.get("xlabel"):
            self.button_xlabel.setChecked(True)
            self.sq_xlabel.setText(settings["xlabel"])
        
        if settings.get("ylabel"):
            self.button_ylabel.setChecked(True)
            self.sq_ylabel.setText(settings["ylabel"])

    def find_plot_section(self, widget):
        """Find the PlotSection instance in the widget hierarchy"""
        current = widget
        while current is not None:
            if hasattr(current, 'update_plot_settings'):
                return current
            current = current.parent()
        return None
    
    # def connect_signals(self):
    #     """Connect all signals to notify_change and visibility toggles"""
    #     # Connect each checkbox to its specific handler
    #     self.checkbox_title.stateChanged.connect(lambda state: self.on_checkbox_changed(state, self.checkbox_title, self.sq_title))
    #     self.checkbox_xlabel.stateChanged.connect(lambda state: self.on_checkbox_changed(state, self.checkbox_xlabel, self.sq_xlabel))
    #     self.checkbox_ylabel.stateChanged.connect(lambda state: self.on_checkbox_changed(state, self.checkbox_ylabel, self.sq_ylabel))

    def connect_signals(self):
        """Connect all signals to notify_change and visibility toggles"""
        # Conectar los botones toggle para mostrar/ocultar los campos de texto
        self.button_title.toggled.connect(lambda checked: self.sq_title.setVisible(checked))
        self.button_title.toggled.connect(self.notify_change)
        self.button_xlabel.toggled.connect(lambda checked: self.sq_xlabel.setVisible(checked))
        self.button_xlabel.toggled.connect(self.notify_change)
        self.button_ylabel.toggled.connect(lambda checked: self.sq_ylabel.setVisible(checked))
        self.button_ylabel.toggled.connect(self.notify_change)

        # Connect each text input to its specific handler
        self.sq_title.textChanged.connect(lambda text: self.on_text_changed(text, self.sq_title, self.button_title))
        self.sq_xlabel.textChanged.connect(lambda text: self.on_text_changed(text, self.sq_xlabel, self.button_xlabel))
        self.sq_ylabel.textChanged.connect(lambda text: self.on_text_changed(text, self.sq_ylabel, self.button_ylabel))
        
    def on_checkbox_changed(self, state, checkbox, text_input):
        """Handle checkbox state changes"""
        # Update visibility
        text_input.setVisible(state == Qt.CheckState.Checked.value)
        # Notify changes
        self.notify_change()

    def on_text_changed(self, text, text_input, checkbox):
        """Handle text changes"""
        # Only notify if the corresponding checkbox is checked
        if checkbox.isChecked():
            self.notify_change()

    # def get_label_settings(self):
    #     """Return the current label settings"""
    #     return {
    #         "title": self.sq_title.text() if self.checkbox_title.isChecked() else "",
    #         "xlabel": self.sq_xlabel.text() if self.checkbox_xlabel.isChecked() else "",
    #         "ylabel": self.sq_ylabel.text() if self.checkbox_ylabel.isChecked() else ""
    #     }

    def get_label_settings(self):
        """Return the current label settings"""
        return {
            "title": self.sq_title.text() if self.button_title.isChecked() else "",
            "xlabel": self.sq_xlabel.text() if self.button_xlabel.isChecked() else "",
            "ylabel": self.sq_ylabel.text() if self.button_ylabel.isChecked() else ""
        }