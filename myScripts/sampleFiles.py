import os
import random
import shutil

# Set the source and destination directories
source_dir = '/home/javgonza/LION/data/bedge'
destination_dir = '/home/javgonza/LION/data/useable_bed'

# Get a list of all files in the source directory
all_files = os.listdir(source_dir)

# Randomly select 120 files
files_to_move = random.sample(all_files, 120)

# Move each selected file to the destination directory
for file_name in files_to_move:
    shutil.move(os.path.join(source_dir, file_name), destination_dir)

print(f"Moved {len(files_to_move)} files from {source_dir} to {destination_dir}.")
