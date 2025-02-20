from src.grist_api import fetch_existing_records, list_columns, add_data_to_table, update_records

def get_grist_data(doc_id, table_id):
    """
    Récupère les enregistrements et colonnes existantes dans Grist.
    """
    existing_records = fetch_existing_records(doc_id, table_id)
    columns = list_columns(doc_id, table_id)
    column_ids = [col['id'] for col in columns]

    return existing_records, column_ids

def push_to_grist(doc_id, table_id, additions, updates):
    """
    Ajoute et met à jour les enregistrements dans Grist.
    """
    if additions:
        add_data_to_table(doc_id, table_id, additions)
        print(f"Ajout des enregistrements réussi")

    if updates:
        update_records(doc_id, table_id, updates)
        print(f"Mise à jour des enregistrements réussie")