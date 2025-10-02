# app per visualitzar els arxius csv generats

import streamlit as st
import pandas as pd
import os

DATA_DIR = "data"

st.title("📊 Navegador de dades Kpler")

# Llista els arxius CSV
files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
files.sort(reverse=True)

file_selected = st.selectbox("Selecciona un fitxer CSV:", files)

if file_selected:
    df = pd.read_csv(os.path.join(DATA_DIR, file_selected))
    st.write(f"Mostrant **{file_selected}** amb {len(df)} files")
    st.dataframe(df)

    # Opcions extra
    st.download_button(
        "Descarregar CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_selected,
        "text/csv"
    )
