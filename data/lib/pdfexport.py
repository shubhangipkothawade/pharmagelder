import unidecode
import pandas as pd
import openpyxl
import numpy as np

number_fields = ["donations_grants", "sponsorship", "registration_fees", "travel_accommodation", "fees", "related_expenses", "total"]

# Shift all entries in a row one cell to the left
def shift_left(dataframe, index):
    dataframe[index: index + 1] = dataframe[index: index + 1].shift(-1, axis='columns')
    return dataframe

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

"""

    Bereinigen von Zahlen

"""
def cleanup_number(dataset):
    dataset = replace_apostrophe(dataset)
    dataset = remove_chf(dataset)
    dataset = remove_spaces(dataset)
    return dataset

"""

    Diese Funktion summiert alle Beträge

"""
def sum_amounts(dataset):
    dataset['total'] = dataset[["donations_grants", "sponsorship", 'registration_fees', 'travel_accommodation', 'fees', 'related_expenses']].sum(axis=1, skipna=True)
    return dataset

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

    Export to Excel

"""
def write_to_excel(dataset, organisation):
    #Add Organisation to dataset
    dataset['source'] = organisation

    #Check Dataset
    check_dataframe(dataset)

    #select writer
    writer = pd.ExcelWriter('../../export/' + organisation + '.xlsx', options={'encoding':'utf-8'})

    # Write the frame to excel
    dataset.to_excel(writer, 'daten', index=False) 
    
    writer.save()

    print("saved")

"""

    Export to CSV

"""
def write_to_csv(dataset, organisation, index = False):
    #Add Organisation to dataset
    dataset['source'] = organisation

    #Check Dataset
    check_dataframe(dataset)

    #write
    dataset.to_csv('../../export/' + organisation + '.csv', sep=";", index=index)

    print("saved")

"""

    Entfernt Umbrüche in allen Spalten

"""
def remove_carination(dataset):
    for column in dataset:
        if not np.issubdtype(dataset[column].dtype, np.number):
            dataset[column] = dataset[column].str.replace('\\r', '')
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

    Checked Dataframe auf Korrektheit

"""
def check_dataframe(ds):
    
    fix_columns = ['name', 'location', 'country', 'address', 'uci', 'donations_grants', 'sponsorship', 'registration_fees', 'travel_accommodation', 'fees', 'related_expenses', 'total', 'type', 'source']
    
    #Check to many columns
    for column in ds.columns:
        if column not in fix_columns:
            print("Column '" + column + "' zuviel")
            
    #Check missing column
    for column in fix_columns:
        if column not in ds.columns:
            print("Column '" + column + "' fehlt")
          
    #Check Numbers
    if not np.issubdtype(ds['donations_grants'].dtype, np.number):
        print("donations_grants not a number")
        
    if not np.issubdtype(ds['sponsorship'].dtype, np.number):
        print("sponsorship not a number")
        
    if not np.issubdtype(ds['registration_fees'].dtype, np.number):
        print("registration_fees not a number")
        
    if not np.issubdtype(ds['travel_accommodation'].dtype, np.number):
        print("travel_accommodation not a number")
        
    if not np.issubdtype(ds['fees'].dtype, np.number):
        print("fees not a number")
        
    if not np.issubdtype(ds['related_expenses'].dtype, np.number):
        print("related_expenses not a number")
        
    if not np.issubdtype(ds['total'].dtype, np.number):
        print("total not a number")
        
    # Check type
    if len(ds[~ds['type'].isin(['hcp', 'hco'])]) > 0:
        print("type not always hcp/hco")
        
    #Check if Sum = total
    if np.issubdtype(ds['total'].dtype, np.number):
        ds['_total'] = ds[["donations_grants", "sponsorship", 'registration_fees', 'travel_accommodation', 'fees', 'related_expenses']].sum(axis=1, skipna=True)
        if len(ds[ds.total.round(2) != ds._total.round(2)]) > 0:
            print("Total nicht Summe der Werte")
        ds = ds.drop(columns=['_total'], inplace=True)

"""

    Fügt UCI an der entsprechenden Stelle ein

"""
def add_uci(dataframe):
    dataframe.insert(4, 'uci', np.nan)
    return dataframe

"""

    Fügt den Type mittels index ein. Achtung: index zuvor reseten!

"""
def add_type_by_index(df, index, type_before = 'hcp', type_after = 'hco'):
    df['type'] = np.where(df.index < index, type_before, type_after)