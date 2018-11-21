from datacheck import *
import numpy as np
import pandas as pd
import openpyxl

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

    Main Export function

"""
def export_file(dataset, organisation):
    write_to_excel(dataset, organisation)