import json
import os
import psycopg2
from kafka import KafkaConsumer
from datetime import datetime

# Configuration
KAFKA_SERVER = 'kafka:9092'
TOPIC_NAME = 'manga_raw'
RAW_PATH = '../data_lake/raw/'
DB_CONFIG = {
    "host": "postgres",
    "database": "manga_db",
    "user": "manga",
    "password": "manga12"
}


def archive_to_datalake(items):
    """Sauvegarde un lot de données en JSON Lines compressé ou brut"""
    os.makedirs(RAW_PATH, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{RAW_PATH}batch_{timestamp}.jsonl"

    with open(filename, "a", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"--- [ARCHIVAGE] {len(items)} items sauvegardés dans {filename}")


def insert_to_postgres(items):
    """Insère les données nettoyées dans Postgres"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        for item in items:
            # Exemple simple : adapte selon tes colonnes Scrapy
            cur.execute(
                "INSERT INTO mangas (title, url, created_at) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                (item.get('title'), item.get('url'), datetime.now())
            )
        conn.commit()
        cur.close()
        conn.close()
        print(f"--- [POSTGRES] {len(items)} items insérés")
    except Exception as e:
        print(f"Erreur Postgres: {e}")


# Initialisation du Consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_SERVER],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='manga_archiver_group'
)

print("--- Consumer démarré. En attente de données...")

batch = []
BATCH_SIZE = 10  # On attend d'avoir 10 items avant d'écrire sur disque/DB

for message in consumer:
    item = message.value
    batch.append(item)

    if len(batch) >= BATCH_SIZE:
        archive_to_datalake(batch)
        insert_to_postgres(batch)
        batch = []  # On vide le tampon
