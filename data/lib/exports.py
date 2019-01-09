from datacheck import *
import numpy as np
import pandas as pd
import openpyxl

"""

    Export to Excel

"""
def write_to_excel(dataset, exportfile, open=False):
    #select writer
    writer = pd.ExcelWriter(exportfile, options={'encoding':'utf-8'})

    # Write the frame to excel
    dataset.to_excel(writer, 'daten', index=False) 
    
    writer.save()

    if open:
        import subprocess, os, sys
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', exportfile))
        elif os.name == 'nt': # For Windows
            os.startfile(exportfile)
        elif os.name == 'posix': # For Linux, Mac, etc.
            subprocess.call(('xdg-open', exportfile))

"""

    Export to CSV

"""
def write_to_csv(dataset, organisation, index = False):
    #Add Organisation to dataset
    dataset['source'] = organisation

    #Check Dataset
    #check_dataframe_list(dataset)

    #write
    dataset.to_csv(organisation, sep=";", index=index)

"""

    Main Export function

"""
def export_list(dataset, organisation):
    #Add Organisation to dataset
    dataset['source'] = organisation

    #Check Dataset
    check_dataframe_list(dataset)

    #Reorder Dataframe
    dataset = dataset[fix_columns]

    #Export
    #write_to_excel(dataset, '../../export/lists/' + organisation + '.xlsx' )
    dataset.to_csv('../../export/lists/' + organisation + '.csv', sep=",", index=False)

    print("saved")

def export_acumulations(dataset, organisation):
    #Add Organisation to dataset
    dataset['source'] = organisation

    #Check Dataset
    check_dataframe_accumulations(dataset)

    #Reorder Dataframe
    dataset = dataset[fix_columns_accumulations]

    #write_to_excel(dataset, '../../export/accumulations/' + organisation + '.xlsx' )
    dataset.to_csv('../../export/accumulations/' + organisation + '.csv', sep=",", index=False)

    print("saved")
