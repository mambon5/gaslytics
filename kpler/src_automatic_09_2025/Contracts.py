#!/usr/bin/env python
# coding: utf-8

# In[10]:


# Access_token.py
import sys
from Access_token import get_token
import requests
import pandas as pd
from io import StringIO
from datetime import datetime  
import os


# In[ ]:


# Get the token and request data
token = get_token()


url = "https://api-lng.kpler.com/v1/contracts"


response = requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"},
    #params=params
)


df = pd.read_csv(StringIO(response.text), sep=";")
df

# In[11]:


from datetime import datetime
# Save to CSV with timestamp
today_str = datetime.today().strftime("%Y-%m-%d")
output_path = f"data/kpler_contracts_{today_str}.csv"
os.makedirs("data", exist_ok=True)

# Save to CSV
df.to_csv(output_path, index=False)
print(f"✅ Data saved to {output_path}")
