# gas_tweets_model.py
"""
Pipeline per relacionar tuits amb preu del gas.
- Scrape tweets amb snscrape (per dates i keywords)
- Baixa preus amb yfinance (ticker 'NG=F' per Natural Gas Futures)
- Agrega tuits per dia -> TF-IDF -> SVD
- Combina amb lags de preu i entrena un model Keras (regressió)
"""

import os
import pandas as pd
import numpy as np
import datetime as dt
from tqdm import tqdm

# scraping
import subprocess
import sys

# ML / text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, r2_score

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# finance data
import yfinance as yf

# text processing
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure nltk assets
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# ---------------------------
# CONFIG
# ---------------------------
# Paraules claus per cercar tuits; ajusta al teu idioma/mercat
KEYWORDS = ["natural gas", "gas natural", "NG", "gasprices", "gas price", "gasprices"] 

# Rangs de data (YYYY-MM-DD)
START_DATE = "2021-01-01"
END_DATE   = "2024-12-31"

# Ticker per gas natural futures
GAS_TICKER = "NG=F"

# Paràmetres TF-IDF / SVD
MAX_FEATURES = 5000
SVD_COMPONENTS = 50

# Lags de preu a incloure com a features
PRICE_LAGS = [1, 2, 3, 7]

# Model params
EPOCHS = 30
BATCH_SIZE = 32
VALIDATION_SPLITS = 3

# ---------------------------
# Helpers
# ---------------------------
def scrape_tweets_to_df(keywords, start_date, end_date, csv_path="tweets.csv"):
    """
    Llegeix un CSV amb tweets i filtra per keywords i rang de dates.
    CSV ha de tenir columnes: 'Timestamp', 'Text'
    Retorna DataFrame amb ['date','content'].
    """
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['Timestamp']).dt.date
    df = df.rename(columns={'Text':'content'})

    # Filtra per dates
    start_dt = pd.to_datetime(start_date).date()
    end_dt = pd.to_datetime(end_date).date()
    df = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]

    # Filtra per keywords
    if keywords:
        pattern = "|".join([re.escape(kw) for kw in keywords])
        df = df[df['content'].str.contains(pattern, case=False, na=False)]

    df = df[['date','content']]
    if df.empty:
        print("No hi ha tuits després de filtrar per dates i keywords")
    return df


def clean_text(s):
    s = re.sub(r'http\S+', '', s)  # treu URLs
    s = re.sub(r'@\w+', '', s)     # treu mentions
    s = re.sub(r'#', '', s)        # treu '#'
    s = re.sub(r'[^A-Za-z0-9À-ÿ\s]', ' ', s)  # manté lletres, números i acc., separa símbols
    s = s.lower()
    tokens = word_tokenize(s)
    stops = set(stopwords.words('english')) | set(stopwords.words('spanish'))
    tokens = [t for t in tokens if t not in stops and len(t) > 1]
    return " ".join(tokens)

# ---------------------------
# 1) Obtenir tuits
# ---------------------------
def aggregate_tweets_by_date(tweets_df):
    tweets_df['date'] = pd.to_datetime(tweets_df['date'])
    tweets_df['clean'] = tweets_df['content'].astype(str).map(clean_text)
    agg = tweets_df.groupby(tweets_df['date'].dt.date).agg(
        tweets_list = ('clean', lambda x: " ".join(x)),
        n_tweets = ('clean', 'count'),
        avg_length = ('clean', lambda s: np.mean([len(t.split()) for t in s]) if len(s)>0 else 0)
    ).reset_index().rename(columns={'index':'date'})
    agg['date'] = pd.to_datetime(agg['date'])
    return agg

# ---------------------------
# 2) Obtenir preus del gas
# ---------------------------
def get_gas_prices(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=(pd.to_datetime(end_date) + pd.Timedelta(days=1)).strftime("%Y-%m-%d"))
    df = df[['Close']].rename(columns={'Close':'close'}).reset_index()
    df['date'] = pd.to_datetime(df['Date']).dt.date
    df = df[['date','close']]
    df['date'] = pd.to_datetime(df['date'])
    return df

