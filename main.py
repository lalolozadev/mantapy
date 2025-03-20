from PyQt6.QtWidgets import QApplication
from windows.welcome import WelcomeWindow
import sys


# Run the program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec())

# # Verify if the data file exists
# def verify_file(self):
#     cont = 0
#     while not os.path.exists(self.data_dir):
#         print(f"Checking if the file exists: {self.data_dir}")
#         print("File does not exist, please try again.")
#         self.get_input()
#         cont += 1

#         if cont == 2:
#             return None  # Return None if file doesn't exist after two attempts
    
#     return self.data_dir

# # Get file type using magic module
# def get_file_type(self, file_path):
#     file_type = magic.from_file(file_path, mime=True)
#     return file_type

# # Main method to run the program logic
# def run(self):
#     self.show_welcome_message()
#     self.get_input()
    
#     verified_file = self.verify_file()
#     if not verified_file:
#         print("File verification failed. Exiting program.")
#         return
    
#     print(f"File found at: {verified_file}")
    
#     file_type = self.get_file_type(verified_file)
#     print(f"The file type is: {file_type}")

