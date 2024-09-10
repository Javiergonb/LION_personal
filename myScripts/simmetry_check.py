import torch
import open3d as o3d
import numpy as np

# Example PyTorch tensor (point cloud with shape (1, num_points, 3))
h_tensor = torch.load("/home/javgonza/tensors/Plates/train/latent_points_NA-effigy_661_point_cloud.pth")

# Convert the tensor to a NumPy array
h_np = h_tensor.squeeze().detach().cpu().numpy()  # Remove the batch dimension and move to CPU

# Convert the NumPy array to an Open3D PointCloud object
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(h_np)

# Example: Mirror the point cloud along the YZ-axis using PyTorch
h_mirrored_tensor = h_tensor.clone()
h_mirrored_tensor[:, :, 0] = -h_mirrored_tensor[:, :, 0]

# Convert the mirrored tensor to a NumPy array
h_mirrored_np = h_mirrored_tensor.squeeze().detach().cpu().numpy()

# Convert the mirrored NumPy array to an Open3D PointCloud object
pcd_mirrored = o3d.geometry.PointCloud()
pcd_mirrored.points = o3d.utility.Vector3dVector(h_mirrored_np)

# Compute Chamfer Distance between the original and mirrored point clouds
dists = pcd.compute_point_cloud_distance(pcd_mirrored)
cd = np.mean(dists)
print(f"Chamfer Distance: {cd}")
