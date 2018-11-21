import numpy as np

"""

    Diese Funktion setzt Vorname vor Nachname, getrennt mit Komma

"""
def revert_name(dataset):
    dataset = dataset.apply(lambda s: (' '.join(s.split(',')[::-1])).strip())
    return dataset

"""

    Standard-String-Umformungen wie:
      * Switzerland -> CH

"""
def basic_string_conversion(dataframe):
    dataframe['country'] = dataframe['country'].str.replace('Switzerland', 'CH')
    return dataframe

"""

    Entfernt Umbrüche in allen Spalten

"""
def remove_carination(dataset):
    for column in dataset:
        if not np.issubdtype(dataset[column].dtype, np.number):
            dataset[column] = dataset[column].str.replace('\\r', '')
    return dataset

