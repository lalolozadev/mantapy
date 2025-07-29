import sys
import os

def resource_path(relative_path):
    """Devuelve la ruta absoluta del recurso, compatible con PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

sys_name = sys.platform

if sys_name == "linux":
    logo_path = resource_path("img/logo_mantapy.png")
    arrow_down_path = resource_path("img/down-arrow.png")
elif sys_name == "win32":
    logo_path = resource_path("assets/logo_mantapy.png")
    arrow_down_path = resource_path("assets/down-arrow.png")