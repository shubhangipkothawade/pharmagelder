import numpy as np
from consts import *

"""

    Diese Funktion setzt Vorname vor Nachname, getrennt mit Komma

"""
def revert_name(dataset, sep=','):
    dataset = dataset.apply(lambda s: (' '.join(s.split(sep)[::-1])).strip())
    return dataset

"""

    Standard-String-Umformungen wie:
      * Switzerland -> CH

"""
def basic_string_conversion(dataframe):

    #Format Country
    dataframe['country'] = dataframe['country'].str.replace('Switzerland', 'CH')
    dataframe['country'] = dataframe['country'].str.replace('Schweiz', 'CH')

    #clear field which contains only "."
    for column in dataframe.columns:
        if not np.issubdtype(dataframe[column].dtype, np.number):
            dataframe.loc[dataframe[column] == '.', column] = ""

    #Remove titles
    dataframe.loc[dataframe.type == 'hcp', 'name'] = dataframe.loc[dataframe.type == 'hcp', 'name'].str.replace(r'\b(Dr|med|prof|prakt|pd)[\s[.]]*', '', regex=True, case=False)
    dataframe.name = dataframe.name.str.strip()

    return dataframe

"""

    Entfernt Umbrüche in allen Spalten

"""
def remove_carination(dataset, substr = ""):
    for column in dataset:
        if not np.issubdtype(dataset[column].dtype, np.number):
            dataset[column] = dataset[column].str.replace('\\r', substr)
    return dataset

