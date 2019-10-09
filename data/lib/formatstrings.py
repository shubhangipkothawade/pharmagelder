import numpy as np
from consts import *

"""

    Diese Funktion setzt Vorname vor Nachname, getrennt mit Komma

"""
"""
def revert_name(dataset, sep=','):
    print("revert_name: Be sure: Only revert hcp, not hco!")
    dataset = dataset.apply(lambda s: (' '.join(s.split(sep)[::-1])).strip())
    return dataset
"""    

def revert_name(dataset, sep=','):
    for index, row in dataset[dataset.type == 'hcp'].iterrows():
        if row['type'] == 'hcp':
            splitted = row['name'].strip().split(sep)
            if len(splitted) == 2:
                dataset.loc[index, 'name'] =  (' '.join(splitted[::-1])).strip()
            else:
                if len(splitted) == 3:
                    dataset.loc[index, 'name'] =  splitted[1] + ' ' + splitted[2] + ' ' + splitted[0]
                else:
                    dataset.loc[index, 'name'] =  (' '.join(splitted[::-1])).strip()
                dataset.loc[index, '_export_information'] = 'Name besteht aus mehr als drei Wörtern. Evt falsch gedrecht. Bitte checken. Original: ' + row['name']
    
    return dataset
    

"""

    Standard-String-Umformungen wie:
      * Switzerland -> CH

"""
def basic_string_conversion(dataframe):

    #Format Country
    dataframe['country'] = dataframe['country'].str.replace('Switzerland', 'CH')
    dataframe['country'] = dataframe['country'].str.replace('SWITZERLAND', 'CH')
    dataframe['country'] = dataframe['country'].str.replace('Schweiz', 'CH')

    #clear field which contains only "."
    for column in dataframe.columns:
        if not np.issubdtype(dataframe[column].dtype, np.number):
            dataframe.loc[dataframe[column] == '.', column] = ""

    #Remove titles
    dataframe.loc[dataframe.type == 'hcp', 'name'] = dataframe.loc[dataframe.type == 'hcp', 'name'].str.replace(regex_title, '', regex=True, case=False)
    dataframe.name = dataframe.name.str.strip()

    return dataframe

"""

    Entfernt Umbrüche in allen Spalten

"""
def remove_carination(dataset, substr = ""):
    for column in dataset:
        if not np.issubdtype(dataset[column].dtype, np.number):
            dataset[column] = dataset[column].str.replace('\\r', substr)
        if not np.issubdtype(dataset[column].dtype, np.number):
            dataset[column] = dataset[column].str.replace('\\n', substr)
    return dataset

"""

    Wandelt alle Columns in Strings um. Benutzen, bevor geshiftet wird.

"""
def columns_to_string(_df):
    #fill na

    #transform columns
    for column in _df:
        _df[column] = _df[column].astype(str)
    return _df