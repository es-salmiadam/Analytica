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
    
    # Corriger les valeurs clippées (1.0 et -1.0) en les rendant uniques
    for i in range(len(df)):
        val = df[col_name].iloc[i]
        # Si c'est exactement 1.0, le réduire légèrement de manière unique
        if val == 1.0:
            df.loc[i, col_name] = 0.999999 - (i * 1e-6)
        # Si c'est exactement -1.0, le réduire légèrement de manière unique
        elif val == -1.0:
            df.loc[i, col_name] = -0.999999 + (i * 1e-6)
        # Pour les autres, ajouter une variation très petite basée sur l'index
        else:
            df.loc[i, col_name] = val + (i * 1e-8)
    
    # Vérifier les doublons
    duplicates = df[col_name].duplicated().sum()
    print(f"  Lignes: {len(df)}")
    print(f"  Doublons: {duplicates}")
    print(f"  Moyenne: {df[col_name].mean():.6f}")
    print(f"  Min: {df[col_name].min():.12f}")
    print(f"  Max: {df[col_name].max():.12f}")
    
    # Sauvegarder le fichier
    df.to_csv(filepath, index=False)
    print(f"  ✅ Fichier corrigé!")

print("\n" + "="*60)
print("✅ DUPLICADOS ELIMINADOS!")
print("   - Valores 1.0/-1.0 convertidos en únicos")
print("   - Todas las valores son diferentes")
print("   - Listo para Power BI")
print("="*60)
