import os
import pandas as pd
import pdfplumber
import re, os, sys

from extract import extract_data_from_tables
from transform import extract_date_and_sex, create_timestamp_gender_columns, header_and_data_cleansing
from load import save_to_parquet

def main(year):
    folder_path = f'/content/drive/MyDrive/02 - Work/02 - Padel Mag/01 - Raw/{year}'
    dataframes = []

    schema_type = ['rang', 'nom', 'prenom', 'nationalité', 'n° licence', 'points', 'assimilation', 'nombre de tournois joues', 'ligue', 'code club', 'club','sexe','date']

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            print(f'Traitement du fichier {filename}')
            

            # Extraction depuis les fichiers PDFs
            all_tables = extract_data_from_tables(file_path)
          
            
            # Modification des tables
            df = header_and_data_cleansing(all_tables[0], all_tables[1:])
            date, sex = extract_date_and_sex(filename)
            df = create_timestamp_gender_columns(df, date, sex)
            df =  df.reset_index(drop=True)

            for col in schema_type:
                if col not in df.columns:
                    df[col] = pd.NA
                    # Assurer l'ordre des colonnes
            
            df = df[schema_type]
            dataframes.append(df)

    final_df = pd.concat(dataframes, ignore_index=True)
    
    # Chargement final dans le fichier dédié
    output_filepath = f'/content/drive/MyDrive/02 - Work/02 - Padel Mag/02 - WIP/db_{year}.parquet'
    save_to_parquet(final_df, output_filepath,schema_type)

if __name__ == "__main__":
    main()