# ---------------------------
# 3) Construir features
# ---------------------------
def build_features(price_df, tweets_agg):
    # join per data
    df = pd.merge(price_df, tweets_agg, on='date', how='left')
    df = df.sort_values('date').reset_index(drop=True)
    # omple nans de tweets amb 0
    df['tweets_list'] = df['tweets_list'].fillna('')
    df['n_tweets'] = df['n_tweets'].fillna(0)
    df['avg_length'] = df['avg_length'].fillna(0)
    # calc returns
    df['ret_1'] = df['close'].pct_change()
    # lags de preu
    for lag in PRICE_LAGS:
        df[f'close_lag_{lag}'] = df['close'].shift(lag)
        df[f'ret_lag_{lag}'] = df['ret_1'].shift(lag)
    # target: next-day return
    df['target_ret_next'] = df['close'].shift(-1) / df['close'] - 1
    return df

# ---------------------------
# 4) Text -> vector
# ---------------------------
def text_to_features(corpus, max_features=MAX_FEATURES, svd_components=SVD_COMPONENTS):
    tfidf = TfidfVectorizer(max_features=max_features)
    X_tfidf = tfidf.fit_transform(corpus)
    svd = TruncatedSVD(n_components=svd_components, random_state=42)
    X_svd = svd.fit_transform(X_tfidf)
    return X_svd, tfidf, svd

# ---------------------------
# 5) Model (Keras)
# ---------------------------
def build_and_train_model(X_train, y_train, X_val, y_val, input_dim):
    # simpla MLP
    model = keras.Sequential([
        layers.Input(shape=(input_dim,)),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(1, activation='linear')
    ])
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                  loss='mse',
                  metrics=['mse'])
    es = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    history = model.fit(X_train, y_train, validation_data=(X_val, y_val),
                        epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=[es], verbose=2)
    return model, history

# ---------------------------
# MAIN
# ---------------------------
def main():
    print("1) Scraping tweets (pot trigar segons quantitat)...")
    tweets_df = scrape_tweets_to_df(KEYWORDS, START_DATE, END_DATE, csv_path="twitter_dataset.csv")

    if tweets_df.empty:
        print("No hi ha tuits; surt.")
        return
    tweets_agg = aggregate_tweets_by_date(tweets_df)
    print(f"Dates amb tuits: {len(tweets_agg)}")

    print("2) Descarregar preus del gas...")
    price_df = get_gas_prices(GAS_TICKER, START_DATE, END_DATE)
    print(f"Preus: {len(price_df)} dies")

    print("3) Construir features base i unir dades...")
    df = build_features(price_df, tweets_agg)
    # Retira files sense target
    df = df.dropna(subset=['target_ret_next']).reset_index(drop=True)
    print(f"Files després de preparar: {len(df)}")

    print("4) Transformar text a vectors (TF-IDF + SVD)...")
    X_text, tfidf_obj, svd_obj = text_to_features(df['tweets_list'].astype(str).tolist())
    print("Text -> dims:", X_text.shape)

    # Build tabular features
    tab_feats = ['n_tweets', 'avg_length'] + [f'close_lag_{l}' for l in PRICE_LAGS] + [f'ret_lag_{l}' for l in PRICE_LAGS]
    X_tab = df[tab_feats].fillna(0).values
    # standardize numeric
    scaler = StandardScaler()
    X_tab = scaler.fit_transform(X_tab)

    # combine
    X = np.hstack([X_text, X_tab])
    y = df['target_ret_next'].values

    # Train/test split temporal
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # further split train->val
    val_idx = int(0.8 * len(X_train))
    X_tr, X_val = X_train[:val_idx], X_train[val_idx:]
    y_tr, y_val = y_train[:val_idx], y_train[val_idx:]

    print("Shapes:", X_tr.shape, X_val.shape, X_test.shape)

    print("5) Entrenar model Keras (MLP)...")
    model, history = build_and_train_model(X_tr, y_tr, X_val, y_val, input_dim=X.shape[1])

    print("6) Avaluar sobre test set...")
    y_pred = model.predict(X_test).flatten()
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Test MSE: {mse:.6e}, RMSE: {np.sqrt(mse):.6e}, R2: {r2:.4f}")

    # Avaluació bàsica direccional (up/down)
    dir_true = (y_test > 0).astype(int)
    dir_pred = (y_pred > 0).astype(int)
    acc = (dir_true == dir_pred).mean()
    print(f"Accuracy direccional (up/down): {acc:.3f}")

    # Append results a df per dia per visió
    results_df = df.iloc[split_idx:].copy()
    results_df['pred_ret'] = y_pred
    results_df['true_ret'] = y_test
    # guardar
    results_df.to_csv("results_with_preds.csv", index=False)
    print("Resultats guardats a results_with_preds.csv")

    print("Fet.")

if __name__ == "__main__":
    main()
