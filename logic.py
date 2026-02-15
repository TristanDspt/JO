import streamlit as st
import pandas as pd
import json


# --- PARTIE LOGIQUE / PANDAS ---

@st.cache_data

def load_and_process():
    # Chargement du JSON
    with open('jo_metadata.json', 'r', encoding='utf-8') as f:
        config_jo = json.load(f)

    # Chargement du Excel
    xls = pd.ExcelFile("medals.xlsx")

    # Boucle de chargement Excel
    all_data = []

    for sheet in xls.sheet_names:
        df_tmp = pd.read_excel(xls, sheet_name=sheet)
        
        # On split le nom de ta feuille (ex: "2024_Ete")
        saison, annee = sheet.split('_')
        
        # On va chercher l'info : config_jo["Ete"]["2024"]
        # .get() permet d'éviter un crash si l'année n'existe pas dans le JSON
        info = config_jo.get(saison, {}).get(annee, {"ville": "Inconnue", "pays": "Inconnu"})
        
        df_tmp['Année'] = annee
        df_tmp['Saison'] = saison
        df_tmp['Ville'] = info['ville']
        df_tmp['Pays Hôte'] = info['pays']
        
        all_data.append(df_tmp)

    df = pd.concat(all_data, ignore_index=True)

    # Valeur des médailles
    gold, silver, bronze = 3, 2, 1
    df['Points'] = (df.Or * gold) + (df.Argent * silver) + (df.Bronze * bronze)

    return df