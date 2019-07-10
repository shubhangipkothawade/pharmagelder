#%% [markdown]
# # Match Address - Run twice! Multithreading
# The magic! Here we match addresses. You can run this file on an external server - it will take some times.  
# Changed logic in new version: No network anymore. Just find the most similar sibling in the live db files.   
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
#num_process = 1

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
git_live = '../../data/0. live data/1_recipient_expanded.csv'
git_new = '../../data/3. transformation/3_list_expanded.csv'

server_live = '1_recipient_expanded.csv'
server_new = '3_list_expanded.csv'

on_git = os.path.isfile(git_new)

#%% [markdown]
# ## Read Data

#%%
if on_git:
    df_live = pd.read_csv(git_live)
    df_new = pd.read_csv(git_new)
else:
    df_live = pd.read_csv(server_live)
    df_new = pd.read_csv(server_new)

df_live = df_live[df_live.type == run_for].copy()
df_new = df_new[df_new.type == run_for].copy()
df_new['address'] = df_new['address'].fillna("")

#For Testing
#df_new = df_new[df_new.source.isin(['eli', 'shire', 'almirall'])]
#df_new = df_new[df_new.source.isin(['eli'])]
#df_new = df_new[df_new['name'] == 'Calderari Gianluca']

#Reset index
df_new = df_new.reset_index(drop=True)

#Set Startindex to 1
df_new['parent'] = -1

total_rows = len(df_new)

#%% [markdown]
# ## Calc rows

#%%
#Convert
df_new['name_expand'] = df_new['name_expand'].astype("str")
df_new['address_expand'] = df_new['address_expand'].astype("str")
df_new['location_expand'] = df_new['location_expand'].astype("str")

df_live['name_expand'] = df_live['name_expand'].astype("str")
df_live['address_expand'] = df_live['address_expand'].astype("str")
df_live['location_expand'] = df_live['location_expand'].astype("str")

#Sort
df_new = df_new.sort_values('name_expand')

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
    df_live = datasets['df_live']
    df_part = datasets['df_part']

    #create empty matchlist
    #df_matchlist = pd.DataFrame(columns=['source', 'target', 'r_name', 'r_address', 'r_location', 'r_ratio'])
    
    counter = 0
    total_rows = len(df_part)
    for index, row in df_part.iterrows():
        #try:
            #Frist Fuzzynize only location
            df_live['r_location'] = 0
            df_live['r_address'] = 0
            df_live['r_name'] = 0
            df_live['r_sum'] = 0

            df_live['r_location'] = df_live['location_expand'].apply(lambda x: fuzz.token_set_ratio(x, row['location_expand']))

            #Fuzzy name, when r_location >= 85
            df_live['r_name'] = df_live.loc[df_live.r_location >= cond['condition_location'], 'name_expand'].apply(lambda x: fuzz.token_set_ratio(x.lower(), row['name_expand']))

            #Fuzzy address, when r_location > 85 & r_name >= 80
            df_live['r_address'] = df_live.loc[(df_live.r_location >= cond['condition_location']) & (df_live.r_name >= cond['condition_name']), 'address_expand'].apply(lambda x: np.amax([fuzz.token_set_ratio(x, row['address_expand']), fuzz.partial_ratio(x, row['address_expand'])]))

            df_live['r_sum'] = df_live['r_location'] + df_live['r_address'] + df_live['r_name']

            #condition_fix = (df_data.index != index) & (df_data['parent'] != index)
            if row['address'] == '':
                condition1 = (df_live.r_name >= cond['condition_name']) & (df_live.r_location >= cond['condition_location'])
            else:
                condition1 = (df_live.r_name >= cond['condition_name']) & (df_live.r_location >= cond['condition_location']) & (df_live.r_address >= cond['condition_address'])

            #Select by condition
            df_matches = df_live[(condition1)]
            if len(df_matches > 0):
                df_part.loc[index, 'parent'] = int(df_matches.nlargest(1, 'r_sum')['id'])

            if counter % 10 == 0:
                sys.stdout.write("\rProgress: %s%%" % round(100 / total_rows * counter, 2))
                sys.stdout.flush()

            counter += 1
            
        #except:
            #print("ERROR")
            #print(row['name_expand'] + ' ' + row['location_expand'] + ' ' + row['address_expand'])
            #raise

    #elapsed_time = time.time() - start_time
    #print('\nFinished in: ' + str(round(elapsed_time / 60, 2)) + ' minutes')
    return df_part


#%%
#Create pool
pool = mp.Pool(processes = num_process)

#Create Jobs
jobs = []
job_len = int(math.ceil(len(df_new) / num_process))
for x in range(0, num_process):
    part = df_new[x * job_len : x * job_len + job_len]
    jobs.append({"df_live": df_live.copy(), "df_part": part})
    print('Thread Data len: ' + str(len(part)))

    
print("Total len: " + str(len(df_new)))
print("")

#Run Threats 
matchlist_list = pool.map(run, jobs)
pool.close()
pool.join()

#Concat Results
df_matches = pd.concat(matchlist_list)
#print(str(len(matchlist_list)))
print("")

#Time Spend
elapsed_time = time.time() - start_time

print('\nFinished in: ' + str(round(elapsed_time / 60, 2)) + ' minutes')


#%%
if on_git:
    df_matches.to_csv('../../data/3. transformation/4_%s_matched_against_live.csv' % run_for, index=False)
else:
    df_matches.to_csv('4_%s_matched_against_live.csv' % run_for, index=False)


#%%



