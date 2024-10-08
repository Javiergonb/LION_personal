import os
import numpy as np

# Path to the folder containing the numpy files
input_folder_path = '/home/javgonza/LION/data/plates_and_bowls_v_1/04580795/train'

# Path to the folder where you want to save the normalized datasets
output_folder_path = '/home/javgonza/LION/data/normalized_plates_and_bowls/train'

# Ensure the output directory exists
os.makedirs(output_folder_path, exist_ok=True)

# Iterate over each file in the input folder
for filename in os.listdir(input_folder_path):
    if filename.endswith('.npy'):  # Check if the file is a numpy file
        input_file_path = os.path.join(input_folder_path, filename)
        
        # Load point cloud from .npy file
        point_cloud = np.load(input_file_path)  # Shape: (N, 3)

        # Calculate the mean of the bounding box (center)
        bbox_min = np.min(point_cloud, axis=0)  # Shape: (3,)
        bbox_max = np.max(point_cloud, axis=0)  # Shape: (3,)
        bbox_center = (bbox_max + bbox_min) / 2  # Shape: (3,)

        # Calculate the scale (half the length of the largest dimension of the bounding box)
        bbox_scale = np.max(bbox_max - bbox_min) / 2  # Scalar

        # Normalize the point cloud
        normalized_point_cloud = (point_cloud - bbox_center) / bbox_scale

        # Path to save the normalized point cloud
        output_file_path = os.path.join(output_folder_path, filename)

        # Save the normalized point cloud
        np.save(output_file_path, normalized_point_cloud)

        print(f'Normalized point cloud saved to: {output_file_path}')
