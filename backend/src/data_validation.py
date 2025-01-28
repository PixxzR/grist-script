def filter_new_records(existing_records, new_records, duplicate_check_attribute, duplicate_method):
    """
    Filtre ou gère les doublons en fonction de la configuration.

    Parameters:
    - existing_records (list): Liste des enregistrements existants dans la table.
    - new_records (list): Liste des nouveaux enregistrements à ajouter.
    - duplicate_check_attribute (str): Colonne utilisée pour identifier les doublons.
    - duplicate_method (str): Méthode de gestion des doublons.

    Returns:
    - List des enregistrements à ajouter.
    - List des enregistrements à mettre à jour.
    """
    if not duplicate_check_attribute:
        # Si aucun attribut n'est défini, retourne tout en tant que nouveaux enregistrements
        return new_records, []

    updates = []
    additions = []

    # Index des enregistrements existants par l'attribut de duplication
    existing_map = {str(record[duplicate_check_attribute]): record for record in existing_records}

    for record in new_records:
        key = str(record.get(duplicate_check_attribute))

        if key in existing_map:
            # Prépare un enregistrement pour la mise à jour
            existing_record = existing_map[key]
            update_fields = {}

            # Compare les champs pour identifier les différences
            for field, value in record.items():
                if value and (field not in existing_record or existing_record[field] != value):
                    update_fields[field] = value

            if update_fields:
                updates.append({"id": existing_record["id"], "fields": update_fields})
        else:
            # Nouvel enregistrement à ajouter
            additions.append(record)

    return additions, updates