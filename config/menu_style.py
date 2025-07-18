from .text import text_small
from .colors import *

padding = 5
border_radius = 5

menu = ("QComboBox {"
        f"background-color: {azul3};"
        "border: 1px solid gray;"
        f"padding: {padding}px;"
        f"border-radius: {border_radius}px;"
        "color: black;"
        f"font-size: {text_small}px;"
    "}"
    "QComboBox::drop-down {"
        "border-left: 1px solid gray;"
        #"background-color: #dcdcdc;"
        "width: 20px;"
    "}"
    "QComboBox::down-arrow {"
        "image: url(assets/down-arrow.png);"
        "width: 10px;"
        "height: 10px;"
    "}"
    )

file_input_style = (
    "QLineEdit {"
        f"background-color: {azul3};"
        "border: 1px solid gray;"
        f"padding: {padding}px;"
        f"border-radius: {border_radius}px;"
        "color: black;"
        f"font-size: {text_small}px;"
    "}"
)