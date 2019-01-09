import pandas as pd
import urllib.request
import numpy as np
import os
import sys
import git

#URL to the connection spreadsheet
ID_CONNECTION_SHEET = '2PACX-1vQO6w43ux3cONNFWW5o6aEX08bLhQJ6imIZUm6It4fMf_cMGfCWO3npNXe5uGAQCHj19jXACtclnfza'
EXPORT_FOLDER = '/data/python/pharmagelder/repo/data/2. manual check/%s/'
GIT_REPOSITORY = '/data/python/pharmagelder//repo'
GIT_COMMIT_DETECTION = '/data/python/pharmagelder/repo/data/2. manual check/*.csv'

#Templates
SHEET_URL = 'https://docs.google.com/spreadsheets/d/e/%s/pub?output=csv'

def log(value):
    #display(Markdown(value))
    print(value)

#Init repo
repo = git.Repo(GIT_REPOSITORY)

#Fetch repo
log("Pull from git")
#repo.remotes.origin.fetch()
repo.git.pull()

#Load Connection Sheet
log("Download Connection-Sheet")
df = pd.read_csv(SHEET_URL % ID_CONNECTION_SHEET)
df = df.fillna("")

def load_file(_id, _name, _subfolder):
    ullfilename = os.path.join(EXPORT_FOLDER % _subfolder, _name + '.csv')
    try:
        urllib.request.urlretrieve(SHEET_URL % _id, ullfilename)
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
