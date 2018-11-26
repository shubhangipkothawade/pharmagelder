from consts import *
import pandas as pd

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

    Entfernt Punkte (1.500)

"""
def remove_dots(dataset):

    for field in number_fields:
        dataset[field] = dataset[field].str.replace(".", '')

    return dataset

"""

    Entfernt Kommas (1,500)

"""
def remove_comma(dataset):

    for field in number_fields:
        dataset[field] = dataset[field].str.replace(",", '')

    return dataset

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
    for field in number_fields:
        dataset[field] = dataset[field].str.replace(",", '.')
    
    return dataset

"""

    Entfernt CHF

"""
def remove_chf(dataset):
    for field in number_fields:
        dataset[field] = dataset[field].str.replace("CHF", '')
    
    return dataset

"""

    Entferne spaces in Zahlen

"""
def remove_spaces(dataset):
    for field in number_fields:
        dataset[field] = dataset[field].str.replace(" ", '')
    
    return dataset