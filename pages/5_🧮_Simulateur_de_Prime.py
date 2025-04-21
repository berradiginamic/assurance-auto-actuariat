import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm

def main():
    st.title("🧮 Simulateur de Prime Pure")

    df = st.session_state.get("final_dataframe", None)
    if df is None:
        st.warning("Veuillez charger les données dans l'application.")
        return

    # Préparation du DataFrame pour les modèles
    df = df.copy()
    df["Frequence"] = df["ClaimNb"] / df["Exposure"]
    df["Cout_moyen"] = df["ClaimAmount"] / df["ClaimNb"].replace(0, np.nan)
    df_non_zero = df[df["ClaimNb"] > 0].copy()

    # ======= Modèles GLM =======
    st.markdown("## 🔁 Calcul des modèles en arrière-plan...")

    # Modèle fréquence
    X_freq = pd.get_dummies(df[["VehPower", "Area"]], drop_first=True)
    X_freq = sm.add_constant(X_freq).astype(float)
    y_freq = df["ClaimNb"]
    exposure = np.log(df["Exposure"])
    glm_freq = sm.GLM(y_freq, X_freq, family=sm.families.Poisson(), offset=exposure)
    res_freq = glm_freq.fit()

    # Modèle coût
    X_cout = pd.get_dummies(df_non_zero[["VehPower", "Area"]], drop_first=True)
    X_cout = sm.add_constant(X_cout).astype(float)
    y_cout = df_non_zero["Cout_moyen"]
    glm_cout = sm.GLM(y_cout, X_cout, family=sm.families.Gamma(sm.families.links.log()))
    res_cout = glm_cout.fit()

    st.success("✅ Modèles GLM recalculés avec succès !")

    # ======= Interface utilisateur =======
    st.markdown("## 🎯 Choix du profil assuré")

    # Choix utilisateur
    vehpower = st.slider("Puissance du véhicule", int(df["VehPower"].min()), int(df["VehPower"].max()), 6)
    area = st.selectbox("Zone géographique", df["Area"].unique())
    exposure_input = st.slider("Durée d'exposition (en années)", 0.1, 1.0, 1.0)

    # Création de la ligne à prédire
    input_data = pd.DataFrame({
        "VehPower": [vehpower],
        "Area": [area]
    })
    input_freq = pd.get_dummies(input_data, drop_first=True)
    input_freq = sm.add_constant(input_freq.reindex(columns=X_freq.columns, fill_value=0)).astype(float)

    # Prédiction fréquence
    freq_pred = res_freq.predict(input_freq, offset=np.log([exposure_input]))[0]

    # Prédiction coût
    input_cout = sm.add_constant(input_freq.drop(columns='const')).astype(float)
    input_cout = input_cout.reindex(columns=X_cout.columns, fill_value=0)
    cout_pred = res_cout.predict(input_cout)[0]

    # Prime pure
    prime = freq_pred * cout_pred

    # Résultat
    st.markdown("## 📊 Résultat de la Simulation")

    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Fréquence estimée", f"{freq_pred:.3f}")
    col2.metric("💰 Coût moyen estimé", f"{cout_pred:.0f} €")
    col3.metric("🧾 Prime pure estimée", f"{prime:.0f} €")


if __name__ == "__main__":
    main()