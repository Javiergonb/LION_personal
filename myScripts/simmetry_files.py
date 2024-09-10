import numpy as np
import open3d as o3d
import os
import torch
import json

def calculate_chamfer_distance(pcd1, pcd2):
    dists = pcd1.compute_point_cloud_distance(pcd2)
    return np.mean(dists)

def process_point_clouds_and_tensors_json(original_folder, encoded_folder, output_file):
    chamfer_distances = {}
    
    for filename in os.listdir(original_folder):
        if filename.endswith('.npy'):
            base_name = filename.split('.')[0]  # e.g., 'airplane1'
            print(f"Calculating Chanfer distance of: {base_name}")
            file_path = os.path.join(original_folder, filename)
            point_cloud_np = np.load(file_path)
            
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(point_cloud_np)
            
            # Mirror point cloud
            mirrored_np = point_cloud_np.copy()
            mirrored_np[:, 0] = -mirrored_np[:, 0]
            
            pcd_mirrored = o3d.geometry.PointCloud()
            pcd_mirrored.points = o3d.utility.Vector3dVector(mirrored_np)
            
            # Calculate Chamfer distance for original
            cd = calculate_chamfer_distance(pcd, pcd_mirrored)
            chamfer_distances[f'{base_name}_original'] = cd
            
            # Process encoded tensor
            encoded_filename = f'latent_points_{base_name}.pth'
            encoded_file_path = os.path.join(encoded_folder, encoded_filename)
            print(f"Calculating ENcoded distance of: {encoded_file_path}")
            if os.path.exists(encoded_file_path):
                tensor = torch.load(encoded_file_path)
                tensor_np = tensor.squeeze().detach().cpu().numpy()
                
                pcd_encoded = o3d.geometry.PointCloud()
                pcd_encoded.points = o3d.utility.Vector3dVector(tensor_np)
                
                # Mirror encoded point cloud
                mirrored_encoded_np = tensor_np.copy()
                mirrored_encoded_np[:, 0] = -mirrored_encoded_np[:, 0]
                
                pcd_encoded_mirrored = o3d.geometry.PointCloud()
                pcd_encoded_mirrored.points = o3d.utility.Vector3dVector(mirrored_encoded_np)
                
                # Calculate Chamfer distance for encoded
                cd_encoded = calculate_chamfer_distance(pcd_encoded, pcd_encoded_mirrored)
                chamfer_distances[f'{base_name}_encoded'] = cd_encoded
    
    # Save Chamfer distances to JSON file
    with open(output_file, 'w') as f:
        json.dump(chamfer_distances, f, indent=4)

# Example usage
process_point_clouds_and_tensors_json('/home/javgonza/LION/data/chair/train', '/home/javgonza/tensors/Shapenet/chair/train', '../chamfer_distances_chair.json')
