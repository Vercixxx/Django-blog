import json, os


current_directory = os.path.dirname(__file__)

parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
grandparent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))

file_path = os.path.join(grandparent_directory, 'private_files', 'secret_data.json')

with open(file_path, 'r') as file:
    json_data = json.load(file)
    
