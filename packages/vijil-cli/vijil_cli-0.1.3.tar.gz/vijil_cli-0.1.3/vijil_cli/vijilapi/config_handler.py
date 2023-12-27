import json

CONFIG_FILE_PATH = "vijil_config.json"

def save_config(username, token):
    config_data = {"username": username, "token": token}
    with open(CONFIG_FILE_PATH, 'w') as config_file:
        json.dump(config_data, config_file)

def load_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data.get("username"), config_data.get("token")
    except FileNotFoundError:
        return None, None