import streamlit as st
import statsmodels.api as sm
import pandas as pd

def main():
    st.title("📊 Simulateur de Prime Pure")
    df = st.session_state.get("final_dataframe")

    area = st.selectbox("Zone géographique", df["Area"].unique())
    vehpower = st.slider("Puissance véhicule", 4, 15, 6)
    exposure = st.slider("Exposition", 0.1, 1.0, 1.0)

    frequence = 0.2 if area == "B" else 0.12  # valeurs à ajuster selon modèle
    cout_moyen = 500 + 30 * vehpower
    prime = frequence * cout_moyen * exposure

    st.markdown(f"""
    **Résultat :**
    - 📌 Fréquence estimée : `{frequence:.2f}`
    - 💰 Coût moyen estimé : `{cout_moyen:.0f} €`
    - 🧾 Prime pure estimée : `{prime:.0f} €`
    """)

if __name__ == "__main__":
    main()