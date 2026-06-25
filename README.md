# Analyse Big Data de tweets (Spark, Hadoop, NLP & Machine Learning)

Ce projet de PFE met en place une architecture Big Data pour analyser des données de réseaux sociaux (Twitter 2022) et extraire des indicateurs sur les tendances et l opinion des utilisateurs, avec une couche de Machine Learning pour la prévision du sentiment.

## Objectifs du projet

- Ingestion et stockage de données massives de tweets dans Hadoop / HDFS.
- Traitement distribué des données brutes avec Apache Spark (nettoyage, agrégation journalière).
- Analyse NLP des contenus textuels : nettoyage (Regex), extraction des hashtags tendances, calcul du score de sentiment.
- Modélisation prédictive par séries temporelles (Holt-Winters) pour prévoir l évolution du sentiment à 30 jours.
- Création d un tableau de bord interactif Power BI pour visualiser volumes, engagement, tendances et prévisions.

## Fonctionnalités principales

- Pipeline complète de bout en bout : ingestion → stockage HDFS → traitement Spark → NLP → ML → visualisation Power BI.
- Nettoyage et préparation des tweets (suppression URLs, mentions, stopwords, emojis, normalisation).
- Analyses descriptives : tweets par période, Top 10 hashtags, métriques d engagement (likes, retweets, replies).
- Analyse de sentiment (score -1 à +1) avec TextBlob, agrégée par jour sur toute l année 2022.
- Prévision à 30 jours du sentiment par l algorithme Holt-Winters (tendance + saisonnalité hebdomadaire).
- Dashboard Power BI interactif avec filtres dynamiques, KPIs et graphique historique + prévisions sur un axe unifié.

## Stack technique

- **Langage :** Python 3.14
- **Traitement Big Data :** Apache Spark (PySpark), Hadoop / HDFS, Cloudera VM
- **NLP :** TextBlob, Regex (`re`), `collections.Counter`
- **Machine Learning :** Statsmodels — Holt-Winters (ExponentialSmoothing)
- **Manipulation de données :** Pandas, NumPy
- **Visualisation / BI :** Microsoft Power BI Desktop
- **Environnement :** Windows 11, Visual Studio Code, Jupyter Notebook

## Structure du projet

```
PFE101/
├── Notebooks/
│   └── main.ipynb                   # Pipeline NLP complète + export Power BI
├── Scripts/
│   ├── generate_forecast.py         # Prévision Holt-Winters 30 jours
│   ├── windows_ai_analysis.py       # Analyse locale : hashtags + engagement
│   ├── spark_pipeline.py            # Pipeline Spark + HDFS (Cloudera)
│   ├── vm_spark_pipeline.py         # Version allégée pour VM Cloudera
│   └── hdfs_manager.py              # Utilitaire gestion HDFS
├── data/
│   ├── Raw/dataset.csv              # Dataset brut (non versionné)
│   └── Processed/
│       ├── sentiment_per_day.csv    # Score de sentiment journalier (2022)
│       ├── sentiment_combined.csv   # Historique + prévisions → Power BI
│       ├── top_hashtags.csv         # Top 10 Hashtags
│       ├── tweets_per_day.csv       # Volume de tweets par jour
│       └── engagement_per_day.csv   # Engagement journalier
└── Dashbord.pbix                    # Tableau de bord Power BI
```

## Dataset

Collection de tweets en anglais couvrant toute l année **2022** (Janvier — Décembre), sans biais temporel.

| Caractéristique | Valeur |
|---|---|
| Source | Twitter (X) |
| Langue | Anglais |
| Période | Janvier — Décembre 2022 |
| Volume | ~547 000 enregistrements |
| Format | CSV |
| Colonnes clés | `date`, `content`, `hashtags`, `likeCount`, `retweetCount` |

> Le fichier `data/Raw/dataset.csv` n est pas versionné (volume trop important). À placer manuellement avant exécution.

## Installation et exécution

```bash
pip install pandas numpy statsmodels textblob scikit-learn matplotlib pyspark
python -m textblob.download_corpora
```

```bash
# Analyse des tendances et hashtags
python Scripts/windows_ai_analysis.py

# Pipeline NLP complète (Jupyter)
jupyter notebook Notebooks/main.ipynb

# Génération des prévisions ML
python Scripts/generate_forecast.py
```

Ouvrir `Dashbord.pbix` dans Power BI Desktop puis cliquer **Actualiser**.

## Résultats clés

| Indicateur | Valeur |
|---|---|
| Top Hashtag 2022 | #NFT (1989 occurrences) |
| Sentiment moyen annuel | +0.09 (légèrement positif) |
| Jours à sentiment négatif | ~35% |
| Jours à sentiment positif | ~65% |
| Horizon de prévision ML | 30 jours |
| Saisonnalité détectée | Hebdomadaire (7 jours) |

## Auteur

**Adam ES-SALMI** — BTS Développement en Intelligence Artificielle, Session Juin 2026  
Encadrant : Prof. Younes BELARABI
