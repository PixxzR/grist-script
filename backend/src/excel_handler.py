import pandas as pd

def read_and_validate_excel(file, required_columns):
    """
    Lit un fichier Excel et valide la présence des colonnes requises.
    """
    df = pd.read_excel(file, header=1)  # On suppose que la 2e ligne contient les en-têtes correctes
    df = df.dropna(how="all")  # Supprime les lignes entièrement vides

    columns_in_excel = df.columns.tolist()
    missing_columns = [col for col in required_columns if col not in columns_in_excel]

    if missing_columns:
        raise ValueError(f"Colonnes manquantes : {', '.join(missing_columns)}")

    return df