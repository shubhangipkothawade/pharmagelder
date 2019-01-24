#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataSciece.changeDirOnImportExport setting
#%% [markdown]
# # 1. Match HCOs
# The magic! Here we match addresses. You can run this file on an external server - it will take some times

#%%
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import time

#%% [markdown]
# ## Read Data

#%%
#f = pd.read_csv('2. list_expanded.csv')
d#f = pd.read_csv('../../data/3. transformation/2_list_expanded.csv')
df_hcp = df[df.type == 'hco'].copy()
df_hcp['address'] = df_hcp['address'].fillna("")

#For Testing
#df_hcp = df_hcp[df_hcp.source.isin(['eli', 'shire', 'almirall'])]

#Reset index
df_hcp = df_hcp.reset_index(drop=True)

#Set Startindex to 1
df_hcp.index += 1
len(df_hcp)

#%% [markdown]
# ## Calc rows

#%%
#Add Parent
df_hcp['parent'] = 0
df_hcp['parent'] = df_hcp['parent'].astype(int)
df_hcp['parent'] = df_hcp.index

#Convert
df_hcp['name'] = df_hcp['name'].astype("str")
df_hcp['address_expand'] = df_hcp['address_expand'].astype("str")
df_hcp['location_expand'] = df_hcp['location_expand'].astype("str")

df_hcp['concat'] = df_hcp['name'] + ' ' + df_hcp['location_expand']

#Sort
df_hcp = df_hcp.sort_values('name')


start_time = time.time()

counter = 0
for index, row in df_hcp.iterrows():
    
    if counter % 10 == 0:
        print(counter)
    #print(counter)

    """
    #Works!
    df_hcp['r_name'] = df_hcp['name'].apply(lambda x: fuzz.token_set_ratio(x.lower(), row['name'].lower()))
    df_hcp['r_location'] = df_hcp['location_expand'].apply(lambda x: fuzz.token_set_ratio(x, row['location_expand']))
    df_hcp['r_address'] = df_hcp['address_expand'].apply(lambda x: fuzz.token_set_ratio(x, row['address_expand']))
    df_hcp['r_ratio'] = df_hcp['r_name'] + df_hcp['r_location']# + df_hcp['r_address']
    
    highest_match = df_hcp[(df_hcp.r_name > 80) & (df_hcp.r_location > 85) & (df_hcp.index != index)].nlargest(1, columns=['r_ratio'])
    if len(highest_match) == 1:
        df_hcp.loc[index, 'parent'] = highest_match.iloc[0].name
    """
        
        
    df_hcp['r_name'] = df_hcp['name'].apply(lambda x: fuzz.token_set_ratio(x.lower(), row['name'].lower()))
    df_hcp['r_location'] = df_hcp['location_expand'].apply(lambda x: fuzz.token_set_ratio(x, row['location_expand']))
    df_hcp['r_address'] = df_hcp['address_expand'].apply(lambda x: fuzz.token_set_ratio(x, row['address_expand']))
    df_hcp['r_ratio'] = df_hcp['r_name'] + df_hcp['r_location'] + df_hcp['r_address']
    
    condition_fix = (df_hcp.index != index) & (df_hcp['parent'] != index)
    condition1 = (df_hcp.r_ratio > 240) & (df_hcp.r_location > 85) & (condition_fix)
    condition2 = (df_hcp.r_name > 80) & (df_hcp.r_location > 85) & (condition_fix)
    highest_match = df_hcp[(condition1) | (condition2)].nlargest(1, columns=['r_ratio'])
    if len(highest_match) == 1:
        df_hcp.loc[index, 'parent'] = highest_match.iloc[0].name
    
    counter += 1
elapsed_time = time.time() - start_time
print('Finished in: ' + str(round(elapsed_time / 60, 2)) + ' minutes')


#%%
df_hcp.to_csv('3. hco_matches.csv', index=True)
#df_hcp.to_csv('../../data/3. transformation/3_hco_matches.csv', index=True)


#%%
"""
import sys
sys.path.insert(0, '../../data/lib/')

import numpy as np
import pandas as pd
import importlib

import pdfexport
importlib.reload(pdfexport)

from pdfexport import *


df_index = df_hcp.set_index([df_hcp.parent, df_hcp.index])
df_index.head()

write_to_excel(df_hcp, 'tmp.xlsx', open=True, index=True)
"""


