import re
import pandas as pd
import os
from unidecode import unidecode

def extract_date_and_sex(filename):
    # Convertir le nom du fichier en majuscules pour faciliter la correspondance
    filename_upper = unidecode(filename.upper())

    # Dictionnaire pour convertir le mois en chiffre
    month_to_number = {
        'JANVIER': '01', 'FEVRIER': '02', 'MARS': '03', 'AVRIL': '04',
        'MAI': '05', 'JUIN': '06', 'JUILLET': '07', 'AOUT': '08',
        'SEPTEMBRE': '09', 'OCTOBRE': '10', 'NOVEMBRE': '11', 'DECEMBRE': '12'
    }

    # Trouver le mois et l'année dans le nom du fichier
    month_number = 'Inconnu'
    year = 'Inconnu'
    for month in month_to_number:
        if unidecode(month) in filename_upper:
            month_number = month_to_number[month]
            # Recherche de l'année après le mois
            month_year_pattern = month + r'[\s_-]*(20\d{2})'
            year_match = re.search(month_year_pattern, filename_upper)
            if year_match:
                year = year_match.group(1)
            break

    # Format final de la date
    final_date = f"{month_number}-{year}" if month_number != 'Inconnu' and year != 'Inconnu' else 'Date Inconnue'

    # Déterminer le sexe
    sex = 'Female' if 'DAMES' in filename_upper else 'Male' if 'MESSIEURS' in filename_upper else 'Inconnu'

    return final_date, sex

def create_timestamp_gender_columns(df, date, sex):
  # Ajout des deux nouvelles colonnes Sex & Date 
  df['sexe'] = sex
  df['date'] = date
  
  return df

# Fonction pour vérifier si la valeur n'est pas un nombre et n'est pas vide
def is_not_number_and_not_empty(s):
    if pd.isna(s) or s == '':  # Vérifie si la valeur est NaN ou vide
        return False
    try:
        float(s)  # Tente de convertir en float
        return False
    except ValueError:
        return True


def header_and_data_cleansing(header, data):
    """
    Nettoyer les en-têtes et les données du DataFrame.

    Parameters:
        header (list): Liste des en-têtes de colonnes.
        data (list of list): Données sous forme de liste de listes.

    Returns:
        pd.DataFrame: DataFrame nettoyé.
    """
    if not header or not data:
        raise ValueError("Les en-têtes et les données ne peuvent pas être vides.")

    # Nettoyage et mise en forme des en-têtes
    cleaned_header = [col.lower().replace('n°licence','n° licence').replace('\n', ' ').replace('nb.','nombre').strip() for col in header]

    # Création du DataFrame avec des en-têtes nettoyés
    df = pd.DataFrame(data, columns=cleaned_header)
    # Conversion des colonnes en chaînes et réinitialisation de l'index
    df = df.astype(str).reset_index(drop=True)

    # Maintenant, conversion des valeurs numériques dans 'points'
    df.loc[df['points'].apply(is_not_number_and_not_empty), 'assimilation'] = df['points']
    df['points'] = pd.to_numeric(df['points'], errors='coerce', downcast='integer')
    df['points'] =  df['points'].fillna(0)
  
    df['nombre de tournois joues'] = pd.to_numeric(df['nombre de tournois joues'], errors='coerce', downcast='integer')
    df['nombre de tournois joues'] = df['nombre de tournois joues'].fillna(0)      
    
    df = df.astype({'points': 'int32','nombre de tournois joues': 'int32' }, errors='ignore')

    # Filtre sur les lignes à supprimer
    df = df[(df['nom'] != 'NOM') & (df['prenom'] != 'PRENOM') & (df['rang']!='RANG')]
    df = df.dropna(subset=['n° licence'])

    return df