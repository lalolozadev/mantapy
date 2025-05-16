from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon, QFont
from windows.welcome import WelcomeWindow
import sys
from config.text import text_small


# Run the program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Verdana")
    app.setFont(font)
    app.setWindowIcon(QIcon("assets/logo_mantapy.ico"))
    window = WelcomeWindow()
    window.setWindowTitle("Mantapy - Welcome")
    window.show()
    sys.exit(app.exec())