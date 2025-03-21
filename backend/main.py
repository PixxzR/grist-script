from flask import Flask, request, jsonify, send_from_directory
import time
import os
from flask_cors import CORS
from admin_config import load_admin_config, save_admin_config
from src.excel_handler import read_and_validate_excel
from src.grist_handler import get_grist_data, push_to_grist
from src.data_processor import process_records

# Liste pour stocker l'historique des imports
import_history = []

# Définir le chemin du dossier frontend
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="/")
CORS(app, origins=["http://localhost:8080"])
ADMIN_CONFIG_FILE = os.path.join("data", "admin_config.json")



@app.route("/")
def index():
    return send_from_directory("../frontend/svelte-app/public", "index.html")


@app.route("/admin/config", methods=["GET", "POST"])
def admin_config():
    """
    Gérer la configuration de l'administration :
    - GET : Récupérer la configuration actuelle
    - POST : Mettre à jour la configuration
    """
    if request.method == "GET":
        config = load_admin_config()
        return jsonify(config)

    if request.method == "POST":
        try:
            data = request.json
            config = load_admin_config()

            # Mettre à jour les colonnes obligatoires
            if "required_columns" in data:
                config["required_columns"] = data["required_columns"]

            # Mettre à jour l'attribut à vérifier pour les doublons
            if "duplicate_check_attribute" in data:
                config["duplicate_check_attribute"] = data["duplicate_check_attribute"]

            # Mettre à jour la méthode de gestion des doublons
            if "duplicate_method" in data:
                config["duplicate_method"] = data["duplicate_method"]

            # Mettre à jour les valeurs de DOC_ID et TABLE_ID
            if "doc_id" in data:
                config["doc_id"] = data["doc_id"]
            if "table_id" in data:
                config["table_id"] = data["table_id"]

            # Mettre à jour la clé API
            if "api_key" in data:
                config["api_key"] = data["api_key"]

            # Mettre à jour la base URL
            if "base_url" in data:
                config["base_url"] = data["base_url"]

            save_admin_config(config)
            return jsonify({"message": "Configuration mise à jour avec succès", "config": config})

        except Exception as e:
            return jsonify({"message": f"Erreur lors de la mise à jour : {str(e)}"}), 500
                


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint pour téléverser un fichier Excel et importer les données dans Grist.
    """
    try:
        # Charger la configuration
        config = load_admin_config()
        required_columns = config.get("required_columns", [])
        duplicate_check_attribute = config.get("duplicate_check_attribute", "NIR")
        doc_id = config.get("doc_id")
        table_id = config.get("table_id")

        # Étape 1 : Lecture et validation du fichier Excel
        file = request.files['file']
        data = read_and_validate_excel(file, required_columns)
        print(f"Étape 1 : Données extraites de l'Excel\n{data}")

        # Étape 2 : Récupération des données de Grist
        existing_records, column_ids = get_grist_data(doc_id, table_id)
        print(f"Étape 2 : Données existantes dans Grist\n{existing_records}")
        print(f"Étape 3 : Colonnes disponibles dans Grist : {column_ids}")

        if "Date de transmission données MDPH" not in column_ids:
            return jsonify({"status": "error", "message": "La colonne 'Date de transmission données MDPH' est manquante dans Grist."}), 400

        # Étape 4 : Préparer les données à ajouter ou mettre à jour
        new_records = data.to_dict(orient="records")
        additions, updates = process_records(new_records, existing_records, column_ids, duplicate_check_attribute)

        print(f"Étape 5 : Nouveaux enregistrements à ajouter\n{additions}")
        print(f"Étape 5 : Enregistrements à mettre à jour\n{updates}")

        # Étape 6 : Envoyer les données à Grist
        push_to_grist(doc_id, table_id, additions, updates)

        # Journaliser l'import
        import_history.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "success",
            "added": len(additions),
            "updated": len(updates),
            "message": "Import et mise à jour réussis"
        })

        return jsonify({"status": "success", "added": len(additions), "updated": len(updates)})

    except Exception as e:
        print(f"Erreur : {e}")
        import_history.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "error",
            "message": str(e)
        })
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/status', methods=['GET'])
def get_status():
    """
    Endpoint pour vérifier le statut des imports récents.
    """
    if import_history:
        return jsonify({"import_history": import_history})
    else:
        return jsonify({"message": "Aucun historique d'import trouvé."})


if __name__ == "__main__":
    app.run(debug=True)