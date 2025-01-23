def filter_new_records(existing_records, new_records, duplicate_check_attribute, duplicate_method):
    """
    Filtre ou gère les doublons en fonction de la configuration.

    Parameters:
    - existing_records (list): Liste des enregistrements existants dans la table.
    - new_records (list): Liste des nouveaux enregistrements à ajouter.
    - duplicate_check_attribute (str): Colonne utilisée pour identifier les doublons.
    - duplicate_method (str): Méthode de gestion des doublons.

    Returns:
    - List des enregistrements à ajouter (sans doublons).
    """
    if not duplicate_check_attribute:
        # Si aucun attribut n'est défini, renvoie tous les enregistrements.
        return new_records

    # Construire un ensemble des valeurs existantes pour l'attribut spécifié
    # Convertir en chaînes pour uniformiser les types
    existing_keys = {str(record.get(duplicate_check_attribute)) for record in existing_records}

    filtered_records = []

    for record in new_records:
        # Convertir la clé de l'enregistrement en chaîne pour comparaison
        key = str(record.get(duplicate_check_attribute))

        if key in existing_keys:
            # La logique est la même pour toutes les méthodes : exclure les doublons.
            if duplicate_method in ["overwrite", "sum", "replace"]:
                continue  # Ne pas ajouter le doublon
        else:
            # Ajouter l'enregistrement s'il n'est pas un doublon
            filtered_records.append(record)

    return filtered_records