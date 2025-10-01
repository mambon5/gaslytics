#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


#sin parametros aparece el total de los inventarios de todos los paises (principalmente europa)
#nos interesa tener un split por: split = "byCountry" y split = "byInstallation"
#{{split}}

#Optional [String]: Splits the inventories data "byCountry" or "byInstallation"

# In[ ]:


token = get_token()

url = "https://api-lng.kpler.com/v1/inventories"
params = {
    "split": "byCountry",
}



response = requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"},
   params=params,
)

df_inv_country = pd.read_csv(StringIO(response.text), sep=";")
df_inv_country

# In[ ]:


token = get_token()

url = "https://api-lng.kpler.com/v1/inventories"
params = {
    "split": "byInstallation",
}

response = requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"},
   params=params,
)

df_inv_install = pd.read_csv(StringIO(response.text), sep=";")
df_inv_install

# In[12]:


# Save to CSV with timestamp
today_str = datetime.today().strftime("%Y-%m-%d")
output_path = f"data/kpler_storages_inv_inst_{today_str}.csv"
os.makedirs("data", exist_ok=True)

# Save to CSV
df_inv_install.to_csv(output_path, index=False)
print(f"✅ Data saved to {output_path}")

# In[16]:


# Save to CSV with timestamp
today_str = datetime.today().strftime("%Y-%m-%d")
output_path = f"data/kpler_storages_inv_countries_{today_str}.csv"
os.makedirs("data", exist_ok=True)

# Save to CSV
df_inv_country.to_csv(output_path, index=False)
print(f"✅ Data saved to {output_path}")

# In[ ]:



