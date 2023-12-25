from glob import glob
from os.path import join
from pprint import pprint
import os


def get_folder_info(folder_path):
    """get detiled info for a folder
        1. number of files
        2. file size distribution
        3. file type distribution

    Args:
        folder_path (str): path to the folder
    """
    file_list = glob(join(folder_path, "**/*"), recursive=True)
    total_n_folders = len([f for f in file_list if os.path.isdir(f)])
    total_n_files = len(file_list) - total_n_folders
    print(f"=== Folder info for [{folder_path}] ===")
    print(f"n folders: {total_n_folders}")
    print(f"n files: {total_n_files}")
    total_size = sum([os.path.getsize(f) for f in file_list if os.path.isfile(f)])
    print(f"total size: {total_size//1048576} MB, {total_size%1048576} Bytes")
    print("=== Size distribution ===")
    # get file size distribution
    file_size_list = [os.path.getsize(f) for f in file_list if os.path.isfile(f)]
    file_size_list.sort()
    file_size_index = {
        1:"0B",
        1024: "0B<x<1KB",
        4*1024: "1KB<=x<4KB", 
        16*1024: "4KB<=x<16KB", 
        64*1024: "16KB<=x<64KB",
        256*1024: "64KB<=x<256KB", 
        1024*1024: "256KB<=x<1MB", 
        4*1024*1024: "1MB<=x<4MB", 
        16*1024*1024: "4MB<=x<16MB",
        64*1024*1024: "16MB<=x<64MB", 
        256*1024*1024: "64MB<=x<256MB", 
        1024*1024*1024: "256MB<=x<1GB", 
        4*1024*1024*1024: "1GB<=x<4GB",
        16*1024*1024*1024: "4GB<=x<16GB", 
        64*1024*1024*1024: "16GB<=x<64GB", 
        256*1024*1024*1024: "64GB<=x<256GB",
        1024*1024*1024*1024: "256GB<=x<1TB", 
        4*1024*1024*1024*1024: "1TB<=x<4TB", 
        16*1024*1024*1024*1024: "4TB<=x<16TB",
        64*1024*1024*1024*1024: "16TB<=x<64TB",
        256*1024*1024*1024*1024: "64TB<=x<256TB",
        1024*1024*1024*1024*1024: "256TB<=x<1PB"}
        
    file_size_dist = {k:0 for k in file_size_index.keys()}
    for file_size in file_size_list:
        for size in file_size_dist.keys():
            if file_size < size:
                file_size_dist[size] += 1
    counted = 0
    for k in sorted(file_size_dist.keys()):
        file_size_dist[k] -= counted
        counted += file_size_dist[k]
        if file_size_dist[k] > 0:
            print(f"{file_size_index[k]}: {file_size_dist[k]}")

    # get file type distribution
    print("=== File type distribution ===")
    file_type_list = [os.path.splitext(f)[1] for f in file_list if os.path.isfile(f)]
    file_type_dist = {}
    for file_type in file_type_list:
        if file_type in file_type_dist.keys():
            file_type_dist[file_type] += 1
        else:
            file_type_dist[file_type] = 1
    # print sorted by value
    lesser_file_types = {k:file_type_dist[k] for k in file_type_dist.keys() if file_type_dist[k] < 10}
    for k in sorted(file_type_dist, key=file_type_dist.get, reverse=True):
        if file_type_dist[k] >= 10:
            print(f"{k}: {file_type_dist[k]}")
    print("_lesser file types_")
    print(lesser_file_types)