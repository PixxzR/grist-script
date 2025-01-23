from src.excel_reader import read_and_validate_excel
from src.grist_api import add_data_to_table, fetch_existing_records
from src.column_operations import list_and_display_columns
from src.data_validation import filter_new_records
from flask import Flask, request, jsonify, send_from_directory
import time
import os

# Constantes de configuration
EXCEL_FILE = "data/fake_data.xlsx"
DOC_ID = "dDr69dYrw5zk"
TABLE_ID = "Table_Test_API"

# Liste pour stocker l'historique des imports
import_history = []

# Définir le chemin du dossier frontend
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="/")

@app.route("/")
def index():
    """
    Servir la page principale (index.html).
    """
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint pour téléverser un fichier Excel et importer les données dans Grist.
    """
    try:
        # Récupérer le fichier Excel
        file = request.files['file']
        data = read_and_validate_excel(file)

        # Récupérer les données existantes dans Grist
        existing_records = fetch_existing_records(DOC_ID, TABLE_ID)

        # Filtrer les nouveaux enregistrements
        unique_keys = ["Nom", "Ville"]
        filtered_records = filter_new_records(existing_records, data.to_dict(orient="records"), unique_keys)

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