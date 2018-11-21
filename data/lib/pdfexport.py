
# Import local
import datacheck
import exports
import formatstrings
import typefield
import formatnumbers


import importlib
importlib.reload(datacheck)
importlib.reload(exports)
importlib.reload(formatstrings)
importlib.reload(typefield)
importlib.reload(formatnumbers)

from datacheck import *
from exports import *
from formatstrings import *
from typefield import *
from formatnumbers import *

# Import global
import numpy as np


# Shift all entries in a row one cell to the left
def shift_left(dataframe, index):
    dataframe[index: index + 1] = dataframe[index: index + 1].shift(-1, axis='columns')
    return dataframe


"""

    Diese Funktion summiert alle Beträge

"""
def sum_amounts(dataset):
    dataset['total'] = dataset[["donations_grants", "sponsorship", 'registration_fees', 'travel_accommodation', 'fees', 'related_expenses']].sum(axis=1, skipna=True)
    return dataset


"""

    Entfernt alle leeren Columns in einem Dataframe

"""
def remove_empty_columns(df):
    #Loop Columns
    for column in df.columns:
        
        #Wenn Column leer, entfernen
        if len(df[df[column].notna()]) == 0:
            df = df.drop(columns=column)

    return df


"""

    Fügt UCI an der entsprechenden Stelle ein

"""
def add_uci(dataframe):
    dataframe.insert(4, 'uci', np.nan)
    return dataframe

