import os
import torch
import numpy as np
from default_config import cfg as config
from models.lion import LION

# Paths
model_path = './lion_ckpt/unconditional/chair/checkpoints/model.pt'
model_config = './lion_ckpt/unconditional/chair/cfg.yml'
input_dir = '/home/javgonza/LION/data/chair/train'
output_dir = '/home/javgonza/tensors/Shapenet/chair/train'

# Config
config.merge_from_file(model_config)

# LION
lion = LION(config)
lion.load_model(model_path)

# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Iterate over all .npy files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.npy'):
        # Load the point cloud data from the .npy file
        file_path = os.path.join(input_dir, filename)
        point_cloud = np.load(file_path)

        # Add a batch dimension if needed
        point_cloud = np.expand_dims(point_cloud, axis=0)  # Now shape is [1, N, point_dim]

        # Convert to PyTorch tensor and move to device
        point_cloud_tensor = torch.tensor(point_cloud, dtype=torch.float32).to(device)

        # Get the latent representation
        h0 = lion.vae.get_latent_points(point_cloud_tensor)

        # Save the latent points with a name based on the original file
        output_filename = f'latent_points_{os.path.splitext(filename)[0]}.pth'
        torch.save(h0, os.path.join(output_dir, output_filename))
        print(f"Saved {output_filename}!")


