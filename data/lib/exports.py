from datacheck import *
import numpy as np
import pandas as pd
import openpyxl

"""

    Export to Excel

"""
def write_to_excel(dataset, exportfile):
    #select writer
    writer = pd.ExcelWriter(exportfile, options={'encoding':'utf-8'})

    # Write the frame to excel
    dataset.to_excel(writer, 'daten', index=False) 
    
    writer.save()

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
    dataset.to_csv('../../export/lists/' + organisation + '.csv', sep=";", index=False)

    print("saved")

def export_acumulations(dataset, organisation):
    #Add Organisation to dataset
    dataset['source'] = organisation

    #Check Dataset
    check_dataframe_accumulations(dataset)

    #write_to_excel(dataset, '../../export/accumulations/' + organisation + '.xlsx' )
    dataset.to_csv('../../export/accumulations/' + organisation + '.csv', sep=";", index=False)

    print("saved")
