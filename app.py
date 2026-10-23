
import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="E-Commune",
    page_icon="🏛️",
    layout="wide"
)

# Données fictives pour notre prototype
demandes = pd.DataFrame([
    {"ID": "DEM-001", "Type": "Attestation de résidence", "Statut": "En cours", "Jour": 1},
    {"ID": "DEM-002", "Type": "Légalisation de signature", "Statut": "Terminée", "Jour": 2},
    {"ID": "DEM-003", "Type": "Attestation administrative", "Statut": "En attente", "Jour": 3},
    {"ID": "DEM-004", "Type": "Attestation de résidence", "Statut": "En cours", "Jour": 4},
    {"ID": "DEM-005", "Type": "Légalisation de signature", "Statut": "Terminée", "Jour": 2},
    {"ID": "DEM-006", "Type": "Attestation administrative", "Statut": "En attente", "Jour": 5},
    {"ID": "DEM-007", "Type": "Attestation de résidence", "Statut": "En cours", "Jour": 1},
    {"ID": "DEM-008", "Type": "Attestation administrative", "Statut": "Terminée", "Jour": 2},
])

# En-tête
st.title("🏛️ E-Commune")
st.subheader("Plateforme de gestion des demandes administratives")
st.caption("Prototype pédagogique — données entièrement fictives")

# Indicateurs
total = len(demandes)
terminees = (demandes["Statut"] == "Terminée").sum()
en_cours = (demandes["Statut"] == "En cours").sum()
en_attente = (demandes["Statut"] == "En attente").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total des demandes", total)
col2.metric("Terminées", int(terminees))
col3.metric("En cours", int(en_cours))
col4.metric("En attente", int(en_attente))

st.divider()

# Graphique des statuts
st.subheader("Répartition des demandes")
repartition = demandes["Statut"].value_counts()
st.bar_chart(repartition)

# Tableau des demandes
st.subheader("Suivi des demandes")
filtre = st.selectbox(
    "Filtrer par statut",
    ["Toutes", "En cours", "En attente", "Terminée"]
)

if filtre == "Toutes":
    affichage = demandes
else:
    affichage = demandes[demandes["Statut"] == filtre]

st.dataframe(affichage, use_container_width=True, hide_index=True)