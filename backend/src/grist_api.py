import requests
from admin_config import load_admin_config
# Charger les configurations
config = load_admin_config()
BASE_URL = config.get("base_url", "")
API_KEY = config.get("api_key", "")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def add_records(doc_id, table_id, records):
    """
    Ajoute des enregistrements à une table existante dans Grist.
    """
    url = f"{BASE_URL}/docs/{doc_id}/tables/{table_id}/records"
    payload = {"records": [{"fields": record} for record in records]}
    print(f"Payload envoyé : {payload}")  # DEBUG : Affiche le contenu envoyé
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json().get("records", [])

def list_columns(doc_id, table_id, include_hidden=False):
    """
    Liste les colonnes d'une table spécifique.
    """
    url = f"{BASE_URL}/docs/{doc_id}/tables/{table_id}/columns"
    params = {"hidden": str(include_hidden).lower()}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json().get("columns", [])

def add_data_to_table(doc_id, table_id, records):
    """
    Ajoute des enregistrements à une table dans Grist.
    """
    try:
        response = add_records(doc_id, table_id, records)
        print(f"Enregistrements ajoutés : {[record['id'] for record in response]}")
        return response
    except Exception as e:
        print(f"Erreur lors de l'ajout des enregistrements : {e}")
        return None

def fetch_existing_records(doc_id, table_id):
    """
    Récupère tous les enregistrements existants dans une table Grist.
    """
    url = f"{BASE_URL}/docs/{doc_id}/tables/{table_id}/records"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        records = response.json().get("records", [])
        # Inclut l'ID dans les données retournées
        existing_data = [
            {
                "id": record["id"],  # Ajoute l'ID unique de Grist
                **record["fields"],  # Inclut les champs de la ligne
            }
            for record in records
        ]
        return existing_data
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des enregistrements existants : {e}")
        return []   
     
def update_records(doc_id, table_id, records):
    """
    Met à jour les enregistrements existants dans une table Grist.

    Parameters:
    - doc_id (str): ID du document.
    - table_id (str): ID de la table.
    - records (list): Liste des enregistrements à mettre à jour, avec leurs IDs.

    Returns:
    - dict: Réponse contenant les IDs des enregistrements mis à jour.
    """
    # Récupérer toutes les colonnes disponibles dans Grist
    columns = list_columns(doc_id, table_id)
    column_ids = [col['id'] for col in columns]
    print(f"Noms des colonnes dans Grist : {column_ids}")  # Debug : Affiche les colonnes disponibles

    # Construire les enregistrements pour le payload
    payload_records = []
    for record in records:
        # Vérifier que chaque enregistrement a bien la structure attendue
        if "id" in record and "fields" in record:
            # S'assurer que toutes les colonnes sont présentes dans `fields`
            for column in column_ids:
                if column not in record["fields"]:
                    record["fields"][column] = None  # Ajouter les colonnes manquantes avec `None`

            payload_records.append(record)
        else:
            print(f"Enregistrement mal formé : {record}")  # Debug : Log des enregistrements incorrects

    # Construire le payload final
    url = f"{BASE_URL}/docs/{doc_id}/tables/{table_id}/records"
    payload = {"records": payload_records}

    # Debug : Afficher le payload avant l'envoi
    print(f"Payload pour update : {payload}")

    try:
        response = requests.patch(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la mise à jour des enregistrements : {e}")
        print(f"Erreur complète : {e.response.text}")  # Debug : Affiche les détails de l'erreur
        return None
    

# Ajout d'une fonction pour compléter les données à partir de l'existant
def build_update_payload(existing_records, updated_fields, columns):
    """
    Construit un payload pour mettre à jour les enregistrements en conservant les valeurs existantes.

    Parameters:
    - existing_records (list): Les enregistrements existants dans Grist.
    - updated_fields (dict): Les champs mis à jour depuis l'Excel.
    - columns (list): Les colonnes disponibles dans Grist.

    Returns:
    - dict: Payload formaté pour les mises à jour.
    """
    records_to_update = []

    for record_id, updates in updated_fields.items():
        # Récupérer les valeurs actuelles de l'enregistrement
        existing_record = next((rec for rec in existing_records if rec["id"] == record_id), None)
        if not existing_record:
            continue  # Si l'enregistrement n'existe pas, on le saute

        # Compléter les valeurs manquantes avec les données existantes
        fields = {}
        for col in columns:
            col_id = col["id"]
            fields[col_id] = updates.get(col_id, existing_record["fields"].get(col_id))

        # Ajouter au payload
        records_to_update.append({"id": record_id, "fields": fields})

    return records_to_update


def get_additions_and_updates(new_records, existing_records, column_ids, duplicate_check_attribute, current_date):
    """Compare les données pour déterminer les ajouts et les mises à jour."""
    additions = []
    updates = []

    for new_record in new_records:
        matching_record = next(
            (record for record in existing_records if record.get(duplicate_check_attribute) == new_record.get(duplicate_check_attribute)),
            None
        )

        if matching_record:
            updated_fields = {}
            for column in column_ids:
                existing_value = matching_record.get(column)
                new_value = new_record.get(column)

                if existing_value is None or existing_value == "":
                    updated_fields[column] = new_value
                elif new_value != existing_value:
                    updated_fields[column] = new_value

            # Ajouter la date d'importation
            updated_fields["Date_de_transmission_donnees_MDPH"] = current_date

            if updated_fields:
                updates.append({"id": matching_record["id"], "fields": updated_fields})
        else:
            # Ajouter la date pour les nouveaux enregistrements
            new_record["Date_de_transmission_donnees_MDPH"] = current_date
            additions.append(new_record)

    return additions, updates
