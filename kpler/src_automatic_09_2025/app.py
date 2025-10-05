import streamlit as st
import os
import csv

DATA_DIR = "data"

st.title("📊 Navegador de CSV (Sense Pandas)")


# Llista de fitxers CSV
files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
files.sort(reverse=True)
file_selected = st.selectbox("Selecciona un fitxer CSV:", files)


if file_selected:
    file_path = os.path.join(DATA_DIR, file_selected)

    # Botó per descarregar el CSV complet
    with open(file_path, "rb") as f:
        st.download_button(
            label="Descarregar CSV",
            data=f,
            file_name=file_selected,
            mime="text/csv"
        )

    # Drop-down per seleccionar quantes files mostrar
    num_rows_options = [10, 20, 50, 100, 200, 500, 1000]
    n = st.selectbox("Selecciona quantes files mostrar:", num_rows_options, index=0)  # per defecte 10


    
    # Llegir tot el CSV
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    
    if rows:
        headers = rows[0]
        data = rows[1:(n+1)]  # Mostrar només les primeres n files seleccionades
        
        # Generar taula HTML simple
        table_html = "<table border='1' style='border-collapse: collapse;'><thead><tr>"
        for h in headers:
            table_html += f"<th>{h}</th>"
        table_html += "</tr></thead><tbody>"
        for row in data:
            table_html += "<tr>"
            for cell in row:
                table_html += f"<td>{cell}</td>"
            table_html += "</tr>"
        table_html += "</tbody></table>"

        st.markdown(table_html, unsafe_allow_html=True)



