from PyQt6.QtWidgets import QFrame, QVBoxLayout, QScrollArea, QWidget, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import config.text as text

class ContentSection(QFrame):
    def __init__(self, text):
        super().__init__()
        self.init_ui(text)
    
    #--------------------------------------------

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

    #--------------------------------------------

    def update_content_text(self, text):
        if hasattr(self, "tableWidget"):
            self.container_layout.removeWidget(self.tableWidget)
            self.tableWidget.deleteLater()
            del self.tableWidget

        self.label.setText(f"<span style='font-size:18px; color:#333;'>{text}</span>")
        self.label.show()
    
    #--------------------------------------------

    def update_content_table(self, df):
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


    #--------------------------------------------

    def update_content_plot(self, plot_type, x_data, y_data, z_data=None):
        """Renders a plot in the content area based on the selected columns."""
        if hasattr(self, "canvas"):
            self.container_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            del self.canvas

        # Create a Matplotlib figure
        figure = Figure()
        ax = figure.add_subplot(111)

        # Generate the plot based on the selected type
        if plot_type == "Line":
            ax.plot(x_data, y_data, label="Line Plot")
        elif plot_type == "Scatter":
            ax.scatter(x_data, y_data, label="Scatter Plot")
        elif plot_type == "Bar":
            ax.bar(x_data, y_data, label="Bar Plot")

        # Configure the plot
        ax.set_title("Plot Preview")
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.legend()

        # Render the plot in a Matplotlib canvas
        self.canvas = FigureCanvas(figure)
        self.container_layout.addWidget(self.canvas)
        self.label.hide()  # Hide the default label when a plot is displayed