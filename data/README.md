# The Extraction Scripts
## Rule of formating - Lists
* Name: `Firstname Lastname`
* Land: `Switzerland`
* Type: `hcp` or `hco`
* Numbers: No inverted comma, use Dot for decimal.
Right: `1000.50`, wrong: `1'000,50`

## How a "list"-dataset should look like
```
name,location,country,address,plz,uci,donations_grants,sponsorship,registration_fees,travel_accommodation,fees,related_expenses,total,type
Max Mustermann,Zürich,CH,Strasse 5,,,,,315.0,487.0,,,802.0,hcp
```
The export function will add the column `source`. Dont do it manually.
## How a "accumulation"-dataset shoud look like
```
type,donations_grants,sponsorship,registration_fees,travel_accommodation,fees,related_expenses,total
hcp_amount,,,0.0,0.0,2400.0,0.0,2400.0
hco_amount,0.0,109439.0,0.0,0.0,0.0,0.0,109439.0
hcp_count,,,0.0,0.0,2.0,0.0,2.0
hco_count,0.0,3.0,0.0,0.0,0.0,0.0,3.0
rnd,,,,,,,1761943.0
```

## Required functions for lists
This Functions have to be in the list extraction

**basic_string_conversion**  
`df_export = basic_string_conversion(df_export)`  
Does some cleaning:  
* `Switzerland` to `CH`
* Removes `Dr. Md. Med etc.`

**export_list**  
`export_list(df_export, 'NAME_OF_COMPANY')`  
Safes the dataframe to the right folder **and** checks the dataframe. It calculates, checks for carinations, reorder the datasets, add new fields, etc. This is your final function in each script!

## Required functions for accumulations
**export_accumulation**  
`export_accumulation(df_export, 'astrazeneca')`  
Similar to `export_list`. This is your final function!

### Export-Funktionen
**write_to_excel (not in production!)**  
`df_export = write_to_excel(df_export, 'tmp.xlsx'[, open=False])`  
Safes the dataframe as Excel and may open it directly. Use this during development, but not at the end!

**write_to_csv (not in production!)**  
`df_export = write_to_excel(df_export, 'novartis'[, index=False])`  
Similar to `write_to_excel`. Not in production!

### Format numbers
**amounts_to_number**  
`df_export = amounts_to_number(df_export)`  
Converts all number columns (`sponsorship, donations, etc.`) to actually floats. Use this in every script if possible. Only avoid, if cells have text, which you cant convert automaticly (as in scanned pdfs)

**cleanup_number**  
`df_export = cleanup_number(df_export)`  
Cleans the number fields (strings at the moment), to that you can call `amounts_to_number`
The function actually calls:
* `replace_apostrophe`
* `remove_chf`
* `remove_spaces`

**replace_apostrophe**  
`df_export = replace_apostrophe(df_export)`  
Removes apostrophes in number fields

**remove_chf**  
`df_export = remove_chf(df_export)`  
Removes `CHF` in  all number fields

**remove_spaces**  
`df_export = remove_spaces(df_export)`  
Remove spaces in all number fields

**remove_dots**  
`df_export = remove_dots(df_export)`  
Removes all dots in number fields.

**remove_comma**  
`df_export = remove_comma(df_export)`  
Removes all commas in number fields.


**remove_in_numbers**  
`df_export = remove_in_numbers(df_export, 'X')`  
Removes `X` in number fields

**replace_comma_to_dot**  
`df_export = replace_comma_to_dot(df_export)`  
Replaces comma with dots in all number fields

**replace_in_number**  
`df_export = replace_in_number(df_export, 'X', 'Y')`  
Replaces `X` with `Y` in all numberfields

**add_empty_accumulation**  
`df_export = add_empty_accumulation(df_export, "rnd")`  
Adds en empty accumulation line.

**add_accumulation**  
`df_export = add_accumulation(df_export, AccType.hcp_amount, fees = 14389.37, total = 14389.37)`  
Adds an accumulation manually. You can use all parameters which are allowed in the final table.

### Add Type (Type = HCP or HCO)

