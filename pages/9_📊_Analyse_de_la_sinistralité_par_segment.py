import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🔍 Analyse de la Sinistralité par Segment")

if 'final_dataframe' not in st.session_state or st.session_state['final_dataframe'] is None:
    st.warning("Veuillez charger les données d'abord.")
    st.stop()

df = st.session_state['final_dataframe'].copy()
df = df[df["Exposure"] > 0].copy()
df["Frequence"] = df["ClaimNb"] / df["Exposure"]
df["Cout_moyen"] = df["ClaimAmount"] / df["ClaimNb"].replace(0, np.nan)
df["Sinistralite_pure"] = df["ClaimAmount"] / df["Exposure"]

st.subheader("🎯 Choix des dimensions de segmentation")
seg_col1 = st.selectbox("Variable en X (Segment 1)", df.columns, index=df.columns.get_loc("Region"))
seg_col2 = st.selectbox("Variable en Y (Segment 2)", df.columns, index=df.columns.get_loc("VehPower"))

# Agrégation
grouped = df.groupby([seg_col1, seg_col2])["Sinistralite_pure"].mean().unstack().fillna(0)

# Heatmap
st.subheader("📊 Heatmap - Sinistralité Pure Moyenne")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(grouped, annot=True, fmt=".0f", cmap="Reds", ax=ax)
st.pyplot(fig)

# Affichage des segments à forte sinistralité
st.subheader("🚨 Segments à risque ")
thresh = st.slider("Seuil de sinistralité pure élevée (€)", 500, 3000, 1000)
high_risk = df[df["Sinistralite_pure"] > thresh]
st.write(f"{high_risk.shape[0]} contrats avec sinistralité > {thresh} €")
st.dataframe(high_risk[["Region", "VehBrand", "VehPower", "DrivAge", "Sinistralite_pure"]].sort_values(by="Sinistralite_pure", ascending=False).head(20))
