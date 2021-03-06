from consts import *
import numpy as np

"""

    Checked Dataframe auf Korrektheit

"""
def check_dataframe_list(ds):
    
    #Check to many columns
    for column in ds.columns:
        if column not in fix_columns + [column_export_information]:
            print("Column '" + column + "' zuviel")
            
    #Check missing column
    for column in fix_columns:
        if column not in ds.columns:
            print("Column '" + column + "' fehlt")
          
    #Check Numbers
    for column in number_fields:
        if not np.issubdtype(ds[column].dtype, np.number):
                print(column + " not a number")
        
    # Check type
    if len(ds[~ds['type'].isin(['hcp', 'hco'])]) > 0:
        print("type not always hcp/hco")

    #Check if \n
    for column in ds.columns:
        if not np.issubdtype(ds[column].dtype, np.number):
            if len(ds[ds[column].str.contains('\\r', na=False)]) > 0 or len(ds[ds[column].str.contains('\\n', na=False)]) > 0:
                print("'" + column + "' contains carrination (\\r or \\n)! Use remove_carination()")

    #Check Duplicates
    if len(ds[ds.duplicated()]) > 0:
        print("Duplicates found. Please check for duplicates: df_export[df_export.duplicated()]")
        
    #Check if Sum = total
    if np.issubdtype(ds['total'].dtype, np.number):
        ds['_total'] = ds[["donations_grants", "sponsorship", 'registration_fees', 'travel_accommodation', 'fees', 'related_expenses']].sum(axis=1, skipna=True)
        if len(ds[ds.total.round(2) != ds._total.round(2)]) > 0:
            print("Total nicht Summe der Werte")
        ds = ds.drop(columns=['_total'], inplace=True)


def check_dataframe_accumulations(ds):
    
    #Check to many columns
    for column in ds.columns:
        if column not in fix_columns_accumulations:
            print("Column '" + column + "' zuviel")
            
    #Check missing column
    for column in fix_columns_accumulations:
        if column not in ds.columns:
            print("Column '" + column + "' fehlt")
          
    #Check Numbers
    for column in number_fields:
        if not np.issubdtype(ds[column].dtype, np.number):
                print(column + " not a number")

    #Check types
    types = ["hcp_amount", "hcp_count", "hco_amount", "hco_count", "rnd"]
    for t in types:
        if len(ds[ds.type == t]) != 1:
            print(t + " not found or not unique")

    #Check if Sum = total
    if np.issubdtype(ds['total'].dtype, np.number):
        ds['_total'] = ds[["donations_grants", "sponsorship", 'registration_fees', 'travel_accommodation', 'fees', 'related_expenses']].sum(axis=1, skipna=True)
        ds.loc[ds.type == 'rnd', "_total"] = ds.loc[ds.type == 'rnd', "total"]

        for index, row in ds.iterrows():
            if row['type'] in ['hcp_count', 'hco_count']:
                continue

            if round(np.nan_to_num(row['total']), 2) != round(np.nan_to_num(row['_total']), 2):
                print("Total %s nicht Summe der Werte" % row['type'])

        ds = ds.drop(columns=['_total'], inplace=True)