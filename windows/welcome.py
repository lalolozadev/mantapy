import webbrowser
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from .workspace import MantapyUI
import config.text as text
import config.button as button
import config.window as window

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Welcome to Mantapy")
        
        # Obtener las dimensiones de la pantalla
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        
        # Calcular las coordenadas para centrar la ventana
        x = (rect.width() - window.small[2]) // 2
        y = (rect.height() - window.small[3]) // 2
        
        # Establecer la geometría de la ventana (centrada)
        self.setGeometry(x, y, window.small[2], window.small[3])
        
        layout = QVBoxLayout()
        
        self.label_welcome = QLabel(
            f"<font size='{text.text_title}'><b> Welcome to Mantapy </b></font><br>"
            f"<font size='{text.text_normal}'>An open-source project for oceanographic data analysis and more.</font><br>"
            f"<font size='{text.text_normal}'>Created by: <i>Eduardo Loza</i></font><br><br>"
            f"<font size='{text.text_normal}'><b> License</b><br>"
            f"<font size='{text.text_small}'>GNU GENERAL PUBLIC LICENSE<br>"
            f"<font size='{text.text_small}'>Version 3, 29 June 2007<br>"
            f"<font size='{text.text_small}'>Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/><br>"
        )

        # Centrar el texto  
        self.label_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)   
        layout.addWidget(self.label_welcome)

        # Layout horizontal para los botones
        button_layout = QHBoxLayout()
        # Añadir un padding entre los botones
        button_layout.setSpacing(button.padding) 
        
        self.btn_start = QPushButton("Start")
        # Cambiar el tamaño del botón
        self.btn_start.setFixedSize(button.ini_size[0], button.ini_size[1])  # Ancho 150px, Alto 50px
        # Aplicar un estilo con bordes redondeados
        self.btn_start.setStyleSheet(button.start)
        self.btn_start.clicked.connect(self.open_main_window)
        button_layout.addWidget(self.btn_start)
        
        self.btn_doc = QPushButton("Read Documentation")
        # Cambiar el tamaño del botón
        self.btn_doc.setFixedSize(button.ini_size[0], button.ini_size[1])  # Ancho 150px, Alto 50px
        # Aplicar un estilo con bordes redondeados
        self.btn_doc.setStyleSheet(button.doc)
        self.btn_doc.clicked.connect(self.open_documentation)
        button_layout.addWidget(self.btn_doc)
        
        # Centrar los botones en el layout horizontal
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Añadir los botones al layout principal
        layout.addLayout(button_layout)

        self.setLayout(layout)
    
    def open_main_window(self):
        self.main_window = MantapyUI()
        self.main_window.show()
        self.close()
    
    def open_documentation(self):
        webbrowser.open("https://github.com/lalolozadev/mantapy")