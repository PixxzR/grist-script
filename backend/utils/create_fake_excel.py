import pandas as pd

def create_fake_excel(file_path):
    """
    Crée un faux fichier Excel avec des données simulées.
    """
    # Données fictives
    data = {
        "Nom": ["Alice", "Bob2", "Charlie", "Diana", "Eve"],
        "Age": [25, 30, 35, 40, 45],
        "Ville": ["Pari", "Lyon", "Marseille", "Toulouse", "Bordeaux"]
    }

    # Convertir en DataFrame
    df = pd.DataFrame(data)

    # Sauvegarder au format Excel
    df.to_excel(file_path, index=False, engine="openpyxl")
    print(f"Fichier Excel créé : {file_path}")

# Chemin du fichier Excel
output_file = "fake_data.xlsx"
create_fake_excel(output_file)