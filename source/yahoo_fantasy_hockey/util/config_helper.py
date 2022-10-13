import json
import os
import fnmatch
from pathlib import Path

current_folder = os.path.dirname(os.path.realpath(__file__))

def get_files(folder, pattern):
    result = []
    for root, dir, files in os.walk(folder):
        for items in fnmatch.filter(files, pattern):
            result.append(str(root)+'/'+str(items))
    return result

def load_config():
    config_folder = os.path.join(Path(current_folder).parent, 'config')

    result = {}
    config_folder_files = get_files(config_folder, '[*.json')
    for file in config_folder_files:
        filename_dict_key = file.split('/')[-1].replace('json', '')
        with open(file) as config_file:
            result[filename_dict_key] = json.load(config_file)
    
    return result

