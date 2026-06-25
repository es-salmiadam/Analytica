import pandas as pd
import os

# Chemin des fichiers
data_path = r"c:\Users\Lenovo\Desktop\PFE101\data\Processed"

# Fenêtre de lissage (moving average)
WINDOW_SIZE = 7  # 7 jours pour un lissage élégant

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
    print(f"  Nombre de lignes: {len(df)}")
    
    # Appliquer une moyenne mobile pour un lissage élégant
    # Utiliser 'centered' pour centrer la fenêtre
    df[col_name] = df[col_name].rolling(
        window=WINDOW_SIZE, 
        center=True, 
        min_periods=1
    ).mean()
    
    # Limiter entre -1 et 1 pour garder la validité
    df[col_name] = df[col_name].clip(-1, 1)
    
    # Sauvegarder le fichier
    df.to_csv(filepath, index=False)
    print(f"  ✅ Lissage appliqué (fenêtre: {WINDOW_SIZE} jours)")
    print(f"  ✅ Fichier sauvegardé!")

print("\n" + "="*60)
print("✨ OPTIMISATION VISUELLE TERMINÉE!")
print("   - Lissage appliqué sur 7 jours")
print("   - Courbe plus fluide et élégante")
print("   - Prêt pour la présentation!")
print("   Action: Rafraîchissez Power BI pour voir le résultat")
print("="*60)
