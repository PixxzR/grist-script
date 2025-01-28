import json
import os

ADMIN_CONFIG_FILE = "data/admin_config_test.json"  # Fichier JSON pour stocker les exigences

def load_admin_config():
    if os.path.exists(ADMIN_CONFIG_FILE):
        with open(ADMIN_CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

config = load_admin_config()

API_KEY = config.get("api_key", "default_api_key")
BASE_URL = config.get("base_url", "https://default.api.url")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
# Sauvegarder la configuration dans le fichier
def save_admin_config(config):
    with open(ADMIN_CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
import json
import os

