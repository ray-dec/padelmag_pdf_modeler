import pdfplumber
import os
import re

def extract_data_from_tables(pdf_path):
    """ Extraire les données de toutes les tables dans le PDF. """
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                all_tables.extend(table[1:])  # Ignorer les en-têtes de chaque tableau
    return all_tables
