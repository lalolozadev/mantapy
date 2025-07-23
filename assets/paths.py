import sys
import os

def resource_path(relative_path):
    """Devuelve la ruta absoluta del recurso, compatible con PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

logo_path = resource_path("assets/logo_mantapy.png")
arrow_down_path = resource_path("assets/down-arrow.png")