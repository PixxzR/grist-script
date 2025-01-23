def filter_new_records(existing_records, new_records, unique_keys):
    """
    Filtre les enregistrements pour éviter les doublons.

    Parameters:
    - existing_records (list): Liste des enregistrements existants dans la table.
    - new_records (list): Liste des nouveaux enregistrements à ajouter.
    - unique_keys (list): Liste des colonnes à utiliser pour identifier les doublons.

    Returns:
    - List des enregistrements non doublons.
    """
    filtered_records = []
    existing_key_set = {
        tuple(record[key] for key in unique_keys) for record in existing_records
    }

    for record in new_records:
        record_key = tuple(record.get(key) for key in unique_keys)
        if record_key not in existing_key_set:
            filtered_records.append(record)

    return filtered_records