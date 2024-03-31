# utils/config.py

import os
import yaml

default_config = {
    "start_stop_hotkey": "ctrl+shift+s",
    "note_hotkey": "ctrl+shift+n",
    "notes_dir": "./notes",
    "clear_description": True,
    "sound_effects": True
}

def ensure_config_exists():
    config_path = 'config.yaml'
    if not os.path.isfile(config_path):
        with open(config_path, 'w') as file:
            yaml.dump(default_config, file)
            print(f"'{config_path}' not found. A new file has been created with default settings.")

def load_config():
    ensure_config_exists()
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            config = {**default_config, **config}  # Merge default config with loaded config
            return config
    except yaml.YAMLError as exc:
        print(f"Error loading 'config.yaml': {exc}")
        return default_config

def save_config(config):
    try:
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file)
    except yaml.YAMLError as exc:
        print(f"Error saving 'config.yaml': {exc}")