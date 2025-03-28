from PyQt6.QtWidgets import QApplication
from windows.welcome import WelcomeWindow
import sys

# Run the program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec())

