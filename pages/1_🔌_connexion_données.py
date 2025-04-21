import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from pymongo import MongoClient
import pymysql  # Nécessaire pour MySQL
import io


def show_homepage():
    st.image("images/actuariat.jpg", width=150)
    st.image("images/assurance.jpg", use_column_width=True)

def enrich_with_claim_amount(df):
    if "ClaimAmount" not in df.columns and "ClaimNb" in df.columns and "VehPower" in df.columns:
        vehicule_scale = df["VehPower"].map(lambda x: 250 + 30 * x)
        df["ClaimAmount"] = df["ClaimNb"] * np.random.gamma(shape=2.0, scale=vehicule_scale)
        st.success("✅ Colonne simulée 'ClaimAmount' ajoutée.")
    return df
def main():
    show_homepage()
    st.title("🔌 Connexion aux Données")
    st.write("Choisissez la source de données à analyser.")

    option = st.selectbox("📂 Source de Données", ["Télécharger CSV/Excel", "Se Connecter à une Base de Données"])

    # Option 1 - Fichier CSV ou Excel
    if option == "Télécharger CSV/Excel":
        uploaded_file = st.file_uploader("📎 Choisir un fichier CSV ou Excel", type=["csv", "xlsx"])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                st.session_state['dataframe'] = df
                st.session_state['original_dataframe'] = df.copy()
                st.session_state['dataframe'] = df
                st.session_state['original_dataframe'] = df.copy()
                df = enrich_with_claim_amount(df)
                st.session_state['final_dataframe'] = df.copy()
                st.success("✅ Fichier chargé avec succès.")
                st.dataframe(df)

            except Exception as e:
                st.error(f"❌ Erreur lors du chargement du fichier : {e}")

    # Option 2 - Connexion à base PostgreSQL
    elif option == "Se Connecter à une Base de Données":
        db_type = st.selectbox("🔧 Type de Base de Données", ["PostgreSQL", "MySQL", "MongoDB"])

        if db_type == "PostgreSQL":
            st.subheader("🟦 Connexion PostgreSQL")
            host = st.text_input("Hôte", value="localhost")
            port = st.text_input("Port", value="5432")
            user = st.text_input("Utilisateur")
            password = st.text_input("Mot de passe", type="password")
            database = st.text_input("Nom de la base de données")
            table = st.text_input("Nom de la table à charger")

            if st.button("Se connecter à PostgreSQL"):
                try:
                    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
                    engine = create_engine(url)
                    with engine.connect() as connection:
                        df = pd.read_sql(f"SELECT * FROM {table}", connection)

                    st.session_state['dataframe'] = df
                    st.session_state['dataframe'] = df
                    st.session_state['original_dataframe'] = df.copy()
                    df = enrich_with_claim_amount(df)
                    st.session_state['final_dataframe'] = df.copy()
                    st.success("✅ Données PostgreSQL chargées.")
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"❌ Erreur PostgreSQL : {e}")

        elif db_type == "MySQL":
            st.subheader("🟨 Connexion MySQL")
            host = st.text_input("Hôte", value="localhost", key="mysql_host")
            port = st.text_input("Port", value="3306", key="mysql_port")
            user = st.text_input("Utilisateur", key="mysql_user")
            password = st.text_input("Mot de passe", type="password", key="mysql_pass")
            database = st.text_input("Nom de la base", key="mysql_db")
            table = st.text_input("Nom de la table", key="mysql_table")

            if st.button("Se connecter à MySQL"):
                try:
                    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
                    engine = create_engine(url)
                    with engine.connect() as conn:
                        df = pd.read_sql(f"SELECT * FROM {table}", conn)

                    st.session_state['dataframe'] = df
                    st.session_state['dataframe'] = df
                    st.session_state['original_dataframe'] = df.copy()
                    df = enrich_with_claim_amount(df)
                    st.session_state['final_dataframe'] = df.copy()
                    st.success("✅ Données PostgreSQL chargées.")
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"❌ Erreur MySQL : {e}")

        elif db_type == "MongoDB":
            st.subheader("🟩 Connexion MongoDB")
            host = st.text_input("Hôte", value="localhost", key="mongo_host")
            port = st.text_input("Port", value="27017", key="mongo_port")
            user = st.text_input("Utilisateur", key="mongo_user")
            password = st.text_input("Mot de passe", type="password", key="mongo_pass")
            database = st.text_input("Nom de la base", key="mongo_db")
            collection_name = st.text_input("Nom de la collection", key="mongo_coll")

            if st.button("Se connecter à MongoDB"):
                try:
                    conn_str = f"mongodb://{user}:{password}@{host}:{port}/"
                    client = MongoClient(conn_str)
                    db = client[database]
                    collection = db[collection_name]
                    data = list(collection.find())
                    df = pd.DataFrame(data)

                    if '_id' in df.columns:
                        df.drop('_id', axis=1, inplace=True)

                    st.session_state['dataframe'] = df
                    st.session_state['dataframe'] = df
                    st.session_state['original_dataframe'] = df.copy()
                    df = enrich_with_claim_amount(df)
                    st.session_state['final_dataframe'] = df.copy()
                    st.success("✅ Données PostgreSQL chargées.")
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"❌ Erreur MongoDB : {e}")


if __name__ == "__main__":
    if 'dataframe' not in st.session_state:
        st.session_state['dataframe'] = None
    if 'original_dataframe' not in st.session_state:
        st.session_state['original_dataframe'] = None
    if 'final_dataframe' not in st.session_state:
        st.session_state['final_dataframe'] = None
    main()