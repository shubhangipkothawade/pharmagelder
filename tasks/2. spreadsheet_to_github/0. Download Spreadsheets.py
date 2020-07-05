#%% [markdown]
# # Download Spreadsheets
# This script downloads all Spreadsheets, saves them to the corresponding folder and push it to git. The spreadsheet-ID has to be in the spreadsheet_connections-list: https://docs.google.com/spreadsheets/d/1nla4bvR16WsYxBt--I1qBRqEaLZn1yNXA6gFV79qRjQ/edit#gid=0
#   
# **The get the spreadsheet-id, open the spreadsheet and:**
# * Datei (file)
# * Im Web veröffentlichen (publish to the web)
# * Chose the corresponding sheet and "csv"
# * copy the url
# 
# The spreadsheet_connection-list must look like this:
# 
# name | list | accumulation
# --- | --- | ---
# name of company | id of list | id of accumulation
# Example | --- | ---
# abbvie | url | url
#%% [markdown]
# ## Import

#%%
import pandas as pd
import urllib.request
import numpy as np
import os
import sys
import git

#%% [markdown]
# ## Consts

#%%
#URL to the connection spreadsheet
ID_CONNECTION_SHEET = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSLiBEZgbLzI0z0rb__qVc_j8IvjdHLgYxtdaDDWjLLImA_pYDAWv7B_RHE13VaikkhFSc1KjgOyCHH/pub?gid=0&single=true&output=csv'
EXPORT_FOLDER = '/data/python/pharmagelder/repo/data/2. manual check/%s/'
GIT_REPOSITORY = '/data/python/pharmagelder//repo'
GIT_COMMIT_DETECTION = '/data/python/pharmagelder/repo/data/2. manual check/*.csv'

#Templates
#SHEET_URL = 'https://docs.google.com/spreadsheets/d/e/%s/pub?output=csv'


#%%
def log(value):
    #display(Markdown(value))
    print(value)

#%% [markdown]
# ## Sync folder

#%%
#Init repo
repo = git.Repo(GIT_REPOSITORY)

#Fetch repo
log("Pull from git")
#repo.remotes.origin.fetch()
repo.git.pull()


#%%
#Load Connection Sheet
log("Download Connection-Sheet")
df = pd.read_csv(ID_CONNECTION_SHEET)
df = df.fillna("")


#%%
def load_file(_id, _name, _subfolder):
    ullfilename = os.path.join(EXPORT_FOLDER % _subfolder, _name + '.csv')
    try:
        urllib.request.urlretrieve(_id, ullfilename)
    except Exception as e:
        log("==> Error downloading file %s" % ullfilename)
        print(e)

for index, row in df.iterrows():
    
    log(row['name'])
    #Load List
    if row['list'] != "":
        load_file(row['list'], row['name'], 'lists')
        log('- List loaded')
    else:
        log('==> List not found')
        
    #Load Accumulation
    if row['accumulation'] != "":
        load_file(row['accumulation'], row['name'], 'accumulations')
        log('- Accumulation loaded')
    else:
        log('==>  no Accumulation')
      
log("Data synced")

#%% [markdown]
# ## Push git

#%%
#Push everything to git
log("Try to comming")
repo.git.add(GIT_COMMIT_DETECTION)
if repo.git.diff(None, cached=True) != "":
    repo.git.commit('-m', 'spreadsheet-auto-sync', author='simon.huwiler@ringier.ch')
    repo.git.push()
else:
    log("Nothing changed")

del repo

log("Everything done")


#%%



