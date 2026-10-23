
import streamlit as st
import pandas as pd
import database

st.set_page_config(
    page_title="E-Commune",
    page_icon="🏛️",
    layout="wide"
)

# Création de la base et de la table si nécessaire
database.initialiser_base()

st.title("🏛️ E-Commune")
st.caption("Gestion numérique des demandes administratives")

# Formulaire
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

    description = st.text_area("Informations complémentaires")
    envoyer = st.form_submit_button("Enregistrer la demande")

    if envoyer:
        if not nom.strip():
            st.error("Veuillez saisir le nom du demandeur.")
        else:
            database.ajouter_demande(
                nom.strip(),
                type_demande,
                description.strip()
            )
            st.success("Demande enregistrée dans la base de données !")

# Chargement des données persistantes
lignes = database.obtenir_demandes()

colonnes = [
    "ID", "Demandeur", "Type de demande",
    "Description", "Statut", "Date de création"
]

demandes = pd.DataFrame(lignes, columns=colonnes)

st.divider()
st.header("Tableau de bord")

total = len(demandes)

if total > 0:
    terminees = int((demandes["Statut"] == "Terminée").sum())
    en_cours = int((demandes["Statut"] == "En cours").sum())
    en_attente = int((demandes["Statut"] == "En attente").sum())
else:
    terminees = en_cours = en_attente = 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total des demandes", total)
col2.metric("Terminées", terminees)
col3.metric("En cours", en_cours)
col4.metric("En attente", en_attente)

st.subheader("Répartition des demandes")

if total > 0:
    st.bar_chart(demandes["Statut"].value_counts())
else:
    st.info("Aucune demande enregistrée pour le moment.")

st.subheader("Mettre à jour le statut")

if total > 0:
    id_demande = st.selectbox(
        "Choisir l'ID de la demande",
        demandes["ID"].tolist()
    )

    nouveau_statut = st.selectbox(
        "Nouveau statut",
        ["En attente", "En cours", "Terminée"]
    )

    if st.button("Mettre à jour"):
        database.modifier_statut(
            id_demande,
            nouveau_statut
        )
        st.success("Statut mis à jour.")
        st.rerun()
else:
    st.info("Ajoutez d'abord une demande.")

st.subheader("Suivi des demandes")
recherche = st.text_input(
    "🔎 Rechercher par nom ou type de demande"
)

filtre = st.selectbox(
    "Filtrer par statut",
    ["Toutes", "En cours", "En attente", "Terminée"]
)
if total > 0:
    affichage = demandes.copy()

    if filtre != "Toutes":
        affichage = affichage[
            affichage["Statut"] == filtre
        ]

    if recherche.strip():
        masque = (
            affichage["Demandeur"].str.contains(
                recherche, case=False, na=False
            )
            |
            affichage["Type de demande"].str.contains(
                recherche, case=False, na=False
            )
        )
        affichage = affichage[masque]

    st.dataframe(
        affichage,
        use_container_width=True,
        hide_index=True
    )

    st.caption(f"{len(affichage)} demande(s) trouvée(s).")
else:
    st.info("Le tableau apparaîtra dès qu'une demande sera enregistrée.")

st.divider()
st.subheader("📥 Exporter les demandes")

if not demandes.empty:
    fichier_csv = demandes.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="Télécharger les demandes (CSV)",
        data=fichier_csv,
        file_name="demandes_ecommune.csv",
        mime="text/csv"
    )
else:
    st.info("Aucune demande à exporter.")


st.divider()

st.header("🔐 Gouvernance des données")

st.subheader("Règles de gestion")

st.markdown("""
- **Confidentialité :** ne pas collecter d'informations inutiles.
- **Qualité :** chaque demande doit avoir un nom et un type de document.
- **Intégrité :** le statut doit respecter les valeurs autorisées.
- **Accès :** seules les personnes autorisées doivent consulter les demandes.
- **Traçabilité :** les changements de statut doivent pouvoir être suivis.
- **Conservation :** les données doivent être conservées selon les règles
  définies par l'administration.
""")

st.info(
    "Prototype pédagogique : utiliser uniquement des données fictives. "
    "L'authentification et la journalisation des modifications restent à implémenter."
)