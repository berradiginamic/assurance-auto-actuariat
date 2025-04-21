import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from xhtml2pdf import pisa
import tempfile

st.set_page_config(layout="wide")

st.title("📊 Dashboard Actuariel Interactif - Assurance Auto")

# Load data from session or fallback
if 'final_dataframe' in st.session_state and st.session_state['final_dataframe'] is not None:
    df = st.session_state['final_dataframe'].copy()
else:
    st.warning("Aucune donnée chargée. Veuillez importer un fichier depuis la page de connexion.")
    st.stop()

# --- FILTRES SIDEBAR ---
st.sidebar.header("🎛️ Filtres")
regions = st.sidebar.multiselect("Régions", df["Region"].unique(), default=df["Region"].unique())
brands = st.sidebar.multiselect("Marques de véhicule", df["VehBrand"].unique(), default=df["VehBrand"].unique())
power_range = st.sidebar.slider("Puissance du véhicule", int(df["VehPower"].min()), int(df["VehPower"].max()), (4, 14))

# --- APPLICATION DES FILTRES ---
df_filtered = df[
    (df["Region"].isin(regions)) &
    (df["VehBrand"].isin(brands)) &
    (df["VehPower"] >= power_range[0]) &
    (df["VehPower"] <= power_range[1])
]

st.success(f"{df_filtered.shape[0]} lignes affichées après filtrage")

# --- KPIs ---
st.subheader("🧮 Indicateurs Clés")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Fréquence moyenne", f"{df_filtered['Frequence'].mean():.3f}")
kpi2.metric("Coût moyen", f"{df_filtered['Cout_moyen'].mean():.0f} €")
kpi3.metric("Sinistralité pure", f"{df_filtered['Sinistralite_pure'].mean():.0f} €")

# --- PLOTS ---
st.subheader("📈 Visualisations Interactives")

fig1 = px.bar(df_filtered.groupby("Area")["Frequence"].mean().reset_index(), x="Area", y="Frequence", title="Fréquence moyenne par zone")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(df_filtered.groupby("VehBrand")["Sinistralite_pure"].mean().reset_index(), x="VehBrand", y="Sinistralite_pure", title="Sinistralité pure par marque")
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.histogram(df_filtered, x="DrivAge", nbins=20, title="Distribution de l'âge des conducteurs")
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.scatter(df_filtered, x="VehAge", y="ClaimAmount", color="VehBrand", title="Montant des sinistres en fonction de l'âge du véhicule")
st.plotly_chart(fig4, use_container_width=True)

# --- EXPORT PDF ---
st.subheader("📥 Export du rapport (HTML > PDF)")

def convert_html_to_pdf(source_html, output_filename):
    with open(output_filename, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(src=source_html, dest=result_file)
    return pisa_status.err

if st.button("Générer le rapport PDF"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        html_content = f"""
        <h1>Rapport Actuariel - {now}</h1>
        <h3>Indicateurs Clés</h3>
        <ul>
            <li>Fréquence moyenne : {df_filtered['Frequence'].mean():.3f}</li>
            <li>Coût moyen : {df_filtered['Cout_moyen'].mean():.0f} €</li>
            <li>Sinistralité pure : {df_filtered['Sinistralite_pure'].mean():.0f} €</li>
        </ul>
        <p>Nombre de lignes : {df_filtered.shape[0]}</p>
        """
        convert_html_to_pdf(html_content, tmp_pdf.name)
        with open(tmp_pdf.name, "rb") as file:
            st.download_button("📥 Télécharger le rapport PDF", data=file, file_name="rapport_assurance.pdf")
