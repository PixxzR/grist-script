from datetime import datetime

def process_records(new_records, existing_records, column_ids, duplicate_check_attribute):
    """
    Compare les données Excel et Grist, et génère les enregistrements à ajouter ou mettre à jour.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    additions = []
    updates = []

    for new_record in new_records:
        matching_record = next(
            (record for record in existing_records if record.get(duplicate_check_attribute) == new_record.get(duplicate_check_attribute)),
            None
        )

        if matching_record:
            updated_fields = {}
            for column in column_ids:
                existing_value = matching_record.get(column)
                new_value = new_record.get(column)

                if existing_value is None or existing_value == "":
                    updated_fields[column] = new_value
                elif new_value != existing_value:
                    updated_fields[column] = new_value

            updated_fields["Date de transmission données MDPH"] = current_date

            if updated_fields:
                updates.append({"id": matching_record["id"], "fields": updated_fields})
        else:
            new_record["Date de transmission données MDPH"] = current_date
            additions.append(new_record)

    return additions, updates