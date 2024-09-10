import os
import shutil

def count_and_copy_obj_files(source_directory, destination_directory):
    obj_files = [file for file in os.listdir(source_directory) if file.endswith('.obj')]
    for obj_file in obj_files:
        source_path = os.path.join(source_directory, obj_file)
        destination_path = os.path.join(destination_directory, obj_file)
        shutil.copy(source_path, destination_path)
    return len(obj_files)

source_directory_path = '../data/Museum_Dataset/Plate/Broken_Bottom'
destination_directory_path = '../data/Plates_Obj'

obj_count = count_and_copy_obj_files(source_directory_path, destination_directory_path)
print("Number of .obj files copied:", obj_count)
