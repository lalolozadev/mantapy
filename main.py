from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from windows.welcome import WelcomeWindow
import sys

# Run the program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/logo_mantapy.ico"))
    window = WelcomeWindow()
    window.setWindowTitle("Mantapy - Welcome")
    window.show()
    sys.exit(app.exec())