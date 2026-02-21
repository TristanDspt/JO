# 🏅 JO : Le Classement Alternatif

👉 **Tester l'application en direct :** [tristandspt-jo.streamlit.app](https://tristandspt-jo.streamlit.app)

Ce projet Streamlit propose une nouvelle lecture de l'histoire des Jeux Olympiques en remplaçant le classement officiel (basé uniquement sur le nombre de médailles d'or) par un **système de points pondéré** pour mieux refléter la performance globale des nations.

## 🚀 Le Concept
Le classement officiel des JO peut être biaisé : une seule médaille d'or place une nation devant une autre ayant récolté 50 médailles d'argent. 
**Ma solution :** 
* 🥇 **Or** : 3 points
* 🥈 **Argent** : 2 points
* 🥉 **Bronze** : 1 point

## 🛠️ Stack Technique
* **Langage** : Python 3
* **Interface** : Streamlit (layout wide optimisé pour écran Ultrawide)
* **Analyse de données** : Pandas (Pivot tables, Method chaining, Query)
* **Visualisation** : Seaborn & Matplotlib
* **IDE & OS** : VS Code sur Windows 10

## 📊 Fonctionnalités
* **Tableau de bord interactif** : Comparaison entre le classement officiel, le total de médailles et le classement par points.
* **Analyse Historique** : Graphique d'évolution des 10 meilleures nations de l'édition sélectionnée.
* **Zoom Temporel** : Slider dynamique pour explorer des périodes spécifiques de l'histoire olympique.
* **Légende Intelligente** : Tri automatique de la légende en fonction des performances finales sur le graphique pour une lecture immédiate.

## 📂 Structure du projet
* `main.py` : Interface utilisateur et logique de visualisation.
* `logic.py` : Traitement des données, calculs des points et nettoyage.
* `medals.xlsx` + `olympic_games.csv` : Datasets historiques des Jeux Olympiques.

## ⚙️ Installation
1. Activer l'environnement virtuel.
2. Installer les dépendances : `pip install -r requirements.txt`.
3. Lancer l'application : `streamlit run main.py`.

---
*Projet réalisé par Tristan dans le cadre d'une reconversion Data Analyst.*