**set_type_by_alphabetical_order**  
`df_export = set_type_by_alphabetical_order(df_export)`  
Adds the type based on the alphabets. Means: The moment, a name is not anymore in alphabetical order, it has to be the start of the hco-group.
Example:
```
Banz Meier
Clus Hannes
Dinkelberger Peter <- not in order anymore, must be HCP
Kantonsspital Sarnen
Kantonsspital Zürich
```

Possible to change HCP and HCO 
`df_export = set_type_by_alphabetical_order(df_export, hcp_before_hco = False)`

**add_type_by_index**  
```python
#Add Type by Index
add_type_by_index(df_export, 220, [type_before = 'hcp', type_after = 'hco'])
add_warning(manually=True) #Writes a warning to the output
```
Add type by index: Needs a number. Avoid this if possible.

**Type by Textstring**  
Add the type by search for a text string
```python
#Add Type
index_hco = df_export[df_export['name'].str.contains("INDIVIDUAL NAMED DISCLOSURE", na=False)].index[0]
df_export['type'] = np.where(df_export.index < index_hco, 'hcp', 'hco')
```  
### Others

**sum_amounts**  
`df_export = sum_amounts(df_export)`  
Sums all number fields. Only use, when total not provided

**revert_name**  
`df_export = revert_name(df_export)`  
Changes Lastname To Surname. If more than two names, writes a warning to a separat column.

**remove_carination**  
`df_export = remove_carination(df_export[, substr=""])`  
Removes carination (\r and \n) in **all** columns

**add_uci**  
`df_export = add_uci()`  
Add an empty UCI-Column

**remove_empty_columns (depricated)**  
`df_export = remove_empty_columns(df_export)`  
Remove all columns which are empty. Dont use this, actually...

**columns_to_string**  
`df_export = columns_to_string(df_export)`  
Converts all collumns to strings. Sometimes you need this before shifting a columns.

# Often used code snippets
**Remove empty rows**  
`df_export = df_export.dropna(subset=['donations_grants', 'sponsorship', 'registration_fees', 'travel_accommodation', 'fees', 'related_expenses', 'total'], how='all')`  

**Shift rows**  
`df_export[df_export['name'].notna()] = df_export[df_export['name'].notna()].shift(1, axis='columns')`  
IMPORTANT: Sometimes you have to remove all NaNs in the columns or you will lose data. Look at `Celgene`  
  
**Reorder Columns**  
`df_export = df_export[fix_columns[:-1]]`  

**Unlock PDF**
```python
import pikepdf
pdf = pikepdf.open('pkk-erfassungmepha-pharma-ag20180427_eng_final.pdf')
pdf.save('unlocked.pdf')
```   
**Remove Name in Address**  
Sometimes you see the company name again in the address field. Like:  
"Stiftung SONK","Stiftung SONK Rorschacher Strasse 150"  
```python
for index, row in df_export.iterrows():
    df_export.loc[index, 'address'] = row['address'].replace(row['name'] + ' ', '')
```

**Remove Title**
```python
#Remove Titles
df_export['name'] = df_export.name.str.replace(regex_title, '', regex=True, case=False)
df_export['name'] = df_export.name.str.strip()
```

## Examples
* Duplicated entries: [GlaxoSmithKline](http://localhost:8888/notebooks/data/1.%20pdfexport/files/GlaxoSmithKline/0.%20Lists.ipynb)
* Beautiful Soup: [Lundbeck](http://localhost:8888/notebooks/data/1.%20pdfexport/files/Lundbeck/0.%20Lists.ipynb)
* PDF Unlock: [Mepha](http://localhost:8888/notebooks/data/1.%20pdfexport/files/Mepha/0.%20Lists.ipynb)
* Type by Text-String (`INDIVIDUAL NAMED DISCLOSURE` oä): [Bristol](http://localhost:8888/notebooks/data/1.%20pdfexport/files/Bristol%20Myers%20Squibb/0.%20Lists.ipynb)
* Accumulation manually [Jansen-Cilag](http://localhost:8888/notebooks/data/1.%20pdfexport/files/Jansen-Cilag/1.%20Accumulations.ipynb)
* Nothing to declare: [SFL Pharma](http://localhost:8888/notebooks/data/1.%20pdfexport/files/SFL%20Pharma/0.%20Lists.ipynb)