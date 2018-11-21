import numpy as np

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