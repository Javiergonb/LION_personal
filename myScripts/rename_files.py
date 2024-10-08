import os

def rename_files(directory):
    for filename in os.listdir(directory):
        if ' ' in filename:
            new_filename = filename.replace(' ', '_')
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f'Renamed: {filename} to {new_filename}')

rename_files('../data/3D_Models/Modern-Vase')

