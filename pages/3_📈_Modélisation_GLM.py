import streamlit as st
import pandas as pd
import statsmodels.api as sm
import numpy as np

def main():
    st.title("📈 Modélisation Actuarielle - GLM")

    df = st.session_state.get("final_dataframe", None)
    if df is None:
        st.warning("Aucune donnée disponible. Veuillez d'abord charger les données.")
        return

    required_cols = ["ClaimNb", "Exposure", "ClaimAmount", "VehPower", "Area"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"Colonnes manquantes : {', '.join([c for c in required_cols if c not in df.columns])}")
        return

    df["Frequence"] = df["ClaimNb"] / df["Exposure"]
    df["Cout_moyen"] = df["ClaimAmount"] / df["ClaimNb"].replace(0, np.nan)

    # ------------------------
    st.subheader("🔹 GLM Fréquence (Poisson)")

    X_freq = pd.get_dummies(df[["VehPower", "Area"]], drop_first=True)
    X_freq = sm.add_constant(X_freq).astype(float)

    y_freq = df["ClaimNb"].astype(float)
    exposure = np.log(df["Exposure"]).astype(float)

    if X_freq.isnull().values.any() or y_freq.isnull().values.any() or exposure.isnull().values.any():
        st.error("❌ Des valeurs manquantes détectées dans les variables du modèle.")
        return

    model_freq = sm.GLM(y_freq, X_freq, family=sm.families.Poisson(), offset=exposure)
    result_freq = model_freq.fit()
    st.text(result_freq.summary())

    # ------------------------
    st.subheader("🔹 GLM Coût Moyen (Gamma)")

    df_non_zero = df[df["ClaimNb"] > 0].copy()
    df_non_zero["Cout_moyen"] = df_non_zero["ClaimAmount"] / df_non_zero["ClaimNb"]

    X_cout = pd.get_dummies(df_non_zero[["VehPower", "Area"]], drop_first=True)
    X_cout = sm.add_constant(X_cout).astype(float)
    y_cout = df_non_zero["Cout_moyen"].astype(float)

    if X_cout.isnull().values.any() or y_cout.isnull().values.any():
        st.error("❌ Des valeurs manquantes dans les données du modèle de coût.")
        return

    model_cout = sm.GLM(y_cout, X_cout, family=sm.families.Gamma(sm.families.links.log()))
    result_cout = model_cout.fit()
    st.text(result_cout.summary())

    # ------------------------
    st.subheader("💡 Prime Pure simulée")
    df["Prime_pure"] = df["Frequence"] * df["Cout_moyen"]
    st.write(df[["Area", "VehPower", "Exposure", "Frequence", "Cout_moyen", "Prime_pure"]].head(10))
    st.success("✅ Modèle GLM appliqué avec succès !")


if __name__ == "__main__":
    main()