import pandas as pd

def save_to_parquet(df, filepath,columns):
    df = df[columns]
    df.to_parquet(filepath,index=False)
    print(f"Les données ont été sauvegardées dans {filepath}")
