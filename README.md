# Manga Data Platform

## Overview

**Manga Data Platform** est une plateforme de données conçue pour collecter, traiter et analyser des informations sur les mangas provenant de plusieurs sites web.

Le projet implémente une architecture **Data Engineering moderne** intégrant :

* Scraping de données
* Streaming de données
* Traitement Big Data
* Data Warehouse
* Machine Learning
* API de recommandation

L'objectif est de construire un système capable d'aider les utilisateurs à découvrir les meilleurs mangas selon leurs préférences, tout en produisant des statistiques et analyses avancées.

---

# Architecture

Le système suit une architecture orientée **Data Pipeline**.

```
Websites
   │
   ▼
Scrapy (Data Ingestion)
   │
   ▼
Kafka (Streaming)
   │
   ▼
Spark (Data Processing)
   │
   ▼
PostgreSQL (Data Warehouse)
   │
   ▼
Machine Learning (MLflow)
   │
   ▼
API (FastAPI)
   │
   ▼
Frontend / Dashboard
```

---

# Project Structure

```
manga-data-platform/

ingestion/
   scrapy_project/

streaming/
   kafka_producer.py
   kafka_consumer.py

data_lake/
   raw/
   processed/

processing/
   spark_jobs/
      clean_data.py
      transform_data.py

warehouse/
   postgres_schema.sql
   load_data.py

ml/
   feature_engineering.py
   training.py
   recommendation_model.py

api/
   main.py
   routes/
      manga_routes.py
      stats_routes.py
      recommendation_routes.py

analytics/
   statistics.py
   ranking.py

orchestration/
   airflow_dags/

frontend/
   dashboard/

docker/
   docker-compose.yml
```

---

# Data Pipeline

Le pipeline de données est composé de plusieurs étapes.

## 1. Data Ingestion

Les données sont collectées via des scrapers développés avec **Scrapy**.

Sources :

* SensCritique
* Topito
* autres sites manga

Les données collectées incluent :

* titre du manga
* genre
* note
* popularité
* source

Les données brutes sont stockées dans le **Data Lake**.

```
data_lake/raw/
```

---

## 2. Streaming

Les données scrapées sont envoyées vers **Apache Kafka**.

Chaque manga devient un message dans un topic Kafka.

Exemple :

```
{
  "title": "Dragon Ball",
  "rating": 8.4,
  "source": "senscritique",
  "scraped_at": "2026-03-16"
}
```

---

## 3. Data Processing

Les données sont traitées avec **Apache Spark**.

Traitements :

* nettoyage des données
* suppression des doublons
* normalisation des genres
* transformation des types de données

Les données nettoyées sont stockées dans :

```
data_lake/processed/
```

---

## 4. Data Warehouse

Les données nettoyées sont chargées dans **PostgreSQL** pour les analyses.

Structure simplifiée :

```
mangas
genres
sources
ratings
```

---

## 5. Machine Learning

Les données sont utilisées pour entraîner des modèles de recommandation.

Les expériences sont suivies avec **MLflow**.

Objectifs :

* recommander des mangas
* prédire la popularité
* analyser les tendances

---

## 6. API

Une API développée avec **FastAPI** permet d'exposer les données.

Exemples d'endpoints :

```
GET /mangas
GET /top-mangas
GET /statistics
GET /recommendations
```

---

## 7. Dashboard

Un tableau de bord permettra de visualiser :

* les mangas les plus populaires
* les tendances par genre
* les statistiques de popularité
* les recommandations

---

# Orchestration

Les pipelines sont orchestrés avec **Apache Airflow**.

Exemple de workflow :

```
scrape_sites
   ↓
send_to_kafka
   ↓
spark_cleaning
   ↓
load_postgres
   ↓
train_model
   ↓
generate_statistics
```

---

# Infrastructure

L'infrastructure est déployée avec **Docker**.

Services :

* Kafka
* Zookeeper
* Spark
* PostgreSQL
* Airflow
* MLflow
* API

---

# Future Improvements

* Ajout de nouvelles sources de données
* Amélioration du système de recommandation
* Analyse des tendances des mangas
* Interface utilisateur avancée
* Recherche intelligente

---

# Technologies Used

* Python
* Scrapy
* Apache Kafka
* Apache Spark
* PostgreSQL
* Apache Airflow
* MLflow
* Docker
* FastAPI

---

# Goal of the Project

Créer une plateforme capable de :

* centraliser les données sur les mangas
* produire des analyses et statistiques
* recommander les meilleurs mangas aux utilisateurs
* démontrer une architecture data moderne.
