import os
import numpy as np

# Path to the folder containing the normalized numpy files
output_folder_path = '../data/Plates_v_3'
i = 0
# Iterate over each file in the output folder
for filename in os.listdir(output_folder_path):
    if filename.endswith('.npy'):  # Check if the file is a numpy file
        file_path = os.path.join(output_folder_path, filename)
        
        # Load the normalized dataset
        normalized_dataset = np.load(file_path)
        print(normalized_dataset)
        # Check if all values fall within the range [0, 1]
        i += 1
        if np.all((normalized_dataset >= -1) & (normalized_dataset <= 1)):
            print(f"{filename}: Dataset is normalized correctly to the range [-1, 1].")
        else:
            print(f"{filename}:ERROR")

print(i)