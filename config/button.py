from .text import (
    text_large, text_small
)

# Button size
ini_size = (250, 50)
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
    f"background-color: {green};"
    "color: white;"
    f"font-size: {text_large}px;"
    f"border-radius: {border_radius}px;"
    f"padding: {padding}px;"
    "}"
    "QPushButton:hover {"
    f"background-color: {green_hover};"
    "}"
    "QPushButton:pressed {"
    f"background-color: {green_pressed};"
    "}"
)

doc = ("QPushButton {"
    f"background-color: {gray};"
    "color: white;"
    f"font-size: {text_large}px;"
    f"border-radius: {border_radius}px;"
    f"padding: {padding}px;"
    "}"
    "QPushButton:hover {"
    f"background-color: {gray_hover};"
    "}"
    "QPushButton:pressed {"
    f"background-color: {gray_pressed};"
    "}"
)

load_file = ("QPushButton {"
    f"background-color: {green};"
    "color: white;"
    f"font-size: {text_small}px;"
    f"border-radius: {border_radius}px;"
    f"padding: {padding}px;"
    "}"
    "QPushButton:hover {"
    f"background-color: {green_hover};"
    "}"
    "QPushButton:pressed {"
    f"background-color: {green_pressed};"
    "}"
)

next = ("QPushButton {"
    f"background-color: {green};"
    "color: white;"
    f"font-size: {text_small}px;"
    f"border-radius: {border_radius}px;"
    f"padding: {padding}px;"
    "}"
    "QPushButton:hover {"
    f"background-color: {green_hover};"
    "}"
    "QPushButton:pressed {"
    f"background-color: {green_pressed};"
    "}"
)

back = doc = ("QPushButton {"
    f"background-color: {gray};"
    "color: white;"
    f"font-size: {text_small}px;"
    f"border-radius: {border_radius}px;"
    f"padding: {padding}px;"
    "}"
    "QPushButton:hover {"
    f"background-color: {gray_hover};"
    "}"
    "QPushButton:pressed {"
    f"background-color: {gray_pressed};"
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