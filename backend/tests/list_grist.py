import requests

# Configuration de l'API
API_KEY = "1a5fb3dea181506cbac174e8f0c5dd446e6bf021"
BASE_URL = "https://docs.getgrist.com/api"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def list_orgs():
    """
    Liste toutes les organisations auxquelles l'utilisateur a accès.
    """
    url = f"{BASE_URL}/orgs"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        orgs = response.json()
        return orgs
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des organisations : {e}")
        return []

def list_workspaces(org_id):
    """
    Liste tous les workspaces d'une organisation spécifique.
    """
    url = f"{BASE_URL}/orgs/{org_id}/workspaces"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        workspaces = response.json()
        return workspaces
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des workspaces : {e}")
        return []

def list_documents(workspace_id):
    """
    Liste tous les documents dans un workspace spécifique.
    """
    url = f"{BASE_URL}/workspaces/{workspace_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        workspace_details = response.json()
        return workspace_details.get("docs", [])
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des documents : {e}")
        return []

def list_tables(doc_id):
    """
    Liste toutes les tables d'un document spécifique.
    Retourne une liste de tables avec leurs IDs.
    """
    url = f"{BASE_URL}/docs/{doc_id}/tables"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    # La clé "tables" contient la liste des tables
    return response.json().get("tables", [])  
  
def list_columns(doc_id, table_id, include_hidden=False):
    """
    Liste les colonnes d'une table spécifique dans un document.
    
    Parameters:
    - doc_id (str): L'ID du document (UUID).
    - table_id (str): L'ID ou le nom normalisé de la table.
    - include_hidden (bool): Inclure les colonnes cachées si True.
    
    Returns:
    - List[dict]: Une liste de colonnes avec leurs ID et champs associés.
    """
    url = f"{BASE_URL}/docs/{doc_id}/tables/{table_id}/columns"
    params = {"hidden": str(include_hidden).lower()}  # Convertir booléen en string 'true' ou 'false'

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        # La réponse contient une clé "columns"
        return response.json().get("columns", [])
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des colonnes : {e}")
        return []
    
def main():
    # Étape 1 : Lister les organisations
    orgs = list_orgs()
    print("Organisations trouvées :")
    for org in orgs:
        print(f"- ID : {org['id']}, Nom : {org['name']}")
        org_id = org["id"]

        # Étape 2 : Lister les workspaces pour chaque organisation
        workspaces = list_workspaces(org_id)
        print("  Workspaces associés :")
        for workspace in workspaces:
            print(f"  - ID : {workspace['id']}, Nom : {workspace['name']}")
            workspace_id = workspace["id"]

            # Étape 3 : Lister les documents pour chaque workspace
            documents = list_documents(workspace_id)
            print("    Documents associés :")
            for doc in documents:
                print(f"    - ID : {doc['id']}, Nom : {doc['name']}")
                doc_id = doc["id"]

                # Étape 4 : Lister les tables pour chaque document
                # tables = list_tables(doc_id)
                # print("      Tables associées :")
                # for table in tables.get("tables", []):  # Accès aux tables via la clé "tables"
                #     table_id = table.get("id", "Inconnu")
                #     # Les noms de table ne sont pas présents directement ; vous pouvez ajouter un traitement ici si nécessaire
                #     print(f"      - ID : {table_id}")

if __name__ == "__main__":
    main()