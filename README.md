# Padelmag PDF Modeler

## Description
Le projet "Padelmag PDF Modeler" est conçu pour extraire, transformer, et charger des données à partir de fichiers PDF. 
Ces données sont ensuite chargés dans Power BI pour l'analyse.

L'ensemble des PDFs présent dans ce projet sont open-sources,  sourcés par l'organisme FFT responsable des classements de joueurs de padel français à l'adresse suivante : 

https://padelmagazine.fr/classement-padel/

## Scripts
- `extract.py` : Extrait des données depuis les fichiers PDF en utilisant `pdfplumber`.
- `load.py` : Charge les données extraites dans une structure utilisable, probablement un DataFrame pandas.
- `main.py` : Script principal qui orchestre le processus d'extraction, de transformation et de chargement des données.
- `transform.py` : Transforme les données extraites, possiblement en les nettoyant ou en les restructurant.

## Installation
Pour installer et configurer le projet, suivez ces étapes :
pip install -r requirements.txt
Exécutez ensuite le script `main.py`. Assurez-vous que les fichiers PDF nécessaires sont correctement placés.
L'ensemble des fichiers sont stockés par années par défaut sous ~/./01 - Raw
