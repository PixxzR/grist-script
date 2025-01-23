import json
import os

ADMIN_CONFIG_FILE = "data/admin_config.json"  # Fichier JSON pour stocker les exigences

# Charger la configuration depuis le fichier
def load_admin_config():
    if os.path.exists(ADMIN_CONFIG_FILE):
        with open(ADMIN_CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"required_columns": [], "duplicate_check_attribute": "", "duplicate_method": ""}

# Sauvegarder la configuration dans le fichier
def save_admin_config(config):
    with open(ADMIN_CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
