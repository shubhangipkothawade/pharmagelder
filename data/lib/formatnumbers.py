from consts import *
import pandas as pd
import numpy as np

"""

    Bereinigen von Zahlen

"""
def cleanup_number(dataset):
    dataset = replace_apostrophe(dataset)
    dataset = remove_chf(dataset)
    dataset = remove_spaces(dataset)
    return dataset

"""

    Diese Funktion ändert den Datentyp zu numeric bei allen Zahlencolumns

"""
def amounts_to_number(dataset):
    for field in number_fields:
        dataset[field] = pd.to_numeric(dataset[field])

    return dataset

"""

    Entfernt Tausendertrenner in den (zur Zeit noch als String vorliegenden) Nummernfelder

"""
#Replace apostrophe
def replace_apostrophe(dataset):
    for field in number_fields:
        dataset[field] = dataset[field].str.replace("'", '')
    
    return dataset

"""

    Remove char in number field

"""

def replace_str(value, search, replace):
    if type(value) is str:
        return value.replace(search, replace)
    else:
        return value

def remove_in_numbers(dataset, char):
    for field in number_fields:
        #if not np.issubdtype(dataset[field].dtype, np.number):
        dataset[field] = dataset[field].apply(lambda x: replace_str(x, char, ''), 1)
        #dataset[field] = dataset[field].str.replace(char, '')

    return dataset

"""

    Entfernt Punkte (1.500)

"""
def remove_dots(dataset):
    return remove_in_numbers(dataset, ".")

"""

    Entfernt Kommas (1,500)

"""
def remove_comma(dataset):
    return remove_in_numbers(dataset, ",")

"""

    Remove Brackets

"""
def remove_brackets(dataset):
    for field in number_fields:
        dataset[field] = dataset[field].str.replace("(", '').str.replace(")", '')

    return dataset
"""

    Ersetzt Kommas durch Punkte

"""
def replace_comma_to_dot(dataset):
    return replace_in_number(dataset, ',', '.')
    """
    for field in number_fields:
        dataset[field] = dataset[field].str.replace(",", '.')
    
    return dataset
    """

"""

    Replace in Number Fields

"""
def replace_in_number(dataset, pat, repl):
    for field in number_fields:
        #dataset[field] = dataset[field].str.replace(pat, repl)
        dataset[field] = dataset[field].apply(lambda x: replace_str(x, pat, repl), 1)
    
    return dataset

"""

    Entfernt CHF

"""
def remove_chf(dataset):
    for field in number_fields:
        dataset[field] = dataset[field].str.replace("CHF", '')
        dataset[field] = dataset[field].str.replace("Fr.", '')
        dataset[field] = dataset[field].str.replace("fr.", '')
    
    return dataset

"""

    Entferne spaces in Zahlen

"""
def remove_spaces(dataset):
    for field in number_fields:
        dataset[field] = dataset[field].str.replace(" ", '')
    
    return dataset

"""

    Fügt eine leere Accumulation hinzu

"""
def add_empty_accumulation(dataframe, type_):
    r = {"type": type_,
           "donations_grants": 0,
           "sponsorship": 0,
           "registration_fees": 0,
           "travel_accommodation": 0,
           "fees": 0,
           "related_expenses": 0,
           "total": 0
           }
    return dataframe.append(r, ignore_index=True)