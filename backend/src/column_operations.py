from config import BASE_URL, HEADERS
import requests

def list_and_display_columns(doc_id, table_id, include_hidden=False):
    """
    Liste et affiche les colonnes d'une table dans Grist.
    """
    url = f"{BASE_URL}/docs/{doc_id}/tables/{table_id}/columns"
    params = {"hidden": str(include_hidden).lower()}
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        columns = response.json().get("columns", [])
        print("Colonnes disponibles dans la table :")
        for col in columns:
            col_id = col["id"]
            label = col["fields"].get("label", "Sans étiquette")
            col_type = col["fields"].get("type", "Type inconnu")
            print(f"- ID : {col_id}, Label : {label}, Type : {col_type}")
        return columns
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du listing des colonnes : {e}")
        raise