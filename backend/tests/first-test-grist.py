import requests

# Clé API
API_KEY = "1a5fb3dea181506cbac174e8f0c5dd446e6bf021"
BASE_URL = "https://docs.getgrist.com/api"

# Headers pour authentification
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Tester l'API pour lister les organisations
def list_orgs():
    url = f"{BASE_URL}/orgs"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lève une exception pour les erreurs HTTP
        orgs = response.json()
        print("Liste des organisations :")
        for org in orgs:
            print(f"- ID : {org['id']}, Nom : {org['name']}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")

if __name__ == "__main__":
    list_orgs()