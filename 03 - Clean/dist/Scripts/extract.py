import pdfplumber
import os
import re
import urllib3
import urllib.request
from bs4 import BeautifulSoup
import requests

def download_pdf_padel(categorie,folder_path):
    urllib3.disable_warnings()
    url_page = 'https://www.fft.fr/competition/padel/le-classement-padel'
    response = requests.get(url_page,verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for a in soup.find_all('a', href=True):
        if categorie in a['href']:
            filename = a.get_text(strip=True) + '.pdf'
            try:
                urllib.request.urlretrieve(a['href'], folder_path+filename)
                print(f'Le fichier {filename} a bien été téléchargé depuis le site {url_page}\n')
            except Exception as e:
                print(f"Erreur lors du téléchargement : {e}")
            break

def extract_data_from_tables(pdf_path):
    """ Extraire les données de toutes les tables dans le PDF. """
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                all_tables.extend(table[1:])  # Ignorer les en-têtes de chaque tableau
    return all_tables
