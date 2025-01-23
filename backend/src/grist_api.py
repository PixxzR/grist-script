from config import BASE_URL, HEADERS
import requests

def create_document(workspace_id, doc_name):
    """
    Crée un nouveau document dans un espace de travail.
    """
    url = f"{BASE_URL}/workspaces/{workspace_id}/docs"
    payload = {"name": doc_name}
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.text.strip()  # Retourne l'ID du document

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
        # Transforme en un format plus facile à manipuler
        existing_data = [
            record["fields"] for record in records
        ]
        return existing_data
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des enregistrements existants : {e}")
        return []