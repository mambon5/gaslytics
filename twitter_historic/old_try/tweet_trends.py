"""
Adapted pipeline: Instead of scraping tweets, we fetch Twitter Trends (topics/hashtags) per day.
This avoids the login wall that blocks tweets scraping.

Flow:
  - Use snscrape TwitterTrends to fetch daily trending topics.
  - Treat trends list as pseudo-"text corpus" per day.
  - Build features from trends (TF-IDF or embeddings).
  - Merge with gas price data.
  - Train MLP or LSTM models as before.

Outputs:
  - results_with_preds.csv or results_classification.csv

Note: Trends are fewer and noisier than tweets, but at least accessible.
"""

import argparse
import os
import sys
import re
import numpy as np
import pandas as pd
import datetime as dt
from tqdm import tqdm

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import yfinance as yf

# optional imports
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE = True
except Exception:
    HAS_SENTENCE = False

# ---------------------------
# Helpers
# ---------------------------

def fetch_daily_trends(start_date, end_date, woeid=1, max_days=1000):
    """
    Fetch Twitter daily trending topics using snscrape.
    woeid=1 is global trends. You can use specific WOEID for regions.
    Returns DataFrame with ['date','trends_text'].
    """
    try:
        import snscrape.modules.twitter as sntwitter
    except Exception as e:
        print("snscrape not installed. Install with: pip install snscrape")
        raise
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    rows = []
    for d in dates:
        try:
            for trend in sntwitter.TwitterTrendsScraper(woeid=woeid, date=d.date()).get_items():
                # trends come as objects with .name
                rows.append({"date": d.date(), "trend": getattr(trend, 'name', str(trend))})
        except Exception:
            continue
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    agg = df.groupby('date').agg(trends_text=('trend', lambda x: " ".join(str(t) for t in x))).reset_index()
    agg['date'] = pd.to_datetime(agg['date'])
    return agg


def get_gas_prices(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=(pd.to_datetime(end_date) + pd.Timedelta(days=1)).strftime("%Y-%m-%d"))
    df = df[['Close']].rename(columns={'Close':'close'}).reset_index()
    df['date'] = pd.to_datetime(df['Date']).dt.date
    df = df[['date','close']]
    df['date'] = pd.to_datetime(df['date'])
    return df


def build_features(price_df, trends_df):
    df = pd.merge(price_df, trends_df, on='date', how='left')
    df = df.sort_values('date').reset_index(drop=True)
    df['trends_text'] = df['trends_text'].fillna('')
    df['ret_1'] = df['close'].pct_change()
    df['target_ret_next'] = df['close'].shift(-1) / df['close'] - 1
    df['target_up_next'] = (df['target_ret_next'] > 0).astype(int)
    return df.dropna(subset=['target_ret_next']).reset_index(drop=True)


def text_to_features_tfidf(corpus, max_features=2000, svd_components=50):
    tfidf = TfidfVectorizer(max_features=max_features)
    X_tfidf = tfidf.fit_transform(corpus)
    svd = TruncatedSVD(n_components=svd_components, random_state=42)
    X_svd = svd.fit_transform(X_tfidf)
    return X_svd


def build_mlp(input_dim, regression=True):
    model = keras.Sequential()
    model.add(layers.Input(shape=(input_dim,)))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dropout(0.2))
    if regression:
        model.add(layers.Dense(1, activation='linear'))
        model.compile(optimizer=keras.optimizers.Adam(1e-3), loss='mse', metrics=['mse'])
    else:
        model.add(layers.Dense(1, activation='sigmoid'))
        model.compile(optimizer=keras.optimizers.Adam(1e-3), loss='binary_crossentropy', metrics=['accuracy'])
    return model

# ---------------------------
# Main
# ---------------------------

def main(args):
    print("1) Fetching daily Twitter trends...")
    trends_df = fetch_daily_trends(args.start, args.end, woeid=args.woeid)
    if trends_df.empty:
        print("No trends fetched.")
        return

    print("2) Downloading gas prices...")
    price_df = get_gas_prices(args.ticker, args.start, args.end)

    print("3) Building features...")
    df = build_features(price_df, trends_df)

    print("4) Vectorizing trends text...")
    X_text = text_to_features_tfidf(df['trends_text'].astype(str).tolist(), max_features=args.max_features, svd_components=args.svd)
    X = X_text
    y_reg = df['target_ret_next'].values
    y_clf = df['target_up_next'].values

    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    ytr_reg, yte_reg = y_reg[:split_idx], y_reg[split_idx:]
    ytr_clf, yte_clf = y_clf[:split_idx], y_clf[split_idx:]

    val_idx = int(0.8 * len(X_train))
    X_tr, X_val = X_train[:val_idx], X_train[val_idx:]
    y_tr_reg, y_val_reg = ytr_reg[:val_idx], ytr_reg[val_idx:]
    y_tr_clf, y_val_clf = ytr_clf[:val_idx], ytr_clf[val_idx:]

    print("Shapes:", X_tr.shape, X_val.shape, X_test.shape)

    if args.classification:
        print("5) Training classifier on trends...")
        model = build_mlp(X.shape[1], regression=False)
        es = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        model.fit(X_tr, y_tr_clf, validation_data=(X_val, y_val_clf), epochs=args.epochs, batch_size=args.batch, callbacks=[es], verbose=2)
        preds = (model.predict(X_test).flatten() > 0.5).astype(int)
        acc = accuracy_score(yte_clf, preds)
        print(f"Classification accuracy: {acc:.4f}")
        print(classification_report(yte_clf, preds))
    else:
        print("5) Training regressor on trends...")
        model = build_mlp(X.shape[1], regression=True)
        es = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        model.fit(X_tr, y_tr_reg, validation_data=(X_val, y_val_reg), epochs=args.epochs, batch_size=args.batch, callbacks=[es], verbose=2)
        preds = model.predict(X_test).flatten()
        mse = mean_squared_error(yte_reg, preds)
        r2 = r2_score(yte_reg, preds)
        print(f"Regression Test MSE: {mse:.6e}, R2: {r2:.4f}")

    print("Done.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gas + Twitter Trends pipeline')
    parser.add_argument('--start', type=str, default='2023-01-01')
    parser.add_argument('--end', type=str, default='2023-12-31')
    parser.add_argument('--ticker', type=str, default='NG=F')
    parser.add_argument('--woeid', type=int, default=1, help='WOEID location id (1=global)')
    parser.add_argument('--classification', action='store_true')
    parser.add_argument('--epochs', type=int, default=20)
    parser.add_argument('--batch', type=int, default=16)
    parser.add_argument('--max-features', type=int, default=2000)
    parser.add_argument('--svd', type=int, default=50)

    args = parser.parse_args()
    main(args)
