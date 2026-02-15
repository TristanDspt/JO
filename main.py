import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from logic import load_and_process

# 1. CONFIGURATION
st.set_page_config(layout="wide")

# 2. CHARGEMENT ET FILTRAGE
df = load_and_process()

# Titre Principal Centré
st.markdown("<h1 style='text-align: center;'>Classements des Jeux Olympiques</h1>", unsafe_allow_html=True)

# Explications
with st.expander("❓ C'est quoi ce projet ? (Lire l'explication)"):
    st.markdown("""
        **Le problème :** Le classement officiel des JO se base uniquement sur le nombre de médailles d'or. Si un pays a 100 médailles d'argent et 0 d'or, il sera derrière un pays qui a 1 seule médaille d'or. Pas très juste, non ?
        
        **Ma solution :** J'ai créé un **Classement par points** plus équilibré :
        * 🥇 **Or** : 3 points
        * 🥈 **Argent** : 2 points
        * 🥉 **Bronze** : 1 point
        
        Ici, tu peux comparer le classement "Officiel" avec mon nouveau système et voir quelles nations s'en sortent le mieux sur la globalité de leurs performances.
    """)

liste_annees = sorted(df['Année'].unique(), reverse=True)
annee_choisie = st.selectbox("Sélectionnez l'année des JO :", liste_annees)

df_filtre = df[df['Année'] == annee_choisie]

if not df_filtre.empty:
    # Récupération des infos pour le titre dynamique
    ville = df_filtre['Ville'].iloc[0]
    pays_hote = df_filtre['Pays Hôte'].iloc[0]
    saison = df_filtre['Saison'].iloc[0]
    
    # Préparation des DataFrames de travail
    df_propre = df_filtre.drop(columns=['Ville', 'Pays Hôte', 'Saison', 'Année'])

    # DF Points
    df_points = df_propre.sort_values(by='Points', ascending=False).copy()
    df_points.insert(1, 'NV Rang', df_points.Points.rank(ascending=False, method='min').astype(int))

    # DF Total
    df_total = df_propre.sort_values(by='Total', ascending=False).copy()
    df_total.insert(1, 'NV Rang', df_total.Total.rank(ascending=False, method='min').astype(int))

    # 3. PRÉPARATION DU GRAPHIQUE
    fig, ax_plot = plt.subplots(figsize=(12, 6))
    df_points.set_index('Nation').sort_values('Points', ascending=True)[['Or', 'Argent', 'Bronze']].tail(10).plot(
        kind='barh', 
        stacked=True, 
        color=['gold', 'silver', '#CD7F32'],
        ax=ax_plot
    )
    ax_plot.set_title("Top 10 par points", fontweight='bold', pad=10, fontsize=15)
    ax_plot.set_xlabel("Nombres de médailles")
    ax_plot.set_ylabel("")
    for c in ax_plot.containers:
        ax_plot.bar_label(c, label_type='center', color='black', fontsize=10)

    # 4. INTERFACE GRAPHIQUE (Affichage)
    st.markdown(f"<h2 style='text-align: center;'>Résultats pour les JO d'{saison} : {ville} {annee_choisie} - {pays_hote}</h2>", unsafe_allow_html=True)
    st.write("---")

    # LIGNE 1 : Points
    st.markdown("<h3 style='text-align: center;'>🏆 Classement par points</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_points, hide_index=True, use_container_width=True)
    with col2:
        st.pyplot(fig)

    st.write("---")

    # LIGNE 2 : Comparaisons
    col3, col4 = st.columns(2)
    with col3:
        st.write("#### 🥇 Classement Officiel")
        st.dataframe(df_propre, hide_index=True, use_container_width=True)
    with col4:
        st.write("#### 🔢 Total de médailles")
        st.dataframe(df_total, hide_index=True, use_container_width=True)
else:
    st.error("Données non trouvées pour cette année.")