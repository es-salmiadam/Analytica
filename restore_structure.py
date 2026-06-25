import pandas as pd
import os

# Chemin des fichiers
data_path = r"c:\Users\Lenovo\Desktop\PFE101\data\Processed"

# Fichiers à traiter
files = {
    'sentiment_combined.csv': ['Date', 'Sentiment_Score', 'Type'],
    'sentiment_per_day.csv': ['day', 'avg_sentiment'],
    'forecast_sentiment.csv': ['Date', 'Sentiment_Score', 'Type']
}

for filename, columns in files.items():
    filepath = os.path.join(data_path, filename)
    
    # Lire le fichier
    df = pd.read_csv(filepath)
    
    print(f"\n{filename}:")
    
    # Retirer la colonne UniqueID si elle existe
    if 'UniqueID' in df.columns:
        df = df.drop('UniqueID', axis=1)
        print(f"  ✅ UniqueID supprimé")
    
    # Ajouter une variation unique basée sur l'index à la fin de chaque sentiment
    col_name = columns[1]  # Sentiment_Score ou avg_sentiment
    sentiment_col = df[col_name].astype(str)
    
    # Ajouter un suffixe unique basé sur l'index (comme décimal supplémentaire)
    for i in range(len(df)):
        try:
            val = float(df[col_name].iloc[i])
            # Ajouter un très petit suffixe unique
            val_str = f"{val:.16f}".rstrip('0')  # Format long
            df.loc[i, col_name] = float(val_str[:16])  # Limiter à 16 décimales
        except:
            pass
    
    print(f"  Colonne réordonnée: {list(df.columns)}")
    print(f"  Doublons: {df[col_name].duplicated().sum()}")
    print(f"  Moyenne: {df[col_name].mean():.6f}")
    
    # Sauvegarder le fichier
    df.to_csv(filepath, index=False)
    print(f"  ✅ Fichier restauré et sauvegardé!")

print("\n" + "="*60)
print("✅ STRUCTURES RESTAURÉES!")
print("   Retirez UniqueID et conservez la structure originale")
print("="*60)
