import webbrowser
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from .workspace import MantapyUI
import config.text as text
import config.button as button
import config.window as window
from config.colors import *

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Welcome to Mantapy")
        self.setStyleSheet(f"background-color: {blanco1};")
        
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
            f"<span style='font-size:{text.text_title}px;'><b> Welcome to Mantapy </b></span><br>"
        )

        # Centrar el texto  
        self.label_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)   
        layout.addWidget(self.label_welcome)

        label = QLabel()
        pixmap = QPixmap("assets/logo_mantapy.ico")
        scaled_pixmap = pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar la imagen en el QLabel
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)  # Centrar el QLabel en el layout


        self.label_welcome = QLabel(
            f"<span style='font-size:{text.text_normal}px;'>An open-source project for quick and simple scientific data visualizations.</span><br>"
            f"<span style='font-size:{text.text_normal}px;'>Created by: <i>Eduardo Loza</i></span><br><br>"
            f"<span style='font-size:{text.text_normal}px;'><b> License</b><br>"
            f"<span style='font-size:{text.text_small}px;'>GNU GENERAL PUBLIC LICENSE<br>"
            f"<span style='font-size:{text.text_small}px;'>Version 3, 29 June 2007<br>"
            f"<span style='font-size:{text.text_small}px;'>Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/></span><br>"
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