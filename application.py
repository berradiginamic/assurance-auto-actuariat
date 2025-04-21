import streamlit as st
import base64
from pathlib import Path


def show_homepage():
    # Sidebar
    st.sidebar.image("images/assurance.jpg", width=120)
    st.sidebar.title("Navigation")
    st.sidebar.markdown("""
    - [Connexion aux données](1_🔌_connexion_données.py)
    - [Analyse exploratoire](2_🔍_Analyse_exploratoire_des_données.py)
    - [Modélisation GLM](3_📈_Modélisation_GLM.py)
    - [Simulateur](4_📊_Simulateur_tarification.py)
    - [Dashboard](6_📊_Dashboard_Interactif.py)
    - [Optimisation](10_💼_Optimisation_portefeuille.py)
    """, unsafe_allow_html=True)

    # Bannère
    st.image("images/actuariat.jpg", use_column_width=True)

    # Titre principal
    st.markdown('<h1 style="text-align:center; color:#2C3E50;">Assurance Non-Vie</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; color:#2980B9;">Approche Assurance Automobile</h2>', unsafe_allow_html=True)

    # Intro
    st.write("""
    L'actuariat non-vie est une branche de l'actuariat qui se concentre sur l'évaluation des risques et la gestion des produits d'assurance autres que ceux liés à la vie humaine :
    - assurance automobile,
    - habitation,
    - responsabilité civile,
    - risques professionnels.

    Cette application propose une expérience complète d'analyse, de modélisation et d'optimisation d'un portefeuille automobile.
    """)

    st.markdown("""
    ### 🔄 Fonctionnalités principales de l'application :
    - 🔌 **Connexion aux données** : CSV, Excel, PostgreSQL, MySQL, MongoDB.
    - 🔍 **Analyse exploratoire** : Statistiques, valeurs manquantes, distributions.
    - 📈 **Modélisation GLM** : Poisson pour la fréquence, Gamma pour le coût.
    - 📊 **Simulateur de primes** : Test de profils, tarification dynamique.
    - 🧠 **Benchmark modèles** : Comparaison GLM vs Random Forest.
    - 🎯 **Analyse sinistralité** : Par segment, heatmaps, détection risques.
    - 💼 **Optimisation portefeuille** : Rentabilité, stratégie tarifaire.
    - 🔖 **Export PDF** : Rapport automatisé prêt à partager.
    """, unsafe_allow_html=True)

    # Bouton de lancement rapide
    if st.button("🔄 Commencer l'analyse"):
        st.switch_page("pages/1_🔌_connexion_données.py")

    # Bouton téléchargement PDF (si dispo)
    pdf_path = Path("rapport_assurance.pdf")
    if pdf_path.exists():
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
            pdf_display = f"""
            <div style='text-align:center; margin-top:20px;'>
                <a href='data:application/pdf;base64,{base64_pdf}' download="rapport_assurance.pdf">
                    <button style='padding:0.4em 1.5em; background-color:#2980B9; color:white; border:none;'>
                    📄 Télécharger le rapport PDF
                    </button></a>
            </div>
            """
            st.markdown(pdf_display, unsafe_allow_html=True)


def main():
    show_homepage()


if __name__ == "__main__":
    if 'dataframe' not in st.session_state:
        st.session_state['dataframe'] = None
    if 'original_dataframe' not in st.session_state:
        st.session_state['original_dataframe'] = None
    if 'final_dataframe' not in st.session_state:
        st.session_state['final_dataframe'] = None
    main()
