import os
import open3d as o3d
import numpy as np
import shutil
import random
from pathlib import Path

def mesh_to_point_cloud(file_path, output_file):
    mesh = o3d.io.read_triangle_mesh(file_path)
    pcd = mesh.sample_points_uniformly(number_of_points=15000)
    point_cloud_np = np.asarray(pcd.points)
    return point_cloud_np

def convert_folder_to_point_cloud(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all mesh files in the input folder
    mesh_files = [f for f in os.listdir(input_folder) if f.endswith(('.obj','.off'))]
    for mesh_file in mesh_files:
        print(mesh_file)
        mesh_file_path = os.path.join(input_folder, mesh_file)
        output_point_cloud_path = os.path.join(output_folder, f"{os.path.splitext(mesh_file)[0]}_point_cloud.npy")

        # Convert each mesh to a point cloud
        point_cloud_np = mesh_to_point_cloud(mesh_file_path, output_point_cloud_path)
        np.save(output_point_cloud_path, point_cloud_np)
        print(f"Converted {mesh_file} to {output_point_cloud_path}")

#input_folder = "/home/javgonza/LION/data/plates_and_bowls_v1"
#output_folder = "/home/javgonza/LION/data/plates_and_bowls_v_1"
#convert_folder_to_point_cloud(input_folder,output_folder)

def split_data(input_folder, output_folder, split_ratios=(0.7, 0.1, 0.2)):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Create train, val, and test folders
    for folder in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output_folder, folder), exist_ok=True)

    # List all npy files in the input folder
    npy_files = [file for file in os.listdir(input_folder) if file.endswith('.npy')]
    num_files = len(npy_files)

    # Shuffle the list of files
    random.shuffle(npy_files)

    # Calculate the number of files for each split
    train_size = int(num_files * split_ratios[0])
    val_size = int(num_files * split_ratios[1])
    test_size = num_files - train_size - val_size

    # Move files to respective folders
    for i, file in enumerate(npy_files):
        if i < train_size:
            shutil.move(os.path.join(input_folder, file), os.path.join(output_folder, 'train', file))
        elif i < train_size + val_size:
            shutil.move(os.path.join(input_folder, file), os.path.join(output_folder, 'val', file))
        else:
            shutil.move(os.path.join(input_folder, file), os.path.join(output_folder, 'test', file))

    print(f"Data split completed: {train_size} files for training, {val_size} files for validation, {test_size} files for testing.")


input_folder = '/home/javgonza/LION/data/plates_and_bowls_v_1'
output_folder = '/home/javgonza/LION/data/plates_and_bowls_v_1/04580795'
split_data(input_folder, output_folder, split_ratios=(0.8, 0.1, 0.1))
