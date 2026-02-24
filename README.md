Analyse Big Data de tweets (Kafka, Spark, Hadoop)

Ce projet de PFE met en place une architecture Big Data pour analyser des données de réseaux sociaux et extraire des indicateurs sur les tendances et l’opinion des utilisateurs.​
Objectifs du projet

    Simuler ou consommer un flux de tweets via un dataset public (Kaggle).​

    Ingestion des données en temps réel (ou quasi temps réel) avec Apache Kafka.​

    Stockage des données brutes et préparées dans Hadoop / HDFS.​

    Traitement et analyse des données avec Apache Spark (prétraitement texte, agrégations, indicateurs de sentiment).​

    Création de tableaux de bord interactifs (par exemple avec Tableau) pour visualiser volumes, engagement et sentiment dans le temps.​

Fonctionnalités principales

    Pipeline complet de bout en bout : collecte → ingestion Kafka → stockage HDFS → traitement Spark → visualisation.​

    Nettoyage et préparation des tweets (URLs, mentions, stopwords, normalisation).​

    Analyses descriptives (tweets par période, top hashtags/mots-clés, métriques d’engagement).​

    Première analyse de sentiment simple (positif / négatif / neutre ou score).​

Stack technique

    Langage : Python (pour le traitement et les scripts).​

    Ingestion : Apache Kafka.​

    Traitement : Apache Spark (batch / streaming selon le scénario).​

    Stockage : Hadoop / HDFS.​

    Visualisation : PowerBI
