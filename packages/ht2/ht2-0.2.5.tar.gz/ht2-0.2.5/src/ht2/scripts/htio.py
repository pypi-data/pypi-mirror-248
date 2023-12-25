from ..tools.htio_ops import get_folder_info
import argparse
from glob import glob 
from os.path import join,getsize
import os
from pprint import pprint

def get_path_size(folder_path):
    """
    Recursively calculate the total size of a folder and its subfolders
    Args:
        folder_path (str): path to the folder
    Returns:
        int: total size in bytes
    """
    total_size = 0
    if not os.path.isdir(folder_path):
        return getsize(folder_path)
    for path, dirs, files in os.walk(folder_path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += getsize(fp)
    return total_size


def chunk_up_folder(folder_path, chunk_size=4*1024**3):
    """
    Split a folder into chunks of size less than chunk_size
    note: this is not a recursive function, it only splits at the first level
    Args:
        folder_path (str): path to the folder
        chunk_size (int): chunk size in bytes
    """
    sub_list = glob(join(folder_path, "*"))
    sub_list.sort()
    sub_sizes = [get_path_size(sub) for sub in sub_list]
    chunks = []
    current_chunk = []
    current_chunk_size = 0
    for i in range(len(sub_list)):
        print(sub_list[i], sub_sizes[i])
        if sub_sizes[i] > chunk_size:
            raise Exception(f"file {sub_list[i]} is larger than chunk size {chunk_size}")
        
        if current_chunk_size + sub_sizes[i] > chunk_size:
            chunks.append(current_chunk)
            current_chunk = []
            current_chunk_size = 0
        current_chunk.append(sub_list[i])
        current_chunk_size += sub_sizes[i]
    chunks.append(current_chunk)
    for idx,chunk in enumerate(chunks):
        # chunk_000001/
        chunk_path = join(folder_path, f"chunk_{idx:06d}")
        os.makedirs(chunk_path, exist_ok=True)
        for item in chunk:
            # move file to new folder
            os.rename(item, join(chunk_path, os.path.basename(item)))
        

    pprint(chunks)
    print(len(chunks))




def main():
    parser = argparse.ArgumentParser(description='get folder info')
    parser.add_argument('--task','-t', type=str, default="info", help='select task: info, split, zip, unzip')
    parser.add_argument('--input_folder','-i', type=str, default=".", help='input folder')
    parser.add_argument('--output_folder','-o', type=str, default=".", help='output folder')
    parser.add_argument('--size','-s', type=str, default="4GB", help='size')
    args = parser.parse_args()
    size_str = args.size
    size_byte = 0
    if size_str[-2:] == "KB":
        size_byte = int(size_str[:-2])*1024**1
    elif size_str[-2:] == "MB":
        size_byte = int(size_str[:-2])*1024**2
    elif size_str[-2:] == "GB":
        size_byte = int(size_str[:-2])*1024**3
    elif size_str[-2:] == "TB":
        size_byte = int(size_str[:-2])*1024**4
    elif size_str[-2:] == "PB":
        size_byte = int(size_str[:-2])*1024**5
    else:
        raise Exception(f"size unit {size_str[-2:]} not supported")

    if args.task == "info":
        get_folder_info(args.input_folder)
    elif args.task == "split":
        chunk_up_folder(args.input_folder, chunk_size=size_byte)

    total_size = get_path_size(args.input_folder)
    print(f"Total size of folder {args.input_folder}: {total_size//1048576} MB, {total_size%1048576} Bytes")


if __name__ == "__main__":
    main()



