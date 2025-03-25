from .text import text_normal

# Button size
ini_size = (250, 50)
nav_size = (250, 30)

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
    "font-size: 16px;"
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
    "font-size: 16px;"
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
    "font-size: 12px;"
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
    "font-size: 12px;"
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
    "font-size: 12px;"
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