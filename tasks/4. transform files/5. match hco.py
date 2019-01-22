#!/usr/bin/env python
# coding: utf-8

# # 5. Match HCOs
# The magic! Here we match addresses. You can run this file on an external server - it will take some times

# In[3]:


import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import time


# ## Read Data

# In[4]:


df = pd.read_csv('2. list_expanded.csv')
#df = pd.read_csv('../../data/3. transformation/2. list_expanded.csv')
df_hcp = df[df.type == 'hco'].copy()

#Reset index
df_hcp = df_hcp.reset_index(drop=True)

#Set Startindex to 1
df_hcp.index += 1 
len(df_hcp)


# ## Calc rows

# In[5]:


#Add Parent
df_hcp['parent'] = 0
df_hcp['parent'] = df_hcp['parent'].astype(int)

#Convert
df_hcp['name'] = df_hcp['name'].astype("str")
df_hcp['address_expand'] = df_hcp['address_expand'].astype("str")
df_hcp['location_expand'] = df_hcp['location_expand'].astype("str")

start_time = time.time()

for index, row in df_hcp.iterrows():
    if index % 10 == 0:
        print(index)
    #print(index)
    
    #Calculate ratio for each category
    df_hcp.loc[(df_hcp.index >= index), 'r_name'] = df_hcp['name'].apply(lambda x: fuzz.token_set_ratio(x.lower(), row['name'].lower()))
    df_hcp.loc[(df_hcp.index >= index), 'r_location'] = df_hcp['location_expand'].apply(lambda x: fuzz.token_set_ratio(x, row['location_expand']))
    df_hcp.loc[(df_hcp.index >= index), 'r_address'] = df_hcp['address_expand'].apply(lambda x: fuzz.token_set_ratio(x, row['address_expand']))
    
    #Set the rules.
    df_hcp.loc[(df_hcp.r_name >= 80) & (df_hcp.r_location >= 85) & (df_hcp.r_address >= 80), 'parent'] = index
    
elapsed_time = time.time() - start_time
print('Finished in: ' + str(round(elapsed_time / 60, 2)) + ' minutes')


# In[ ]:


df_hcp.to_csv('3. hcp_matches.csv', index=True)
#df_hcp.to_csv('../../data/3. transformation/3. hco_matches.csv', index=True)

