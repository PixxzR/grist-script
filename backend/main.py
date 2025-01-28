from src.excel_reader import read_and_validate_excel
from src.grist_api import add_data_to_table, fetch_existing_records,update_records,build_update_payload,list_columns
from src.data_validation import filter_new_records
from flask import Flask, request, jsonify, send_from_directory
import time
import os
from flask_cors import CORS
from admin_config import load_admin_config, save_admin_config
import json


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
        # Charger la configuration des colonnes
        config = load_admin_config()
        required_columns = config.get("required_columns", [])
        duplicate_check_attribute = config.get("duplicate_check_attribute", "NIR")  # Par défaut, on prend NIR
        doc_id = config.get("doc_id")
        table_id = config.get("table_id")

        # Étape 1 : Récupération et validation du fichier Excel
        file = request.files['file']
        data = read_and_validate_excel(file)  # Charge les données sous forme de DataFrame
        print(f"Étape 1 : Données extraites de l'Excel\n{data}")  # Debug : Affiche les données extraites

        # Vérification des colonnes requises
        columns_in_excel = data.columns.tolist()
        print(f"Colonnes dans l'Excel : {columns_in_excel}")  # Debug : Affiche les colonnes disponibles dans l'Excel
        missing_columns = [col for col in required_columns if col not in columns_in_excel]
        if missing_columns:
            return jsonify({
                "status": "error",
                "message": f"Colonnes manquantes : {', '.join(missing_columns)}"
            }), 400

        # Étape 2 : Récupération des données existantes dans Grist
        existing_records = fetch_existing_records(doc_id, table_id)
        print(f"Étape 2 : Données existantes dans Grist\n{existing_records}")  # Debug : Affiche les données actuelles dans Grist

        # Étape 3 : Récupération des colonnes dans Grist
        columns = list_columns(doc_id, table_id)
        column_ids = [col['id'] for col in columns]
        print(f"Étape 3 : Colonnes disponibles dans Grist : {column_ids}")  # Debug : Affiche les colonnes dans Grist

        # Étape 4 : Association entre Excel et Grist
        new_records = data.to_dict(orient="records")  # Convertir les données Excel en liste de dictionnaires
        print(f"Étape 4 : Données Excel au format dict\n{new_records}")  # Debug : Affiche les données Excel transformées

        # Étape 5 : Comparaison des données pour mise à jour ou ajout
        additions = []
        updates = []

        for new_record in new_records:
            # Trouver un doublon potentiel dans les données existantes
            matching_record = next(
                (record for record in existing_records if record.get(duplicate_check_attribute) == new_record.get(duplicate_check_attribute)),
                None
            )

            if matching_record:
                # Combiner les champs existants et les nouveaux champs
                updated_fields = {}
                for column in column_ids:
                    existing_value = matching_record.get(column)
                    new_value = new_record.get(column)

                    # Si la colonne est vide dans Grist mais non vide dans Excel, on remplit
                    if existing_value is None or existing_value == "":
                        updated_fields[column] = new_value
                    # Si la valeur est différente, on remplace par celle de l'Excel
                    elif new_value != existing_value:
                        updated_fields[column] = new_value
                    # Si aucune modification, conserver la valeur actuelle
                    else:
                        updated_fields[column] = existing_value

                if updated_fields:
                    updates.append({"id": matching_record["id"], "fields": updated_fields})
            else:
                # Ajouter l'enregistrement si aucun doublon n'existe
                additions.append(new_record)
        print(f"Étape 5 : Nouveaux enregistrements à ajouter\n{additions}")  # Debug : Affiche les données à ajouter
        print(f"Étape 5 : Enregistrements à mettre à jour\n{updates}")  # Debug : Affiche les données à mettre à jour

        # Étape 6 : Envoi des ajouts et mises à jour à Grist
        if additions:
            add_data_to_table(doc_id, table_id, additions)
            print(f"Étape 6 : Ajout des enregistrements réussi")  # Debug : Confirme les ajouts

        if updates:
            update_records(doc_id, table_id, updates)
            print(f"Étape 6 : Mise à jour des enregistrements réussie")  # Debug : Confirme les mises à jour

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
        print(f"Erreur : {e}")  # Debug : Affiche l'erreur complète
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