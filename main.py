import os
import magic

class Mantapy:
    
    def __init__(self, data_dir=None):
        self.data_dir = data_dir
    
    # Presentation
    def show_welcome_message(self):
        print("""
                *** Welcome to Mantapy ***
                Created by: Eduardo Loza
    Open-source project for oceanographic data analysis.
    
    → Please enter the file name or full directory where your data is located.
    Example: /home/mydata/data.csv
        """)
    
    # Request user input
    def get_input(self):
        self.data_dir = input(">>> ")

    # Verify if the data file exists
    def verify_file(self):
        cont = 0
        while not os.path.exists(self.data_dir):
            print(f"Checking if the file exists: {self.data_dir}")
            print("File does not exist, please try again.")
            self.get_input()
            cont += 1

            if cont == 2:
                return None  # Return None if file doesn't exist after two attempts
        
        return self.data_dir

    # Get file type using magic module
    def get_file_type(self, file_path):
        file_type = magic.from_file(file_path, mime=True)
        return file_type
    
    # Main method to run the program logic
    def run(self):
        self.show_welcome_message()
        self.get_input()
        
        verified_file = self.verify_file()
        if not verified_file:
            print("File verification failed. Exiting program.")
            return
        
        print(f"File found at: {verified_file}")
        
        file_type = self.get_file_type(verified_file)
        print(f"The file type is: {file_type}")

# Run the program
if __name__ == "__main__":
    mantapy = Mantapy()  # Create an instance of the Mantapy class
    mantapy.run()  # Execute the program logic
