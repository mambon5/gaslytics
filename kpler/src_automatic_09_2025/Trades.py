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



token = get_token()
params = {
    "columns":
    "start,"
    "end,"
    "origin_country_name,"
    "destination_country_name,"
    "initial_seller_name,"
    "final_buyer_name,"
    "installation_origin_name,"      #Terminal
    "installation_destination_name,"
    "cargo_origin_cubic_meters,"
    "cargo_origin_tons,"
    "next_forecasted_destination_location_name,"
    "next_forecasted_destination_location_eta,"
    "next_forecasted_destination_confidence,"             # Volume in m3 (origin)
    "status,"
    "trade_link_1_seller_name,"
    "trade_link_2_seller_name,"
    "trade_link_3_seller_name,"
    "trade_link_4_seller_name,"
    "trade_link_5_seller_name,"
    "trade_link_1_buyer_name,"
    "trade_link_2_buyer_name,"
    "trade_link_3_buyer_name,"
    "trade_link_4_buyer_name,"
    "trade_link_5_buyer_name,"
    "trade_link_1_type,"

}

url = "https://api-lng.kpler.com/v1/trades"


response = requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"},
    params=params
)


df = pd.read_csv(StringIO(response.text), sep=";")
df

# In[ ]:


from datetime import datetime
# Save to CSV with timestamp
today_str = datetime.today().strftime("%Y-%m-%d")
output_path = f"data/kpler_trades_{today_str}.csv"
os.makedirs("data", exist_ok=True)

# Save to CSV
df.to_csv(output_path, index=False)
print(f"✅ Data saved to {output_path}")
