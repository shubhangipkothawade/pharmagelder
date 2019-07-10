#%% [markdown]
# # Match Address - Run twice! Multithreading
# Match addresses witouth a parent. Perhaps there is a sibling in the same year inside?
# The magic! Here we match addresses. You can run this file on an external server - it will take some times.  
# **You have to run this twice, for hcp and hco's! Change the variable `run_for`**
# 
# **Info next time: Try to set condition_address to 0 on HCO. To many not found pairs**

#%%
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import time
import sys
import os.path
import datetime
import multiprocessing as mp
import math


#%%
run_for = 'hco'
version = 0.5
num_process = mp.cpu_count() * 2

# Conditions
conditions = {
    'hcp' :
        {
            'condition_location': 85,
            'condition_address': 0,
            'condition_name': 89
        },
    'hco' :
        {
            'condition_location': 85,
            'condition_address': 0,
            'condition_name': 85
        },
    }

#%% [markdown]
# ## Check path
# Check, if we run in in the git directory or on the server. If on a server, look for the files in the same directory

#%%
#Check Server or Git
path_git = '../../data/3. transformation/4_%s_matched_against_live.csv'
path_server = '4_%s_matched_against_live.csv'

on_git = os.path.isfile(path_git % run_for)

#%% [markdown]
# ## Read Data

#%%
if on_git:
    df = pd.read_csv(path_git % run_for)
else:
    df = pd.read_csv(path_server % run_for)

df_data = df[df.type == run_for].copy()
df_data['address'] = df_data['address'].fillna("")

#For Testing
#df_data = df_data[df_data.source.isin(['eli', 'shire', 'almirall'])]

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
print("Start fuzzy matcher THREADS %s %s" % (run_for, version))
print("Cores detected: %s" % mp.cpu_count())
print("Threads started: %s" % num_process)
print("Rows to match: %s" % total_rows)
print("Start time: %s" % datetime.datetime.now())
print("===============================")

def run(datasets):
    print("Thread started")
    df_data = datasets['df_data']
    df_part = datasets['df_part']
    
    #create empty matchlist
    df_matchlist = pd.DataFrame(columns=['source', 'target', 'r_name', 'r_address', 'r_location', 'r_ratio'])
    
    counter = 0
    total_rows = len(df_part)
    for index, row in df_part.iterrows():

        #Frist Fuzzynize only location
        df_data['r_location'] = 0
        df_data['r_address'] = 0
        df_data['r_name'] = 0

        df_data['r_location'] = df_data['location_expand'].apply(lambda x: fuzz.token_set_ratio(x, row['location_expand']))

        #Fuzzy name, when r_location >= 85

        df_data['r_name'] = df_data.loc[df_data.r_location >= cond['condition_location'], 'name_expand'].apply(lambda x: fuzz.token_set_ratio(x.lower(), row['name_expand']))

        #Fuzzy address, when r_location > 85 & r_name >= 80
        df_data['r_address'] = df_data.loc[(df_data.r_location >= cond['condition_location']) & (df_data.r_name >= cond['condition_name']), 'address_expand'].apply(lambda x: np.amax([fuzz.token_set_ratio(x, row['address_expand']), fuzz.partial_ratio(x, row['address_expand'])]))

        #condition_fix = (df_data.index != index) & (df_data['parent'] != index)
        condition_fix = (df_data.index != index)
        if row['address'] == '':
            condition1 = (df_data.r_name >= cond['condition_name']) & (df_data.r_location >= cond['condition_location']) & (condition_fix)
        else:
            condition1 = (df_data.r_name >= cond['condition_name']) & (df_data.r_location >= cond['condition_location']) & (df_data.r_address >= cond['condition_address']) & (condition_fix)

        #Select by condition
        df_matches = df_data[(condition1)]

        #Matchlist Add to matchlist
        if len(df_matches) > 0:
            for match_index, match_row in df_matches.iterrows():

                df_matchlist = df_matchlist.append({'source': row['internalid'], 
                                                    'target': match_row['internalid'],
                                                    'r_name': match_row['r_name'],
                                                    'r_address': match_row['r_address'],
                                                    'r_location': match_row['r_location'],
                                                   }, ignore_index=True)


        if counter % 10 == 0:
            sys.stdout.write("\rProgress: %s%%" % round(100 / total_rows * counter, 2))
            sys.stdout.flush()
                
        counter += 1

    #elapsed_time = time.time() - start_time
    #print('\nFinished in: ' + str(round(elapsed_time / 60, 2)) + ' minutes')
    return df_matchlist
    

#Create pool
pool = mp.Pool(processes = num_process)

#Create Jobs
jobs = []
df_selection = df_data[df_data.parent == -1]
job_len = int(math.ceil(len(df_selection) / num_process))
for x in range(0, num_process):
    part = df_selection[x * job_len : x * job_len + job_len]
    jobs.append({"df_data": df_data.copy(), "df_part": part})
    print('Thread Data len: ' + str(len(part)))

    
print("Total len: " + str(len(df_selection)))
print("")

#Run Threats 
matchlist_list = pool.map(run, jobs)
pool.close()
pool.join()

#Concat Results
ds_matchlist_new = pd.concat(matchlist_list)
#print(str(len(matchlist_list)))
print("")
print("len ds_matchlist_new " + str(len(ds_matchlist_new)))

#Time Spend
elapsed_time = time.time() - start_time

print('\nFinished in: ' + str(round(elapsed_time / 60, 2)) + ' minutes')
    


#%%
#Drop columns
#df_data.drop(['r_name', 'r_location', 'r_address'], axis=1, inplace=True)


#%%
if on_git:
    #df_data.to_csv('../../data/3. transformation/5_%s_matches_final.csv' % run_for, index=False)
    ds_matchlist_new.to_csv('../../data/3. transformation/5_%s_matchlist.csv' % run_for, index=False)
else:
    #df_data.to_csv('5_%s_matches_final.csv' % run_for, index=False)
    ds_matchlist_new.to_csv('5_%s_matchlist.csv' % run_for, index=False)


#%%



