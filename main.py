import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from logic import load_and_process

# 1. CONFIGURATION
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] {
        align-items: center;
        justify-content: center;
    }
    div.stRadio > div {
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

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

# Selection de la saison
_, _, col, _ , _= st.columns([3,1,2,1,2])

with col:
    # On utilise un dictionnaire pour mapper l'affichage vers la valeur réelle du DF
    options_saison = {"☀️ Été": "été", "❄️ Hiver": "hiver"}

    choix_visuel = st.pills(
        "Saison :",
        options=list(options_saison.keys()),
        default='☀️ Été',
        label_visibility="collapsed" # Optionnel : masque le texte "Saison" pour gagner de la place
    )
    if choix_visuel is None:
        choix_visuel = '☀️ Été'
    saison_selectionnee = options_saison[choix_visuel]

liste_annees = sorted(df[df['Saison'] == saison_selectionnee]['Année'].unique(), reverse=True)
annee_choisie = st.selectbox("Sélectionnez l'année des JO :", liste_annees)
df_filtre = df[(df['Année'] == annee_choisie) & (df['Saison'] == saison_selectionnee)]

if not df_filtre.empty:
    # Récupération des infos pour le titre dynamique
    ville = df_filtre['Ville'].iloc[0]
    pays_hote = df_filtre['Pays Hôte'].iloc[0]
    saison = df_filtre['Saison'].iloc[0]
    
    # Préparation des DataFrames de travail
    df_propre = df_filtre.drop(columns=['Ville', 'Pays Hôte', 'Saison', 'Année'])

    # DF Points
    df_points = df_propre.sort_values(by='Points', ascending=False).copy()
    df_points.insert(0, 'NV Rang', df_points.Points.rank(ascending=False, method='min').astype(int))

    # DF Officiel
    df_officiel = df_propre.sort_values(by='Rang').copy()

    # DF Total
    df_total = df_propre.sort_values(by='Total', ascending=False).copy()
    df_total.insert(0, 'NV Rang', df_total.Total.rank(ascending=False, method='min').astype(int))

    # 3. PRÉPARATION DES GRAPHIQUES
    # Graphique top 10
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

    # Graphique historique
    liste_t10 = df_points.head(10)["Nation"].tolist()
    df_t10_histo = df.query("Nation in @liste_t10 & Saison == @saison_selectionnee")
    df_t10_histo = df_t10_histo.pivot_table(index='Année', columns='Nation', values='Points').fillna(0)
    df_t10_cumul = df_t10_histo.cumsum()

    # 4. INTERFACE GRAPHIQUE (Affichage)
    st.markdown(f"<h2 style='text-align: center;'>Résultats pour les JO d'{saison} : {ville} {annee_choisie} - {pays_hote}</h2>", unsafe_allow_html=True)
    st.divider()

    config_col = {
            "Rang": st.column_config.NumberColumn("Rang", width=30),
            "Drapeau": st.column_config.ImageColumn("", width=45),
            "NV Rang": st.column_config.NumberColumn("#", width=30),
            "Nation": st.column_config.TextColumn("Nation"),
            "Or": st.column_config.NumberColumn("🥇", width=30),
            "Argent": st.column_config.NumberColumn("🥈", width=30),
            "Bronze": st.column_config.NumberColumn("🥉", width=30),
            "Total": st.column_config.NumberColumn("Total", width=50, format="%d"),
            "Points": st.column_config.ProgressColumn(
                "Points",
                help="Système de Points : 3-2-1",
                format="%d",
                width="medium",
                min_value=0,
                max_value=int(df_points.Points.max()),
            ),
        }

    # LIGNE 1 : Points
    st.markdown("<h3 style='text-align: center;'>🏆 Classement par points</h3>", unsafe_allow_html=True)

    # On crée une petite ligne dédiée pour le toggle, centrée
    _, _, col, _ , _= st.columns([2.8,1,2,1,2])
    with col:
        afficher_tout = st.toggle("Voir tout le classement", value=False)

        limite = None if afficher_tout else 10

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_points.head(limite), hide_index=True, use_container_width=True, column_config=config_col)
    with col2:
        st.pyplot(fig)

    st.divider()

    # LIGNE 2 : Comparaisons
    col3, col4 = st.columns(2)
    with col3:
        st.write("#### 🥇 Classement Officiel")
        st.dataframe(df_officiel.head(limite), hide_index=True, use_container_width=True, column_config=config_col)
    with col4:
        st.write("#### 🔢 Total de médailles")
        st.dataframe(df_total.head(limite), hide_index=True, use_container_width=True, column_config=config_col)

    # LIGNE 3 : Evolution
    st.divider()
    st.markdown("<h3 style='text-align: center;'>📈 Évolution historique du Top 10 actuel</h3>", unsafe_allow_html=True)

    # On définit la période dispo sur le DF de base (brut)
    toutes_annees = sorted(df_t10_histo.index.tolist())
    annees_limitees = [a for a in toutes_annees if a <= annee_choisie]

    col_s, col_ex = st.columns([5, 2])

    with col_s:
        periode = st.select_slider(
        "Filtrer la période historique :",
        options=annees_limitees,
        value=(min(annees_limitees), max(annees_limitees))
        )

    # Filtre : On prend les données BRUTES sur la période
    df_brut_zoom = df_t10_histo.loc[periode[0]:periode[1]]

    # Cumul : On fait le cumulatif sur ce zoom uniquement
    df_t10_zoom = df_brut_zoom.cumsum()

    # Option pour masquer les USA
    with col_ex:
        pays_a_exclure = st.multiselect(
            "🚫 Exclure du graphique :",
            options=df_t10_zoom.columns.tolist(),
            default=[]
    )

    if pays_a_exclure:
        df_t10_zoom = df_t10_zoom.drop(columns=pays_a_exclure)

    # On recalcule le tri de la légende (car si on vire les USA, le n°1 change)
    dernier_score = df_t10_zoom.iloc[-1]
    pays_tries = dernier_score.sort_values(ascending=False).index
    df_t10_zoom = df_t10_zoom[pays_tries]

    # Tri de la legende
    dernier_score = df_t10_zoom.iloc[-1]
    pays_tries = dernier_score.sort_values(ascending=False).index
    df_t10_zoom = df_t10_zoom[pays_tries]

    # Dessin
    fig2, ax2 = plt.subplots(figsize=(12, 5)) 
    sns.lineplot(data=df_t10_zoom, marker='o', ax=ax2, dashes=False)

    # Habillage
    ax2.set_title(f"Performance des leaders de {annee_choisie} au fil du temps", pad=15)
    ax2.set_ylabel("Points")
    ax2.set_xlabel("")
    plt.tick_params(axis='x', pad=2, labelsize=11)
    plt.tick_params(axis='y', pad=2, labelsize=11) 
    ax2.set_xticks(df_t10_zoom.index[::2])
    plt.xticks(rotation=45)

    ax2.legend(title="Nations", bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    sns.despine(left=True, bottom=True)
    plt.grid(axis='y', alpha=0.5)
    plt.grid(axis='x', alpha=0.25)
    
    # Affichage
    st.pyplot(fig2, use_container_width=True)

else:
    st.error("Données non trouvées pour cette année.")
