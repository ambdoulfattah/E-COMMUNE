
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="E-Commune",
    page_icon="🏛️",
    layout="wide"
)

# Initialisation des données fictives
if "demandes" not in st.session_state:
    st.session_state.demandes = pd.DataFrame([
        {"ID": "DEM-001", "Type": "Attestation de résidence", "Statut": "En cours"},
        {"ID": "DEM-002", "Type": "Légalisation de signature", "Statut": "Terminée"},
        {"ID": "DEM-003", "Type": "Attestation administrative", "Statut": "En attente"},
        {"ID": "DEM-004", "Type": "Attestation de résidence", "Statut": "En cours"},
        {"ID": "DEM-005", "Type": "Légalisation de signature", "Statut": "Terminée"},
        {"ID": "DEM-006", "Type": "Attestation administrative", "Statut": "En attente"},
        {"ID": "DEM-007", "Type": "Attestation de résidence", "Statut": "En cours"},
        {"ID": "DEM-008", "Type": "Attestation administrative", "Statut": "Terminée"},
    ])

st.title("🏛️ E-Commune")
st.caption("Gestion numérique des demandes administratives — prototype pédagogique")

# Formulaire de création
st.header("Nouvelle demande")

with st.form("formulaire_demande"):
    nom = st.text_input("Nom du demandeur")
    type_demande = st.selectbox(
        "Type de demande",
        [
            "Attestation de résidence",
            "Légalisation de signature",
            "Attestation administrative"
        ]
    )
    description = st.text_area("Description ou informations complémentaires")
    envoyer = st.form_submit_button("Enregistrer la demande")

    if envoyer:
        if not nom.strip():
            st.error("Veuillez saisir le nom du demandeur.")
        else:
            numero = len(st.session_state.demandes) + 1
            nouvelle_demande = {
                "ID": f"DEM-{numero:03d}",
                "Type": type_demande,
                "Statut": "En attente"
            }

            st.session_state.demandes = pd.concat(
                [
                    st.session_state.demandes,
                    pd.DataFrame([nouvelle_demande])
                ],
                ignore_index=True
            )

            st.session_state[f"nom_{numero}"] = nom.strip()
            st.session_state[f"description_{numero}"] = description
            st.success(f"Demande DEM-{numero:03d} enregistrée !")

st.divider()

# Indicateurs
demandes = st.session_state.demandes

total = len(demandes)
terminees = int((demandes["Statut"] == "Terminée").sum())
en_cours = int((demandes["Statut"] == "En cours").sum())
en_attente = int((demandes["Statut"] == "En attente").sum())

st.header("Tableau de bord")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total des demandes", total)
col2.metric("Terminées", terminees)
col3.metric("En cours", en_cours)
col4.metric("En attente", en_attente)

st.subheader("Répartition des demandes")
st.bar_chart(demandes["Statut"].value_counts())

st.subheader("Suivi des demandes")
filtre = st.selectbox(
    "Filtrer par statut",
    ["Toutes", "En cours", "En attente", "Terminée"]
)

affichage = demandes if filtre == "Toutes" else demandes[
    demandes["Statut"] == filtre
]

st.dataframe(affichage, use_container_width=True, hide_index=True)