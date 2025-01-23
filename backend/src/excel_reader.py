import pandas as pd

def read_and_validate_excel(file_path):
    """
    Lit un fichier Excel et retourne les données.
    """
    try:
        data = pd.read_excel(file_path)
        print(f"Fichier Excel chargé : {len(data)} lignes trouvées.")
        return data
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier Excel : {e}")
        raise