#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Access_token.py
import sys
from Access_token import get_token

# In[4]:


import requests
import pandas as pd
from io import StringIO
import json
from datetime import datetime
import os

# Get the token and request data
token = get_token()


url = "https://api-lng.kpler.com/v1/installations"


response = requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"},
)

df = pd.read_csv(StringIO(response.text), sep=";")
df

# In[5]:


# Save to CSV with timestamp
today_str = datetime.today().strftime("%Y-%m-%d")
output_path = f"data/kpler_installations_{today_str}.csv"
os.makedirs("data", exist_ok=True)

# Save to CSV
df.to_csv(output_path, index=False)
print(f"✅ Data saved to {output_path}")
