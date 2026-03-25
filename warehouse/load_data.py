import pandas as pd
from sqlalchemy import create_engine
import os

DB_URL = "postgresql://manga:manga12@postgres:5432/manga_db"
PROCESSED_PATH = "/app/data_lake/processed/mangas_cleaned"

def load_to_warehouse():
    print("--- [WAREHOUSE] Début du chargement vers Postgres...")
    
    # 1. Vérifier si le dossier Spark existe
    if not os.path.exists(PROCESSED_PATH):
        print(f"Erreur : Le dossier {PROCESSED_PATH} est introuvable. Lancez le job Spark d'abord.")
        return

    try:
        # 2. Lire les fichiers Parquet générés par Spark
        # Pandas lit directement tout le dossier Parquet
        df = pd.read_parquet(PROCESSED_PATH)
        
        if df.empty:
            print("Aucune donnée à charger.")
            return

        # 3. Connexion à Postgres
        engine = create_engine(DB_URL)

        # 4. Insertion dans la table 'mangas'
        # if_exists='append' : ajoute les données à la suite
        # method='multi' : optimisation pour l'insertion de masse
        df.to_sql('mangas', engine, if_exists='append', index=False, method='multi')
        
        print(f"--- [WAREHOUSE] Succès : {len(df)} mangas chargés dans la DB.")

    except Exception as e:
        print(f"Erreur lors du chargement : {e}")

if __name__ == "__main__":
    load_to_warehouse()
