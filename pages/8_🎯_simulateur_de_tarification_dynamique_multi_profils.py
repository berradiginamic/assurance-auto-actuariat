import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm

st.title("🎯 Tarification Dynamique - Comparaison de Profils")

# Chargement des données
if 'final_dataframe' not in st.session_state or st.session_state['final_dataframe'] is None:
    st.warning("Veuillez charger les données d'abord.")
    st.stop()

# Dataset original
df = st.session_state['final_dataframe'].copy()
df = df[df["Exposure"] > 0].copy()
df["Frequence"] = df["ClaimNb"] / df["Exposure"]
df["Cout_moyen"] = df["ClaimAmount"] / df["ClaimNb"].replace(0, np.nan)
df = df.dropna(subset=["Cout_moyen"])

# --- GLM modèles pré-entraînés ---
X_freq = pd.get_dummies(df[["VehPower", "Area"]], drop_first=True)
X_freq = sm.add_constant(X_freq).astype(float)
y_freq = df["ClaimNb"]
exposure = np.log(df["Exposure"])
model_freq = sm.GLM(y_freq, X_freq, family=sm.families.Poisson(), offset=exposure).fit()

X_cout = pd.get_dummies(df[["VehPower", "Area"]], drop_first=True)
X_cout = sm.add_constant(X_cout).astype(float)
y_cout = df["Cout_moyen"]
model_cout = sm.GLM(y_cout, X_cout, family=sm.families.Gamma(sm.families.links.log())).fit()

# --- Interface multi-profils ---
st.subheader("📋 Création de profils personnalisés")
n_profiles = st.number_input("Nombre de profils à comparer", min_value=1, max_value=5, value=2)

profils = []
for i in range(n_profiles):
    st.markdown(f"### Profil {i+1}")
    col1, col2, col3 = st.columns(3)
    with col1:
        power = st.slider(f"Puissance (Profil {i+1})", 4, 15, 6)
    with col2:
        area = st.selectbox(f"Zone (Profil {i+1})", df["Area"].unique(), key=f"area_{i}")
    with col3:
        exposure_input = st.slider(f"Exposition (Profil {i+1})", 0.1, 1.0, 1.0, step=0.1)

    profils.append({"VehPower": power, "Area": area, "Exposure": exposure_input})

# --- Prédictions et résultats ---
results = []
for profil in profils:
    input_df = pd.DataFrame([profil])
    x_freq = pd.get_dummies(input_df, drop_first=True)
    x_freq = sm.add_constant(x_freq.reindex(columns=X_freq.columns, fill_value=0)).astype(float)
    x_cout = x_freq.reindex(columns=X_cout.columns, fill_value=0)

    pred_freq = model_freq.predict(x_freq, offset=np.log([profil["Exposure"]]))[0]
    pred_cout = model_cout.predict(x_cout)[0]
    prime = pred_freq * pred_cout

    profil.update({
        "Fréquence estimée": round(pred_freq, 3),
        "Coût moyen estimé": round(pred_cout, 0),
        "Prime pure": round(prime, 0)
    })
    results.append(profil)

# --- Affichage final ---
st.subheader("📊 Résultats de la comparaison")
df_results = pd.DataFrame(results)
st.dataframe(df_results.set_index(pd.Index([f"Profil {i+1}" for i in range(len(results))])))
