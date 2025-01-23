from src.excel_reader import read_and_validate_excel
from src.grist_api import add_data_to_table, fetch_existing_records
from src.column_operations import list_and_display_columns
from src.data_validation import filter_new_records
from flask import Flask, request, jsonify, send_from_directory
import time
import os
from flask_cors import CORS
from admin_config import load_admin_config, save_admin_config
import json

# Constantes de configuration
EXCEL_FILE = "data/fake_data.xlsx"
DOC_ID = "dDr69dYrw5zk"
TABLE_ID = "Table_Test_API"

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
        # Retourne la configuration actuelle
        config = load_admin_config()
        return jsonify(config)

    if request.method == "POST":
        # Met à jour la configuration
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

            # Sauvegarder la configuration
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
        # Charger la configuration des colonnes
        config = load_admin_config()
        required_columns = config.get("required_columns", [])
        duplicate_check_attribute = config.get("duplicate_check_attribute")
        duplicate_method = config.get("duplicate_method")
        # Récupérer le fichier Excel
        file = request.files['file']
        data = read_and_validate_excel(file)

        # Vérifier que les colonnes respectent les exigences
        columns_in_excel = data.columns.tolist()
        missing_columns = [col for col in required_columns if col not in columns_in_excel]

        if missing_columns:
            return jsonify({
                "status": "error",
                "message": f"Colonnes manquantes : {', '.join(missing_columns)}"
            }), 400

        # Récupérer les données existantes dans Grist
        existing_records = fetch_existing_records(DOC_ID, TABLE_ID)

        # Filtrer les nouveaux enregistrements
        filtered_records = filter_new_records(
            existing_records,
            data.to_dict(orient="records"),
            duplicate_check_attribute,
            duplicate_method
        )
        # Ajouter dans Grist
        if filtered_records:
            add_data_to_table(DOC_ID, TABLE_ID, filtered_records)
            import_history.append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "success",
                "added": len(filtered_records),
                "message": "Import réussi"
            })
            return jsonify({"status": "success", "added": len(filtered_records)})
        else:
            import_history.append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "no_update",
                "added": 0,
                "message": "Aucun nouvel enregistrement à ajouter"
            })
            return jsonify({"status": "no_update", "message": "Aucun nouvel enregistrement à ajouter."})

    except Exception as e:
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