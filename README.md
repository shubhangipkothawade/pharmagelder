# Pharmagelder
## Installation
**Checkout Git**
Checkout this Github Repo at a folder of your choice
```
git init
git remote add origin git@github.com:blickvisual/pharmagelder.git
````

**Install Python Dependencies**
```
#If you use virtual env (recommended)
source env/bin/activate

#Install dependencies
pip install -r requirements.txt
```
**Install Abbeyy Finereader**
For OCR-Recognition, we used Abbeyy Finereader. It's not for free, but worth it.
https://www.abbyy.com/de-de/finereader/

## Procedure
### Step 1 - Export data
In the Folder [data/1. pdfexport/files] you will find a subfolder for each pharmaceutical company. Put the PDFs (if available) there. Each folder needs to files:
* 0. Lists.ipynb
* 1. Accumulations.ipynb

`0. Lists.ipynb` extracts all doctors and organisations. `1. Accumulations.ipynb` extracts the accumulations - all the anonym doctors and organisations.

The exported files will be stored in the folder [data/1. pdfexport/export/]. Do never change something directly in this csv-files. Use the python-notebooks or do it later on google spreadsheets.

#### How to extract
As mentioned before, each pharmaceutical company gets two python notebooks. Update them (or copy them) to export another company. There are plenty of helper functions for extracting the data.
Everything documented in [data/README.md]. The code ist stored in [data/lib]
**Read the Code Documentation [data/README.md]!**

There are different kind of exports:
* Readble PDFs -> Use tabulaPy
* Scanned PDFs -> Use Abbeyy to generate CSV and then Pandas
* Excel -> Use Pandas
* Website -> Copy the source code, then use Beautiful Soup

You will find many examples in the `files` folder.

### Step 2 - Manually Cleaning
After everything is extraced, create a google spreadsheet for each file. Be aware: During import, set number recognition to False. We made for `lists` and `accummulations` a folder each.
Then you need a table where you store the IDs of each file. Then you are able to sync google spreadsheet with Git.

See the detailed documentation in [tasks/2. spreadsheet_to_github/0. Download Spreadsheets.ipynb]
There are two files in the folder [tasks/2. spreadsheet_to_github/]
* `0. Download Spreadsheets.ipynb` use this to trigger the sync manually per jupyter notebook
* `0. Download Spreadsheets.py` use this if you like to automate the sync. You need to edit it!

Now everyone can edit the files, make fixes while your git repository is always up to date.

### Step 3 - Concatenate Files
This is, where the real magic happens!