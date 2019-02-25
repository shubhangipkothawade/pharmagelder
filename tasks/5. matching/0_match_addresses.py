#%% [markdown]
# # Match Address - Run twice!
# The magic! Here we match addresses. You can run this file on an external server - it will take some times.  
# **You have to run this twice, for hcp and hco's! Change the variable `run_for`**

#%%
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import time
import sys
import os.path
import datetime


#%%
run_for = 'hcp'
version = 0.3

# Conditions
conditions ={
    'hcp' :
        {
            'condition_location': 85,
            'condition_address': 75,
            'condition_name': 85
        },
    'hco' :
        {
            'condition_location': 85,
            'condition_address': 75,
            'condition_name': 85
        },
    }

#%% [markdown]
# ## Check path
# Check, if we run in in the git directory or on the server. If on a server, look for the files in the same directory

#%%
#Check Server or Git
path_git = '../../data/3. transformation/3_list_expanded.csv'
path_server = '3_list_expanded.csv'

on_git = os.path.isfile(path_git)

#%% [markdown]
# ## Read Data

#%%
if on_git:
    df = pd.read_csv(path_git)
else:
    df = pd.read_csv(path_server)

df_data = df[df.type == run_for].copy()
df_data['address'] = df_data['address'].fillna("")

#For Testing
#df_data = df_data[df_data.source.isin(['eli', 'shire', 'almirall'])]

#Reset index
df_data = df_data.reset_index(drop=True)

#Set Startindex to 1
df_data.index += 1

#create empty matchlist
df_matchlist = pd.DataFrame(columns=['source', 'target', 'r_name', 'r_address', 'r_location', 'r_ratio'])

total_rows = len(df_data)

#%% [markdown]
# ## Calc rows

#%%
#Convert
df_data['name_expand'] = df_data['name_expand'].astype("str")
df_data['address_expand'] = df_data['address_expand'].astype("str")
df_data['location_expand'] = df_data['location_expand'].astype("str")

#Sort
df_data = df_data.sort_values('name_expand')

cond = conditions[run_for]

start_time = time.time()

print("===============================")
print("Start fuzzy matcher %s %s" % (run_for, version))
print("Rows to match: %s" % total_rows)
print("Start time: %s" % datetime.datetime.now())
print("===============================")

counter = 0
for index, row in df_data.iterrows():
    
    if counter % 10 == 0:
        sys.stdout.write("\rProgress: %s%%" % round(100 / total_rows * counter, 2))
        sys.stdout.flush()
        
    #Frist Fuzzynize only location
    df_data['r_location'] = 0
    df_data['r_address'] = 0
    df_data['r_name'] = 0
    
    df_data['r_location'] = df_data['location_expand'].apply(lambda x: fuzz.token_set_ratio(x, row['location_expand']))
    
    #Fuzzy name, when r_location >= 85
    
    df_data['r_name'] = df_data.loc[df_data.r_location >= cond['condition_location'], 'name_expand'].apply(lambda x: fuzz.token_set_ratio(x.lower(), row['name_expand']))
    
    #Fuzzy address, when r_location > 85 & r_name >= 80
    df_data['r_address'] = df_data.loc[(df_data.r_location >= cond['condition_location']) & (df_data.r_name >= cond['condition_name']), 'address_expand'].apply(lambda x: fuzz.token_set_ratio(x, row['address_expand']))
    
    #condition_fix = (df_data.index != index) & (df_data['parent'] != index)
    condition_fix = (df_data.index != index)
    if row['address'] == '':
        condition1 = (df_data.r_name >= cond['condition_name']) & (df_data.r_location >= cond['condition_location']) & (condition_fix)
    else:
        condition1 = (df_data.r_name >= cond['condition_name']) & (df_data.r_location >= cond['condition_location']) & (df_data.r_address >= cond['condition_address']) & (condition_fix)
    
    #Select by condition
    df_matches = df_data[(condition1)]
    
    #Matchlist Add to matchlist
    if len(df_matches) == 0:
        df_matchlist = df_matchlist.append({'source': index,
                                            'target': index,
                                            'r_name': 100,
                                            'r_address': 100,
                                            'r_location': 100,
                                           }, ignore_index=True)
    else:
        for match_index, match_row in df_matches.iterrows():

            df_matchlist = df_matchlist.append({'source': index, 
                                                'target': match_index,
                                                'r_name': match_row['r_name'],
                                                'r_address': match_row['r_address'],
                                                'r_location': match_row['r_location'],
                                               }, ignore_index=True)

    
    counter += 1

elapsed_time = time.time() - start_time
print('\nFinished in: ' + str(round(elapsed_time / 60, 2)) + ' minutes')


#%%
#Drop columns
#df_data.drop(['r_name', 'r_location', 'r_address'], axis=1, inplace=True)


#%%
if on_git:
    df_data.to_csv('../../data/3. transformation/4_%s_matches.csv' % run_for, index=True)
    df_matchlist.to_csv('../../data/3. transformation/4_%s_matchlist.csv' % run_for, index=False)
else:
    df_data.to_csv('4_%s_matches.csv' % run_for, index=True)
    df_matchlist.to_csv('4_%s_matchlist.csv' % run_for, index=False)


#%%



