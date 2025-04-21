import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import PoissonRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

st.title("🧠 Benchmark de Modèles - Fréquence des Sinistres")

if 'final_dataframe' not in st.session_state or st.session_state['final_dataframe'] is None:
    st.warning("Veuillez charger les données sur la page d'accueil.")
    st.stop()

df = st.session_state['final_dataframe'].copy()
df = df[df["Exposure"] > 0]
df["Frequence"] = df["ClaimNb"] / df["Exposure"]

# --- Préparation des données ---
features = ["VehPower", "VehAge", "DrivAge"]
X = df[features]
y = df["Frequence"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# --- Modèle GLM Poisson ---
st.subheader("GLM Poisson")
glm = PoissonRegressor(alpha=1e-4, max_iter=300)
glm.fit(X_train, y_train)
y_pred_glm = glm.predict(X_test)

# --- Modèle Random Forest ---
st.subheader("Random Forest")
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

# --- Évaluation ---
def afficher_scores(y_true, y_pred, label):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    r2 = r2_score(y_true, y_pred)
    st.write(f"**{label}**")
    st.metric("MAE", f"{mae:.4f}")
    st.metric("RMSE", f"{rmse:.4f}")
    st.metric("R²", f"{r2:.4f}")

col1, col2 = st.columns(2)
with col1:
    afficher_scores(y_test, y_pred_glm, "GLM Poisson")
with col2:
    afficher_scores(y_test, y_pred_rf, "Random Forest")
