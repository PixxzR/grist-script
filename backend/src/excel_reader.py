import pandas as pd

def read_and_validate_excel(file):
    """
    Lit le fichier Excel et retourne un DataFrame.
    """
    import pandas as pd

    # Lire le fichier Excel
    df = pd.read_excel(file, header=1)  # Utilise la 2ème ligne (index 1) comme en-tête
    df = df.dropna(how="all")  # Supprime les lignes complètement vides
    return df