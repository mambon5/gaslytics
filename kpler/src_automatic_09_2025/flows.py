#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Access_token.py
import sys
from Access_token import get_token
import requests
import pandas as pd
from io import StringIO
import json
from datetime import datetime
import os

# In[ ]:


token = get_token()

url = "https://api-lng.kpler.com/v1/flows"
params = {
    "flowDirection": "import",
    "split": "Destination Countries",
    "granularity": "daily",
    "startDate": "2016-01-01",
    "endDate": datetime.now().strftime("%Y-%m-%d"),
    "unit": "cm",
    "withIntraCountry": "true",
    "withForecast": "true",
    #"toZones": "Europe",
    }

"""
Required [String]: Use following splits: ["Total", " Grades", " Products", " Origin Countries",
" Destination Countries", " Origin Continents", " Destination Continents",
" Origin Subcontinents", " Destination Subcontinents", " Origin Trading Regions",
" Destination Trading Regions", " Origin Ports", " Destination Ports", " Origin Installations",
" Destination Installations", " Vessel Type", " Trade Status", " Sources", " Charterers",
" Buyer", " Seller", " Routes", "Trade Type"]
"""

response = requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"},
    params=params,
)

df = pd.read_csv(StringIO(response.text), sep=";")
df

# In[25]:


# Save to CSV with timestamp
today_str = datetime.today().strftime("%Y-%m-%d")
output_path = f"data/kpler_flows_{today_str}.csv"
os.makedirs("data", exist_ok=True)

# Save to CSV
df.to_csv(output_path, index=False)
print(f"✅ Data saved to {output_path}")
