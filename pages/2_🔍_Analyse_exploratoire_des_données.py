import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def show_homepage():
    st.image("images/actuariat.jpg", width=150)
    st.image("images/assurance.jpg", use_column_width=True)

def main():
    show_homepage()

    st.title("📊 Analyse Exploratoire des Données")
    st.markdown("Explorez visuellement et statistiquement vos données d'assurance auto.")

    if 'final_dataframe' in st.session_state and st.session_state['final_dataframe'] is not None:
        df = st.session_state['final_dataframe']

        # Filtres interactifs
        st.sidebar.header("🎛️ Filtres")
        selected_area = st.sidebar.multiselect("Zone géographique (Area)", df['Area'].unique(), default=df['Area'].unique())
        age_range = st.sidebar.slider("Âge du conducteur", int(df['DrivAge'].min()), int(df['DrivAge'].max()),
                                      (int(df['DrivAge'].min()), int(df['DrivAge'].max())))

        # Application des filtres
        df_filtered = df[(df['Area'].isin(selected_area)) &
                         (df['DrivAge'] >= age_range[0]) &
                         (df['DrivAge'] <= age_range[1])]

        st.success(f"{df_filtered.shape[0]} lignes affichées après filtrage")

        # Statistiques descriptives
        st.header("📌 Statistiques descriptives")
        st.dataframe(df_filtered.describe(include='all'))

        # Types de données
        st.subheader("📁 Types de données")
        st.write(df_filtered.dtypes)

        # Valeurs manquantes
        st.subheader("🚫 Valeurs manquantes")
        st.write(df_filtered.isnull().sum())

        # Valeurs uniques des colonnes catégorielles
        st.subheader("🔤 Valeurs uniques (colonnes catégorielles)")
        categorical_columns = df_filtered.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            st.markdown(f"**{col}**")
            st.write(df_filtered[col].value_counts())

        # Visualisations
        st.header("📈 Visualisations")

        st.subheader("Distribution de l'âge du conducteur")
        fig = px.histogram(df_filtered, x='DrivAge', nbins=20)
        st.plotly_chart(fig)

        st.subheader("Répartition des sinistres par zone géographique")
        fig2 = px.bar(df_filtered.groupby("Area")["ClaimNb"].sum().reset_index(), x='Area', y='ClaimNb')
        st.plotly_chart(fig2)

        st.subheader("Heatmap des corrélations")
        numeric_df = df_filtered.select_dtypes(include='number')
        fig3, ax = plt.subplots()
        sns.heatmap(numeric_df.corr(), annot=True, cmap='Blues', ax=ax)
        st.pyplot(fig3)

        # KPIs actuariaux
        st.header("🧮 KPIs Actuariels")

        # Vérification des colonnes
        required_cols = ["ClaimNb", "Exposure", "ClaimAmount"]
        missing = [col for col in required_cols if col not in df.columns]

        if not missing:
            df["Frequence"] = df["ClaimNb"] / df["Exposure"]
            df["Cout_moyen"] = df["ClaimAmount"] / df["ClaimNb"].replace(0, pd.NA)
            df["Sinistralite_pure"] = df["ClaimAmount"] / df["Exposure"]

            col1, col2, col3 = st.columns(3)
            col1.metric("📌 Fréquence moyenne", f"{df['Frequence'].mean():.3f}")
            col2.metric("💰 Coût moyen", f"{df['Cout_moyen'].mean():,.0f} €")
            col3.metric("🔥 Sinistralité pure", f"{df['Sinistralite_pure'].mean():,.0f} €")

            st.subheader("📍 Sinistralité pure par zone géographique")
            st.bar_chart(df.groupby("Area")["Sinistralite_pure"].mean())
        else:
            st.error(f"Colonnes manquantes : {', '.join(missing)}")

if __name__ == "__main__":
    main()
