import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")
st.title("💼 Optimisation du Portefeuille Assurance Auto")

if 'final_dataframe' not in st.session_state or st.session_state['final_dataframe'] is None:
    st.warning("Veuillez charger les données d'abord.")
    st.stop()

# --- Données et calculs ---
df = st.session_state['final_dataframe'].copy()
df = df[df["Exposure"] > 0].copy()
df["Frequence"] = df["ClaimNb"] / df["Exposure"]
df["Cout_moyen"] = df["ClaimAmount"] / df["ClaimNb"].replace(0, np.nan)
df["Sinistralite_pure"] = df["ClaimAmount"] / df["Exposure"]
df = df.dropna(subset=["Cout_moyen"])

# Ajout d'une prime commerciale simulée (aléatoire pour exemple)
df["Prime_commerciale"] = df["Sinistralite_pure"] * np.random.uniform(0.8, 1.4, size=len(df))
df["Rentabilite"] = df["Prime_commerciale"] - df["Sinistralite_pure"]

def get_tag(row):
    if row["Rentabilite"] > 100:
        return "Rentable"
    elif row["Rentabilite"] < -100:
        return "Risque"
    else:
        return "Neutre"

df["Segment"] = df.apply(get_tag, axis=1)

# --- KPIs ---
st.subheader("📊 Répartition des contrats par rentabilité")
st.dataframe(df[["Prime_commerciale", "Sinistralite_pure", "Rentabilite", "Segment"]].head(10))
st.plotly_chart(px.pie(df, names="Segment", title="Part des contrats par niveau de rentabilité"), use_container_width=True)

# --- Recommandations d'action ---
st.subheader("📌 Recommandations d'action")
action_map = {
    "Rentable": "✅ Maintenir / Fidéliser",
    "Neutre": "🔍 Surveiller",
    "Risque": "⚠️ Revoir tarification / conditions"
}
df_action = df.groupby("Segment")["Rentabilite"].agg(["count", "mean"]).reset_index()
df_action["Recommandation"] = df_action["Segment"].map(action_map)
st.dataframe(df_action.rename(columns={"count": "Nb contrats", "mean": "Rentabilité moyenne"}))

# --- Visualisation ---
st.subheader("📈 Visualisation: Prime Commerciale vs Sinistralité Pure")
fig = px.scatter(df, x="Sinistralite_pure", y="Prime_commerciale", color="Segment", hover_data=["Region", "VehBrand", "VehPower"])
fig.add_shape(type="line", x0=0, y0=0, x1=df["Sinistralite_pure"].max(), y1=df["Sinistralite_pure"].max(), line=dict(color="gray", dash="dash"))
st.plotly_chart(fig, use_container_width=True)
