import os
import shutil

def move_files_by_number(input_number, source_directory, destination_directory):
    # Check if the source directory exists
    if not os.path.exists(source_directory):
        print(f"Source directory '{source_directory}' does not exist.")
        return
    
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    
    # Loop through the expected file extensions
    extensions = ['.obj', '.obj.jpg', '.obj.mtl']
    for ext in extensions:
        # Form the filename based on input_number and the current extension
        filename = f"{input_number}{ext}"
        # Form the full path of the source file
        source_file = os.path.join(source_directory, filename)
        # Check if the file exists
        if os.path.exists(source_file):
            # Form the full path of the destination file
            destination_file = os.path.join(destination_directory, filename)
            # Move the file to the destination directory
            shutil.move(source_file, destination_file)
            print(f"Moved {filename} to {destination_directory}")

# Example usage:
input_number = input("Enter the four digit number: ")
source_directory = "../data/Museum_Dataset/Plate/Broken_Bottom"
destination_directory = "../data/Museum_Dataset"

move_files_by_number(input_number, source_directory, destination_directory)
