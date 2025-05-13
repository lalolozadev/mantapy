from PyQt6.QtWidgets import QFrame, QVBoxLayout, QScrollArea, QWidget, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objs as go
import plotly.io as pio
import tempfile
import os
import numpy as np
import config.text as text
import matplotlib.colors as mcolors


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
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        pio.write_html(fig, file=self.temp_file.name, auto_open=False)

        # Mostrar gráfico en QWebEngineView
        self.plot_view = QWebEngineView()
        self.plot_view.load(QUrl.fromLocalFile(self.temp_file.name))
        self.container_layout.addWidget(self.plot_view)
        self.label.hide()

        # Eliminar el archivo temporal después de cargarlo
        QTimer.singleShot(5000, lambda: os.remove(self.temp_file.name) if os.path.exists(self.temp_file.name) else None)

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
            color=None
            ):
        
        """Update plot settings without reading from HTML."""
        if not hasattr(self, "plot_view"):
            return
                    
        # Create a new figure with current data
        fig = go.Figure()
        
        if self.last_plot_type == "Line":
            fig.add_trace(go.Scatter(
                x=self.last_x_data, 
                y=self.last_y_data, 
                mode="lines", 
                name=legend_text or self.last_legend_text or "Line Plot",
                line=dict(color=color) if color else None
            ))
        elif self.last_plot_type == "Scatter":
            fig.add_trace(go.Scatter(
                x=self.last_x_data, 
                y=self.last_y_data, 
                mode="markers", 
                name=legend_text or self.last_legend_text or "Scatter Plot",
                marker=dict(color=color) if color else None
            ))
        elif self.last_plot_type == "Bar":
            fig.add_trace(go.Bar(
                x=self.last_x_data, 
                y=self.last_y_data, 
                name=legend_text or self.last_legend_text or "Bar Plot",
                marker_color=color
            ))

        # Update layout with new settings
        layout_updates = {
            "showlegend": legend if legend is not None else True,
            "title": {"text": title or "", "font": {"size": text.text_normal or 16}},
            "xaxis": {
                "title": {"text": xlabel or "", "font": {"size": text.text_normal or 14}},
                "showgrid": grid if grid is not None else True,
                "range": xlim
            },
            "yaxis": {
                "title": {"text": ylabel or "", "font": {"size": text.text_normal or 14}},
                "showgrid": grid if grid is not None else True,
                "range": ylim
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


    # def update_content_plot(self, plot_type, x_data, y_data, z_data=None, xlim=None, ylim=None):
    #     """Renders a plot in the content area based on the selected columns."""
    #     if hasattr(self, "canvas"):
    #         self.container_layout.removeWidget(self.canvas)
    #         self.canvas.deleteLater()
    #         del self.canvas

    #     x_data = np.array(x_data)
    #     y_data = np.array(y_data)
    #     z_data = np.array(z_data) if z_data is not None else None

    #     # Create a Matplotlib figure
    #     figure = Figure()
    #     ax = figure.add_subplot(111)

    #     # Guarda el último ax y datos
    #     self.last_ax = ax
    #     self.last_plot_type = plot_type
    #     self.last_x_data = x_data
    #     self.last_y_data = y_data
    #     self.last_z_data = z_data

    #     # Generate the plot based on the selected type
    #     if plot_type == "Line":
    #         ax.plot(x_data, y_data, label="Line Plot")
    #     elif plot_type == "Scatter":
    #         ax.scatter(x_data, y_data, label="Scatter Plot")
    #     elif plot_type == "Bar":
    #         ax.bar(x_data, y_data, label="Bar Plot")
        
    #     ax.legend()

    #     # --- APLICAR LIMITES AQUÍ ---

    #     # # Limites X
    #     # if xlim:
    #     #     ax.set_xlim(xlim)
    #     # else:
    #     #     ax.relim()
    #     #     ax.autoscale_view(scalex=True, scaley=False)

    #     # # Limites Y
    #     # if ylim:
    #     #     ax.set_ylim(ylim)
    #     #     ax.set_autoscale_on(False)  # ← esto es necesario aquí
    #     # else:
    #     #     ax.relim()
    #     #     ax.autoscale_view(scalex=False, scaley=True)


    #     # Forzar límites manualmente
    #     if xlim:
    #         ax.set_xlim(xlim)
    #     if ylim:
    #         ax.set_ylim(ylim)




    #     #self.canvas.draw()

    #     # Render the plot in a Matplotlib canvas
    #     self.canvas = FigureCanvas(figure)
    #     self.container_layout.addWidget(self.canvas)
    #     self.label.hide()  # Hide the default label when a plot is displayed


    # def update_plot_settings(self, title, xlabel, ylabel, grid, legend, legend_text, xlim, ylim):
    #     """Update the plot settings based on user input."""
    #     if hasattr(self, "canvas") and self.last_ax is not None:
    #         ax = self.last_ax

    #         # Actualizar título y etiquetas
    #         ax.set_title(title if title else "")
    #         ax.set_xlabel(xlabel if xlabel else "")
    #         ax.set_ylabel(ylabel if ylabel else "")

    #         # Grid
    #         ax.grid(grid)

    #         # Leyenda
    #         if legend:
    #             if legend_text:
    #                 ax.legend([legend_text])
    #             else:
    #                 ax.legend()
    #         else:
    #             current_legend = ax.get_legend()
    #             if current_legend is not None:
    #                 current_legend.remove()

    #         self.canvas.draw()

    #         # Forzar límites manualmente
    #         if xlim:
    #             ax.set_xlim(xlim)
    #         if ylim:
    #             ax.set_ylim(ylim)

    #         self.canvas.draw()