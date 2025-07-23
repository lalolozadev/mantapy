from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon, QFont
from windows.welcome import WelcomeWindow
import sys
from config.text import text_small
from assets.paths import logo_path


# Run the program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Verdana")
    app.setFont(font)
    app.setWindowIcon(QIcon(logo_path))
    window = WelcomeWindow()
    window.setWindowTitle("Mantapy - Welcome")
    window.show()
    sys.exit(app.exec())