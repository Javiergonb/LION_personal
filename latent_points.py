import os
import torch
import numpy as np
from default_config import cfg as config
from models.lion import LION
from models.vae_adain import Model as VAE

# Paths
model_path = '/home/javgonza/exp/0912/all/ef370dh_hvae_lion_B16/checkpoints/epoch_7999_iters_703999.pt'
model_config = '/home/javgonza/exp/0912/all/ef370dh_hvae_lion_B16/cfg.yml'
input_dir = '/home/javgonza/LION/data/airplane/02691156/train'
output_dir = '/home/javgonza/tensors/NEWSHAPENET/train'

# Config
config.merge_from_file(model_config)
print(model_config)
# LION
#lion = LION(config)
#lion.load_model(model_path)

#VAE
vae = VAE(config).cuda()

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
        #print(f'THIS IS CLOUD TENSOR: {point_cloud_tensor}')

        # Get the latent representation
        h0 = vae.get_latent_points(point_cloud_tensor)
               

        # Save the latent points with a name based on the original file
        output_filename = f'latent_points_{os.path.splitext(filename)[0]}.pth'
        torch.save(h0, os.path.join(output_dir, output_filename))
        print(f"Saved {output_filename}!")


