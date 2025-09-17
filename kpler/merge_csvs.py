import os
import pandas as pd

BASE_DIR = "news_data"   # carpeta amb any/mes/dia.csv
OUTPUT_FILE = "all_news.csv"

all_dfs = []

# Recorre totes les subcarpetes (any/mes)
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)
            try:
                df = pd.read_csv(file_path)
                df["SourceFile"] = file_path  # opcional: guardar d’on ve
                all_dfs.append(df)
            except Exception as e:
                print(f"⚠️ No s'ha pogut llegir {file_path}: {e}")

if all_dfs:
    merged_df = pd.concat(all_dfs, ignore_index=True)

    # Ordenar per data si existeix la columna "Date"
    if "Date" in merged_df.columns:
        merged_df["Date"] = pd.to_datetime(merged_df["Date"], errors="coerce")
        merged_df = merged_df.sort_values(by="Date")

    merged_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"✅ Fitxer combinat creat: {OUTPUT_FILE} ({len(merged_df)} notícies)")
else:
    print("⚠️ No s'han trobat CSVs per ajuntar.")
