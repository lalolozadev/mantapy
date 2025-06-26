from PyQt6.QtWidgets import QFrame, QVBoxLayout, QScrollArea, QWidget, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objs as go
import plotly.io as pio
import tempfile
import os
import numpy as np
import config.text as text
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


class ContentSection(QFrame):
    def __init__(self, text):
        super().__init__()
        self.init_ui(text)

        self.last_ax = None  # Guarda el último Axes usado
        self.last_plot_type = None
        self.last_x_data = None
        self.last_y_data = None
        self.last_z_data = None

        self.plot_settings = {
            "title": "",
            "xlabel": "",
            "ylabel": "",
            "grid": False,
            "legend": False,
            "legend_text": "",
            "xlim": None,
            "ylim": None,
            "color": None  # Añadir color a las configuraciones
        }
    
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

    def update_content_plot(
        self,
        plot_type,
        x_data,
        y_data,
        z_data=None,
        xlim=None,
        ylim=None,
        legend=None,
        title=None,
        xlabel=None,
        ylabel=None,
        grid=None,
        legend_text=None,
        color = None,
        enable_regression=False,
        regression_type=None,
    ):
                # Reemplazar comas por nada, luego convertir a float
        x_data = np.array([float(str(x).replace(',', '')) for x in x_data])
        y_data = np.array([float(str(y).replace(',', '')) for y in y_data])

        # Eliminar vista previa anterior si existe
        if hasattr(self, "plot_view") and self.plot_view:
            self.container_layout.removeWidget(self.plot_view)
            self.plot_view.deleteLater()
            self.plot_view = None

        # Solo intenta borrar el archivo temporal si existe
        if hasattr(self, "temp_file") and self.temp_file and os.path.exists(self.temp_file.name):
            try:
                os.remove(self.temp_file.name)
            except Exception:
                pass

        # Crear la figura SIEMPRE
        fig = go.Figure()
        if plot_type == "Line":
            fig.add_trace(go.Scatter(
                x=x_data, 
                y=y_data, 
                mode="lines", 
                name=legend_text or "Line Plot",
                line=dict(color=color) if color else None  # Añadir color
            ))
        elif plot_type == "Scatter":
            fig.add_trace(go.Scatter(
                x=x_data, 
                y=y_data, 
                mode="markers", 
                name=legend_text or "Scatter Plot",
                marker=dict(color=color) if color else None  # Añadir color
            ))
        elif plot_type == "Bar":
            fig.add_trace(go.Bar(
                x=x_data, 
                y=y_data, 
                name=legend_text or "Bar Plot",
                marker_color=color  # Añadir color
            ))
        
        # ... después de crear fig y agregar los datos principales ...
        if enable_regression and regression_type:
            self.add_regression_to_plot(fig, x_data, y_data, regression_type)

        # Guardar el último estado
        self.last_plot_type = plot_type
        self.last_x_data = x_data
        self.last_y_data = y_data
        self.last_legend_text = legend_text
        self.last_color = color  # Guardar el último color

        # Update the layout settings to include all parameters
        fig.update_layout(
            margin=dict(l=40, r=40, t=40, b=40),
            showlegend=legend if legend is not None else True,
            title={"text": title or ""},
            xaxis={
                "title": {"text": xlabel or ""},
                "showgrid": grid if grid is not None else True,
                "range": xlim
            },
            yaxis={
                "title": {"text": ylabel or ""},
                "showgrid": grid if grid is not None else True,
                "range": ylim
            }
        )

        # Guardar gráfico en archivo temporal
        self.current_figure = fig
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        pio.write_html(fig, file=self.temp_file.name, auto_open=False)

        # Mostrar gráfico en QWebEngineView
        self.plot_view = QWebEngineView()
        self.plot_view.load(QUrl.fromLocalFile(self.temp_file.name))
        self.container_layout.addWidget(self.plot_view)
        self.label.hide()

        # Eliminar el archivo temporal después de cargarlo
        QTimer.singleShot(5000, lambda: os.remove(self.temp_file.name) if os.path.exists(self.temp_file.name) else None)

    #--------------------------------------------

    def update_plot_settings(
            self,
            title=None,
            xlabel=None,
            ylabel=None,
            grid=None,
            legend=None,
            legend_text=None,
            xlim=None,
            ylim=None,
            color=None,
            enable_regression=False,
            regression_type=None,
            ):
        """Update plot settings without reading from HTML."""
        if not hasattr(self, "plot_view"):
            return
                    
        # Actualizar settings almacenados
        if title is not None:
            self.plot_settings["title"] = title
        if xlabel is not None:
            self.plot_settings["xlabel"] = xlabel
        if ylabel is not None:
            self.plot_settings["ylabel"] = ylabel
        if grid is not None:
            self.plot_settings["grid"] = grid
        if legend is not None:
            self.plot_settings["legend"] = legend
        if legend_text is not None:
            self.plot_settings["legend_text"] = legend_text
        if xlim is not None:
            self.plot_settings["xlim"] = xlim
        if ylim is not None:
            self.plot_settings["ylim"] = ylim
        if color is not None:
            self.plot_settings["color"] = color
        
        # Create a new figure with current data
        fig = go.Figure()
        
        # Usar los settings almacenados para crear la figura
        if self.last_plot_type == "Line":
            fig.add_trace(go.Scatter(
                x=self.last_x_data, 
                y=self.last_y_data, 
                mode="lines", 
                name=self.plot_settings["legend_text"] or "Line Plot",
                line=dict(color=self.plot_settings["color"]) if self.plot_settings["color"] else None
            ))
        elif self.last_plot_type == "Scatter":
            fig.add_trace(go.Scatter(
                x=self.last_x_data, 
                y=self.last_y_data, 
                mode="markers", 
                name=self.plot_settings["legend_text"] or "Scatter Plot",
                marker=dict(color=self.plot_settings["color"]) if self.plot_settings["color"] else None
            ))
        elif self.last_plot_type == "Bar":
            fig.add_trace(go.Bar(
                x=self.last_x_data, 
                y=self.last_y_data, 
                name=self.plot_settings["legend_text"] or "Bar Plot",
                marker_color=self.plot_settings["color"]
            ))
        
        if enable_regression and regression_type:
            self.add_regression_to_plot(fig, self.last_x_data, self.last_y_data, regression_type)

        # Update layout with settings
        layout_updates = {
            "showlegend": self.plot_settings["legend"],
            "title": {"text": self.plot_settings["title"] or "", "font": {"size": text.text_normal or 16}},
            "xaxis": {
                "title": {"text": self.plot_settings["xlabel"] or "", "font": {"size": text.text_normal or 14}},
                "showgrid": self.plot_settings["grid"],
                "range": self.plot_settings["xlim"]
            },
            "yaxis": {
                "title": {"text": self.plot_settings["ylabel"] or "", "font": {"size": text.text_normal or 14}},
                "showgrid": self.plot_settings["grid"],
                "range": self.plot_settings["ylim"]
            },
            "margin": dict(l=40, r=40, t=40, b=40)
        }

        # Apply updates
        fig.update_layout(**layout_updates)

        # Save and show the updated figure
        if hasattr(self, "temp_file"):
            pio.write_html(fig, file=self.temp_file.name, auto_open=False)
            if self.plot_view:
                self.plot_view.reload()

    #--------------------------------------------

    def add_regression_to_plot(self, fig, x_data, y_data, regression_type):
        """
        Añade una curva de regresión al gráfico plotly.
        regression_type: 'linear', 'poly2', 'poly3'
        """
        x = np.array(x_data).reshape(-1, 1)
        y = np.array(y_data)

        if regression_type == "linear":
            model = LinearRegression()
            model.fit(x, y)
            y_pred = model.predict(x)
            fig.add_trace(go.Scatter(
                x=x_data, y=y_pred,
                mode="lines",
                name="Linear Regression",
                line=dict(dash="dash", color="red")
            ))
        elif regression_type in ["poly2", "poly3"]:
            degree = 2 if regression_type == "poly2" else 3
            poly = PolynomialFeatures(degree)
            x_poly = poly.fit_transform(x)
            model = LinearRegression()
            model.fit(x_poly, y)
            y_pred = model.predict(x_poly)
            fig.add_trace(go.Scatter(
                x=x_data, y=y_pred,
                mode="lines",
                name=f"Poly {degree} Regression",
                line=dict(dash="dot", color="green" if degree == 2 else "blue")
            ))