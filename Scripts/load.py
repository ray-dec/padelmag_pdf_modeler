import pandas as pd

def save_to_parquet(df, filepath,columns):
    df = df[columns]
    df = df.astype('string')
    df.to_parquet(filepath,index=False)
    print(f"Fin du chargement, Le traitement est terminé et les données prêtes à être exploitées.\nLes données ont été sauvegardées à l'emplacement suivant : {filepath}")
