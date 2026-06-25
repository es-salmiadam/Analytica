import pandas as pd
import os

# Chemin des fichiers
data_path = r"c:\Users\Lenovo\Desktop\PFE101\data\Processed"

# Fichiers à traiter
files = {
    'sentiment_combined.csv': 'Sentiment_Score',
    'sentiment_per_day.csv': 'avg_sentiment',
    'forecast_sentiment.csv': 'Sentiment_Score'
}

for filename, col_name in files.items():
    filepath = os.path.join(data_path, filename)
    
    # Lire le fichier
    df = pd.read_csv(filepath)
    
    print(f"\n{filename}:")
    
    # Ajouter une colonne d'index unique pour chaque ligne
    df.insert(0, 'UniqueID', range(1, len(df) + 1))
    
    print(f"  Lignes: {len(df)}")
    print(f"  Colonne UniqueID ajoutée")
    print(f"  Doublons sentiment: {df[col_name].duplicated().sum()}")
    print(f"  Doublons UniqueID: {df['UniqueID'].duplicated().sum()}")
    print(f"  Moyenne sentiment: {df[col_name].mean():.6f}")
    
    # Sauvegarder le fichier
    df.to_csv(filepath, index=False)
    print(f"  ✅ Fichier sauvegardé!")

print("\n" + "="*60)
print("✅ SOLUTION APPLIQUÉE!")
print("   - Colonne UniqueID ajoutée")
print("   - Power BI acceptera les données")
print("="*60)
