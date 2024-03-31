# utils/config.py
import os
import yaml

# Determine the path to the user's Documents directory
documents_dir = os.path.join(os.path.expanduser('~'), 'Documents')
# Specify the directory where the ClipNotes configuration will be stored
clipnotes_config_dir = os.path.join(documents_dir, 'ClipNotes')
# Specify the directory within ClipNotes where notes will be specifically stored
notes_dir = os.path.join(clipnotes_config_dir, 'Notes')

# Ensure the ClipNotes configuration directory exists
if not os.path.exists(clipnotes_config_dir):
    os.makedirs(clipnotes_config_dir)

# Ensure the notes directory exists
if not os.path.exists(notes_dir):
    os.makedirs(notes_dir)

# Path to the configuration file within the ClipNotes directory
config_path = os.path.join(clipnotes_config_dir, 'config.yaml')

default_config = {
    "start_stop_hotkey": "ctrl+shift+s",
    "note_hotkey": "ctrl+shift+n",
    "notes_dir": notes_dir,  # Pointing to the specific Notes directory
    "clear_description": True,
    "sound_effects": True
}

def ensure_config_exists():
    if not os.path.isfile(config_path):
        with open(config_path, 'w') as file:
            yaml.dump(default_config, file)
            print(f"'{config_path}' not found. A new file has been created with default settings.")

def load_config():
    ensure_config_exists()
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            # Ensure that notes_dir always points to the specific Notes directory
            config['notes_dir'] = notes_dir
            return config
    except yaml.YAMLError as exc:
        print(f"Error loading '{config_path}': {exc}")
        return default_config

def save_config(config):
    try:
        with open(config_path, 'w') as file:
            yaml.dump(config, file)
    except yaml.YAMLError as exc:
        print(f"Error saving '{config_path}': {exc}")