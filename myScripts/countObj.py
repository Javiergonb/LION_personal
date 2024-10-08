import os

def count_obj_files(directory):
    obj_files = [file for file in os.listdir(directory) if file.endswith('.obj')]
    return len(obj_files)

directory_path = '../data/Museum_Dataset/Plate/Broken_Bottom'
obj_count = count_obj_files(directory_path)
print("Number of .obj files:", obj_count)
