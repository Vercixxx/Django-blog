import json, os


current_directory = os.path.dirname(__file__)

parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
grandparent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))

secret_file_path = os.path.join(grandparent_directory, 'private_files', 'secret_data.json')
key_file_path = os.path.join(grandparent_directory, 'private_files', 'secret_key.txt')

with open(secret_file_path, 'r') as file:
    json_data = json.load(file)
    
with open(key_file_path, 'r') as file:
    SECRET_KEY_VALUE = file.read().strip()
