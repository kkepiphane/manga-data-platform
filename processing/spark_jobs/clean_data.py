from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, trim, current_timestamp, to_date

# 1. Initialisation de la session Spark
spark = SparkSession.builder \
    .appName("MangaDataCleaning") \
    .getOrCreate()


def clean_manga_data():
    print("--- [SPARK] Démarrage du nettoyage des données...")

    # 2. Lecture des données brutes (JSON Lines) depuis le Data Lake
    # Spark peut lire tout le dossier d'un coup
    raw_df = spark.read.json("../../data_lake/raw/*.jsonl")

    # 3. Nettoyage et Transformation
    # - On supprime les doublons basés sur l'URL
    # - On nettoie le titre (minuscules, sans espaces inutiles)
    # - On ajoute une colonne de date de processing
    cleaned_df = raw_df.dropDuplicates(["url"]) \
        .withColumn("title_clean", trim(lower(col("title")))) \
        .withColumn("processed_at", current_timestamp()) \
        .filter(col("title").isNotNull())  # On vire les données vides

    # 4. Affichage d'un aperçu pour le debug
    cleaned_df.show(5)

    # 5. Écriture dans la zone 'processed' au format Parquet
    # Le format Parquet est compressé et ultra-rapide pour les analyses futures
    output_path = "../../data_lake/processed/mangas_cleaned"

    cleaned_df.write.mode("overwrite").parquet(output_path)

    print(
        f"--- [SPARK] Nettoyage terminé. Données sauvegardées dans : {output_path}")


if __name__ == "__main__":
    clean_manga_data()
    spark.stop()
