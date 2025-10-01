#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Access_token.py
import sys
from Access_token import get_token
import requests
import pandas as pd
from io import StringIO
from datetime import datetime  
import os



# In[ ]:


import requests
import pandas as pd

# Get the token and request data
token = get_token()


url = "https://api-lng.kpler.com/v1/diversions/columns"



response = requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"},
)

df = pd.read_csv(StringIO(response.text), sep=";")
col_data = df

df

# In[5]:


import requests
import pandas as pd

# Get the token and request data
token = get_token()
params = {
    "size": 100000,
    "columns":
    "charterer_name,"

    "vessel_capacity_cubic_meters,"
    "cargo_origin_cubic_meters,"
    "cargo_origin_tons,"

    "diversion_date,"
    "origin_diversion_date,"

    "new_destination_date,"
    "new_destination_eta,"

    "new_destination_continent_name,"
    "new_destination_subcontinent_name,"
    "new_destination_country_name,"
    "new_destination_installation_name,"
    
    "diverted_from_continent_name,"
    "diverted_from_subcontinent_name,"
    "diverted_from_country_name,"
    "diverted_from_installation_name,"
    
    "origin_diversion_location_name,"
    "origin_diversion_country_name,"
    
    "vessel_state,"
    "vessel_type,"
}

url = "https://api-lng.kpler.com/v1/diversions"


response = requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"},
    params=params
)


df = pd.read_csv(StringIO(response.text), sep=";")
df

# In[6]:


from datetime import datetime
# Save to CSV with timestamp
today_str = datetime.today().strftime("%Y-%m-%d")
output_path = f"data/kpler_diversions_{today_str}.csv"
os.makedirs("data", exist_ok=True)

# Save to CSV
df.to_csv(output_path, index=False)
print(f"✅ Data saved to {output_path}")
