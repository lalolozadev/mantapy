from .text import (
    text_large, text_small, text_normal
)
from .colors import *

# Button size
ini_size = (200, 35)
nav_size = (300, 30)

# Button config
padding = 5
border_radius = 5

# Colors
green = "#4CAF50"
green_hover = "#45a049"
green_pressed = "#388e3c"

gray = "#24292e"
gray_hover = "#2b3137"
gray_pressed = "#2b3137"

# Button style
start = ("QPushButton {"
    f"background-color: {verde1};"
    "color: white;"
    f"font-size: {text_normal}px;"
    f"border-radius: {border_radius}px;"
    f"padding: {padding}px;"
    "}"
    "QPushButton:hover {"
    f"background-color: {verde2};"
    "}"
    "QPushButton:pressed {"
    f"background-color: {verde1};"
    "}"
)

doc = ("QPushButton {"
    f"background-color: {azul1};"
    "color: white;"
    f"font-size: {text_normal}px;"
    f"border-radius: {border_radius}px;"
    f"padding: {padding}px;"
    "}"
    "QPushButton:hover {"
    f"background-color: {azul2};"
    "}"
    "QPushButton:pressed {"
    f"background-color: {azul1};"
    "}"
)

load_file = ("QPushButton {"
    f"background-color: {verde1};"
    "color: white;"
    f"font-size: {text_small}px;"
    f"border-radius: {border_radius}px;"
    f"padding: {padding}px;"
    "}"
    "QPushButton:hover {"
    f"background-color: {verde2};"
    "}"
    "QPushButton:pressed {"
    f"background-color: {verde1};"
    "}"
)

next = ("QPushButton {"
    f"background-color: {verde1};"
    "color: white;"
    f"font-size: {text_small}px;"
    f"border-radius: {border_radius}px;"
    f"padding: {padding}px;"
    "}"
    "QPushButton:hover {"
    f"background-color: {verde2};"
    "}"
    "QPushButton:pressed {"
    f"background-color: {verde2};"
    "}"
)

back = ("QPushButton {"
    f"background-color: {azul1};"
    "color: white;"
    f"font-size: {text_small}px;"
    f"border-radius: {border_radius}px;"
    f"padding: {padding}px;"
    "}"
    "QPushButton:hover {"
    f"background-color: {azul2};"
    "}"
    "QPushButton:pressed {"
    f"background-color: {azul1};"
    "}"
)

file_input = (
    "QLineEdit {"
    f"border: 2px solid #ccc;"
    f"border-radius: {border_radius}px;"
    f"padding: {padding}px;"
    f"font-size: {text_small}px;"
    f"background-color: #f9f9f9;"
    "}"
    "QLineEdit:focus {"
    f"border: 2px solid #0078D7;"
    f"background-color: #ffffff;"
    "}"
)
export_plot = ("QPushButton {"
    f"background-color: {verde1};"
    "color: white;"
    f"font-size: {text_small}px;"
    f"border-radius: {border_radius}px;"
    f"padding: {padding}px;"
    "}"
    "QPushButton:hover {"
    f"background-color: {verde2};"
    "}"
    "QPushButton:pressed {"
    f"background-color: {verde1};"
    "}"
)