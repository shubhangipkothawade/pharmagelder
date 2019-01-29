#%% [markdown]
# # 0. Match HCPs
# The magic! Here we match addresses. You can run this file on an external server - it will take some times

#%%
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import time
import sys
import os.path


#%%
version = 0.2

#%% [markdown]
# ## Check path
# Check, if we run in in the git directory or on the server. If on a server, look for the files in the same directory

#%%
#Check Server or Git
path_git = '../../data/3. transformation/2_list_expanded.csv'
path_server = '2_list_expanded.csv'

on_git = os.path.isfile(path_git)

#%% [markdown]
# ## Read Data

#%%
if on_git:
    df = pd.read_csv(path_git)
else:
    df = pd.read_csv(path_server)

df_data = df[df.type == 'hcp'].copy()
df_data['address'] = df_data['address'].fillna("")

#For Testing
df_data = df_data[df_data.source.isin(['eli', 'shire', 'almirall'])]

#Reset index
df_data = df_data.reset_index(drop=True)

#Set Startindex to 1
df_data.index += 1

total_rows = len(df_data)

#%% [markdown]
# ## Calc rows

#%%
#Add Parent
df_data['parent'] = 0
df_data['parent'] = df_data['parent'].astype(int)
df_data['parent'] = df_data.index

#Convert
df_data['name'] = df_data['name'].astype("str")
df_data['address_expand'] = df_data['address_expand'].astype("str")
df_data['location_expand'] = df_data['location_expand'].astype("str")

#Sort
df_data = df_data.sort_values('name')

start_time = time.time()

print("===============================")
print("Start fuzzy matcher HCP %s" % version)
print("Rows to match: %s" % total_rows)
print("===============================")

counter = 0
for index, row in df_data.iterrows():
    
    if counter % 10 == 0:
        sys.stdout.write("\rProgress: %s%%" % round(100 / total_rows * counter, 2))
        sys.stdout.flush()
        
    df_data['r_name'] = df_data['name'].apply(lambda x: fuzz.token_set_ratio(x.lower(), row['name'].lower()))
    df_data['r_location'] = df_data['location_expand'].apply(lambda x: fuzz.token_set_ratio(x, row['location_expand']))
    df_data['r_address'] = df_data['address_expand'].apply(lambda x: fuzz.token_set_ratio(x, row['address_expand']))
    df_data['r_ratio'] = df_data['r_name'] + df_data['r_location'] + df_data['r_address']
    
    condition_fix = (df_data.index != index) & (df_data['parent'] != index)
    if row['address'] == '':
        condition1 = (df_data.r_name >= 80) & (df_data.r_location >= 85) & (condition_fix)
    else:
        condition1 = (df_data.r_name >= 80) & (df_data.r_location >= 85) & (df_data.r_address >= 75) & (condition_fix)
    
    highest_match = df_data[(condition1)].nlargest(1, columns=['r_ratio'])
    if len(highest_match) == 1:
        df_data.loc[index, 'parent'] = highest_match.iloc[0].name
        df_data.loc[index, 'log'] = "name=%s,location=%s,address=%s,total=%s" % (highest_match.iloc[0].r_name, highest_match.iloc[0].r_location, highest_match.iloc[0].r_address, highest_match.iloc[0].r_ratio)
    
    counter += 1

elapsed_time = time.time() - start_time
print('\nFinished in: ' + str(round(elapsed_time / 60, 2)) + ' minutes')


#%%
if on_git:
    df_data.to_csv('../../data/3. transformation/3_hcp_matches.csv', index=True)
else:
    df_data.to_csv('3_hcp_matches.csv', index=True)

