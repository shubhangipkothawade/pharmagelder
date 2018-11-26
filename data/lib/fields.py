import numpy as np
import unidecode

"""

    Diese Funktion setzt den Typ (hcp, hco) anhand der alphabetischen Ordnung.
    Sobald ein Name nicht mehr in alphabetischer Ordnung ist, wird angenommen, 
    dass ab diesem Namen der neue Typ beginnt. Setzt voraus, dass das Dataset
    bereits die korrekten Fieldnames enthält.
    Es wird nur jeweils das erste Wort (bei Doppelnamen) verglichen, da
    unterschiedliche Sortierungen (bei -, " ", ', etc.) vorkommen
"""

"""
def format_for_stringcompare(x, lastname_before_name = True):

    #Name is at the end: Swap!
    if not lastname_before_name:
        tmp = x.split(" ")
        tmp.reverse()
        x = " ".join(tmp)
    
    x = unidecode.unidecode(x)
    x = x.replace("'", "")
    x = x.split(" ")[0]
    #x = x.replace(" ", "aaa")
    #x = x.replace("-", "aaa")
    x = x.lower()
    return x
"""

def format_for_stringcompare(x, lastname_before_name = True):

    #Name is at the end: Swap!
    x = unidecode.unidecode(x)
    if not lastname_before_name:
        tmp = x.split(" ")
        tmp.reverse()
        x = " ".join(tmp)
    
    x = x[0]
    x = x.lower()
    return x

def set_type_by_alphabetical_order(dataset, hcp_before_hco = True, lastname_before_name = True):

    #Define Type-Order
    if hcp_before_hco:
        val_first = 'hcp'
        val_second = 'hco'
    else:
        val_first = 'hco'
        val_second = 'hcp'

    #Reset Index
    dataset = dataset.reset_index(drop=True)

    #Shift name
    dataset['_name_shift'] = dataset.name.shift()

    #Set first row to 'AAAAA'
    dataset.loc[0,'_name_shift']= 'AAAAA'

    alphabet_changed = False

    #Iter rows
    for i, row in dataset.iterrows():
        if format_for_stringcompare(row['name'], lastname_before_name) >= format_for_stringcompare(row['_name_shift'], lastname_before_name) and (not alphabet_changed):
            dataset.loc[i, 'type'] = val_first
        else:
            #print(format_for_stringcompare(row['name'], lastname_before_name) + ' -> ' + format_for_stringcompare(row['_name_shift'], lastname_before_name))
            dataset.loc[i, 'type'] = val_second
            alphabet_changed = True

    #Remove Temp Rows
    dataset = dataset.drop('_name_shift', axis='columns')
    
    return dataset

"""

    Fügt den Type mittels index ein. Achtung: index zuvor reseten!

"""
def add_type_by_index(df, index, type_before = 'hcp', type_after = 'hco'):
    df['type'] = np.where(df.index < index, type_before, type_after)

"""

    Fügt UCI an der entsprechenden Stelle ein

"""
def add_uci(dataframe):
    dataframe.insert(5, 'uci', np.nan)
    return dataframe


"""

    Fügt PLZ an der entsprechenden Stelle ein

"""
def add_plz(dataframe):
    dataframe.insert(4, 'plz', np.nan)
    return dataframe

"""

    Fügt Country an der entsprechenden Stelle ein

"""
def add_country(dataframe):
    dataframe.insert(3, 'country', 'CH')
    return dataframe

