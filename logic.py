import streamlit as st
import pandas as pd
from pycountry_convert import country_name_to_country_alpha2

# --- PARTIE LOGIQUE / PANDAS ---

# Fonction Drapeau
def get_flag_url(country_name):
    if not isinstance(country_name, str):
        return f"https://flagcdn.com/120x90/un.png"

    # Nettoyage interne (sécurité supplémentaire)
    name = country_name.replace('\xa0', '').strip()
    
    mapping = {
        # Pays actuels avec noms spécifiques
        "United States": "us",
        "Great Britain": "gb",
        "South Korea": "kr",
        "China": "cn",
        "Chinese Taipei": "tw",
        "Kosovo": "xk",
        "Netherlands": "nl",
        "Virgin Islands, US": "vi",
        "Republic of Korea": "kr", 
        "Hong Kong": "hk",
        # Entités spéciales (on utilise souvent le drapeau Olympique 'un' ou 'olympic')
        "ROC": "un", # Russie (historique récent)
        "Independent Olympic Athletes": "un",
        "Individual Neutral Athletes": "un",
        "Refugee Olympic Team": "un",
        "Mixed team": "un",
        "Unified Team": "un",
        # Pays historiques (on mappe vers le pays successeur ou ONU)
        "USSR": "ru",
        "Yugoslavia": "rs", # Serbie
        "Serbia and Montenegro": "rs",
        "Czechoslovakia": "cz", # Tchéquie
        "German Democratic Republic (Germany)": "de",
        "Netherlands Antilles": "an"
    }
    
    if name in mapping:
        code = mapping[name]
        return f"https://flagcdn.com/120x90/{code}.png"
    
    try:
        code = country_name_to_country_alpha2(name).lower()
        return f"https://flagcdn.com/120x90/{code}.png"
    except:
        return f"https://flagcdn.com/120x90/un.png"

# Chargement des données
@st.cache_data(ttl=300)
def load_and_process():
    df_histo = pd.read_csv('olympic_games.csv')
    df_histo.drop(columns='athletes', inplace=True)
    df_recent = pd.read_excel('medals.xlsx')

    # Nettoyage des espaces
    df_histo['country'] = df_histo['country'].str.strip()
    df_recent['country'] = df_recent['country'].str.replace('\xa0', '', regex=False).str.strip()

    # Mapping complet
    mapping = {
        "United States of America": "United States",
        "People's Republic of China": "China",
        "Republic of Korea": "South Korea",
        "United Kingdom": "Great Britain",
        "Russian Federation": "Russia",
        "Islamic Republic of Iran": "Iran",
        "Hong Kong, China": "Hong Kong",
        "Czechia": "Czech Republic",
        "Ivory Coast": "Côte d'Ivoire",
        "Democratic People's Republic of Korea": "North Korea"
    }
    df_histo['country'] = df_histo['country'].replace(mapping)

    # Fusion
    df = pd.concat([df_histo, df_recent], ignore_index=True)

    # Calcul des points
    df['Points'] = (df.gold * 3) + (df.silver * 2) + (df.bronze * 1)

    # Création du RANG OFFICIEL (Tri Or > Argent > Bronze)
    # 1. On crée une colonne temporaire de tuples (Or, Argent, Bronze)
    # Les tuples se comparent naturellement : (1, 0, 0) > (0, 10, 10)
    df['rank_key'] = list(zip(df.gold, df.silver, df.bronze))

    # 2. On calcule le rang sur cette clé de tuple
    # On utilise method='min' pour avoir le 1, 1, 3
    df['Rang'] = df.groupby(['year', 'games_type'])['rank_key'].rank(method='min', ascending=False).astype(int)

    # 3. On vire la clé temporaire
    df.drop(columns='rank_key', inplace=True)

    # Calcul du total
    df['Total'] = df.gold + df.silver + df.bronze
    
    # Renommage "User Friendly"
    df = df.rename(columns={
        'year': 'Année',
        'games_type': 'Saison',
        'country': 'Nation',
        'host_city': 'Ville',
        'host_country': 'Pays Hôte',
        'gold': 'Or',
        'silver': 'Argent',
        'bronze': 'Bronze'
    })
    # Traduction des saisons pour l'affichage
    df['Saison'] = df['Saison'].replace({'Summer': 'été', 'Winter': 'hiver'})

    # On crée la colonne Drapeau juste avant de finir
    df['Drapeau'] = df['Nation'].apply(get_flag_url)

    # Ordre des colonnes
    ordre_final = [
        'Rang', 'Drapeau', 'Nation', 'Or', 'Argent', 'Bronze', 'Total', 'Points', 
        'Année', 'Saison', 'Ville', 'Pays Hôte'
    ]
    df = df[ordre_final]

    return df