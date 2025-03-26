from PyQt6.QtWidgets import QFrame, QVBoxLayout, QScrollArea, QWidget, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import config.text as text

# class ContentSection(QFrame):
#     def __init__(self, text):
#         super().__init__()
#         self.init_ui(text)

#     def init_ui(self, text):
#         layout = QVBoxLayout(self)
#         layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         # Create scroll area
#         self.scroll_area = QScrollArea()
#         self.scroll_area.setWidgetResizable(True)
#         self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

#         # Create container widget for the label
#         container = QWidget()
#         container_layout = QVBoxLayout(container)

#         self.label = QLabel(
#             f"<span style='font-size:{text.text_title}px;'><b> Welcome to Mantapy </b></span><br>"
#             f"<span style='font-size:{text.text_normal}px;'>An open-source project for oceanographic data analysis and more.</span><br>"
#             f"<span style='font-size:{text.text_normal}px;'>Created by: <i>Eduardo Loza</i></span><br><br>"
#             f"<span style='font-size:{text.text_normal}px;'><b> License</b><br>"
#             f"<span style='font-size:{text.text_small}px;'>GNU GENERAL PUBLIC LICENSE<br>"
#             f"<span style='font-size:{text.text_small}px;'>Version 3, 29 June 2007<br>"
#             f"<span style='font-size:{text.text_small}px;'>Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/></span><br>"
#         )
#         self.label.setWordWrap(True)
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
#         container_layout.addWidget(self.label)
#         self.scroll_area.setWidget(container)
#         layout.addWidget(self.scroll_area)
#         self.setLayout(layout)
    
#     def setText(self, text):
#         """Cambia el texto mostrado en la sección de contenido."""
#         self.label.setText(f"<span style='font-size:18px; color:#333;'>{text}</span>")

#     def update_content_text(self, text, as_notebook=False):
#         """Actualiza el texto mostrado en la sección de contenido."""
#         if as_notebook:
#             self.label.setText(text)
#         else:
#             self.label.setText(f"<span style='font-size:18px; color:#333;'>{text}</span>")

class ContentSection(QFrame):
    def __init__(self, text):
        super().__init__()
        self.init_ui(text)

    def init_ui(self, text):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Crear área de scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Contenedor de contenido (puede ser texto o tabla)
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)

        # Label para mostrar texto
        self.label = QLabel(
            f"<span style='font-size:{text.text_title}px;'><b> Welcome to Mantapy </b></span><br>"
            f"<span style='font-size:{text.text_normal}px;'>An open-source project for oceanographic data analysis and more.</span><br>"
            f"<span style='font-size:{text.text_normal}px;'>Created by: <i>Eduardo Loza</i></span><br><br>"
            f"<span style='font-size:{text.text_normal}px;'><b> License</b><br>"
            f"<span style='font-size:{text.text_small}px;'>GNU GENERAL PUBLIC LICENSE<br>"
            f"<span style='font-size:{text.text_small}px;'>Version 3, 29 June 2007<br>"
            f"<span style='font-size:{text.text_small}px;'>Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/></span><br>"
        )
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Agregar el label por defecto
        self.container_layout.addWidget(self.label)
        self.scroll_area.setWidget(self.container)
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

    def setText(self, text):
        """Cambia el texto mostrado en la sección de contenido."""
        self.label.setText(f"<span style='font-size:18px; color:#333;'>{text}</span>")

    def update_content_text(self, text):
        """Actualiza el texto y elimina cualquier tabla anterior."""
        if hasattr(self, "tableWidget"):
            self.container_layout.removeWidget(self.tableWidget)
            self.tableWidget.deleteLater()
            del self.tableWidget

        self.label.setText(f"<span style='font-size:18px; color:#333;'>{text}</span>")
        self.label.show()

    def update_content_table(self, df):
        """Muestra un DataFrame en un QTableWidget dentro del área de contenido."""
        if hasattr(self, "tableWidget"):
            self.container_layout.removeWidget(self.tableWidget)
            self.tableWidget.deleteLater()

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])
        self.tableWidget.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[row, col]))
                self.tableWidget.setItem(row, col, item)

        self.container_layout.addWidget(self.tableWidget)
        self.label.hide()  # Oculta el texto cuando se muestra la tabla
