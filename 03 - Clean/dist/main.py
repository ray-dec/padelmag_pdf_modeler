import os
import pandas as pd
import re, os, sys

# Chemin vers les scripts spécifiques au projet
project_path = './'

# Convertir en chemin absolu (utile si le script est exécuté dans différents environnements)
absolute_path = os.path.abspath(project_path)

# Vérifier si le chemin existe déjà dans sys.path pour éviter les doublons
if absolute_path not in sys.path:
    # Ajouter le chemin au début de sys.path
    sys.path.insert(0, absolute_path)

from Scripts.extract import extract_data_from_tables,download_pdf_padel
from Scripts.transform import extract_date_and_sex, create_timestamp_gender_columns, header_and_data_cleansing
from Scripts.load import save_to_parquet


def main() :

    folder_path ='./02 - WIP/'    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    dataframes = []

    schema_type = ['rang', 'nom', 'prenom', 'nationalité', 'n° licence', 'points', 'assimilation', 'nombre de tournois joues', 'ligue', 'code club', 'club','sexe','date']
    download_pdf_padel('DAMES',folder_path)
    download_pdf_padel('MESSIEURS', folder_path)

    for filename in os.listdir(folder_path):

        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)

            if os.path.exists(folder_path+'raw/'+filename):
                os.remove(file_path)
                print(f'Le fichier {filename} a déjà été intégré.\n')

            else :        
                print(f"Traitement du fichier {filename}.\nVeuillez patienter... Ne quittez pas l'application !\n")

                # Extraction depuis les fichiers PDFs 
                all_tables = extract_data_from_tables(file_path)
                print("Fin de l'extraction des données depuis le PDF. \nLancement du cleaning...\n")

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

                if not os.path.exists(folder_path+'raw/'):
                    os.makedirs(folder_path+'raw/', exist_ok=True)
                print(f"Fin du cleaning. Le fichier PDF a été archivé dans {folder_path+'raw/'}\n")
                os.replace(file_path,folder_path+'raw/'+filename)
    
    
    database = pd.read_parquet(folder_path+'database.parquet')
    dataframes.append(database)
    final_df = pd.concat(dataframes, ignore_index=True)
    final_df.drop_duplicates(inplace=True)

    # Chargement final dans le fichier dédié
    output_filepath = folder_path+'database.parquet'
    save_to_parquet(final_df, output_filepath,schema_type)
    print("\n Vous pouvez à présent fermer l'application.")

if __name__ == "__main__":
    main()