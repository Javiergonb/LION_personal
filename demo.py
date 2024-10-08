# Copyright (c) 2022, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# NVIDIA CORPORATION & AFFILIATES and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION & AFFILIATES is strictly prohibited.

"""
    require diffusers-0.11.1
"""
import os
import clip
import torch
from PIL import Image
from default_config import cfg as config
from models.lion import LION
from utils.vis_helper import plot_points
from huggingface_hub import hf_hub_download 

model_path = '/home/javgonza/exp/0928/all/8e9753h_train_lion_B32/checkpoints/epoch_11999_iters_527999.pt'
model_config = '/home/javgonza/exp/0928/all/8e9753h_train_lion_B32/cfg.yml'

config.merge_from_file(model_config)
lion = LION(config)
lion.load_model(model_path)

if config.clipforge.enable:
    input_t = ["a swivel chair, five wheels"] 
    device_str = 'cuda'
    clip_model, clip_preprocess = clip.load(
                        config.clipforge.clip_model, device=device_str)    
    text = clip.tokenize(input_t).to(device_str)
    clip_feat = []
    clip_feat.append(clip_model.encode_text(text).float())
    clip_feat = torch.cat(clip_feat, dim=0)
    print('clip_feat', clip_feat.shape)
else:
    clip_feat = None

output = lion.sample(10)
pts = output['points']
#xyz_coordinates = output['z_reshape'][:, :, :3].squeeze(-1).squeeze(-1)
#print(xyz_coordinates)

#SAVE TENSOR
#torch.save(xyz_coordinates, '/home/javgonza/tensors/tensorDDPM.pth')
#print("Saved!")

#SAVE NUMPY ARRAY
#numpy_array = output.numpy()
#file_path = './Normalize.npy'
#np.savetxt(file_path, numpy_array, delimiter=' ')
#print(f'Tensor saved to {file_path}')

#SAVE AN IMAGE
img_name = "airplane_simmetry3.jpg"
plot_points(pts, output_name=img_name)
img = Image.open(img_name)
img.save("airplane_simmetry3.jpg")
img.close()