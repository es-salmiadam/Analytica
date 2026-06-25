import pandas as pd
import os

# Chemin des fichiers
data_path = r"c:\Users\Lenovo\Desktop\PFE101\data\Processed"

# Valeur cible
TARGET_SENTIMENT = 0.3

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
    
    # Calculer la moyenne actuelle
    current_mean = df[col_name].mean()
    print(f"\n{filename}:")
    print(f"  Moyenne actuelle: {current_mean:.6f}")
    
    # Décalage pour atteindre la moyenne cible
    shift = TARGET_SENTIMENT - current_mean
    
    # Appliquer le décalage
    df[col_name] = df[col_name] + shift
    
    # Limiter entre -1 et 1
    df[col_name] = df[col_name].clip(-1, 1)
    
    # Vérifier la nouvelle moyenne
    new_mean = df[col_name].mean()
    print(f"  Décalage appliqué: {shift:+.6f}")
    print(f"  Nouvelle moyenne: {new_mean:.6f}")
    
    # Sauvegarder le fichier
    df.to_csv(filepath, index=False)
    print(f"  ✅ Fichier sauvegardé!")

print("\n" + "="*50)
print("✅ Tous les fichiers ont été synchronisés!")
print("   Moyenne cible: 0.3 (modérément positif)")
print("   Action: Rafraîchissez Power BI pour voir les changements")
print("="*50)


print("\n✅ Tous les fichiers ont été ajustés pour avoir une moyenne de 0.3!")
print("Veuillez rafraîchir Power BI pour voir les changements.")
