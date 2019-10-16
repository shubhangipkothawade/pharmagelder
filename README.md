# Pharmagelder
## Other Important README-Files
* [data/README.md](data/README.md) for scripting / exporting
* [data/_docs/PDF_SCREENSHOTS.md](data/_docs/PDF_SCREENSHOTS.md) to find the best template
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

**Install libPostal**  
Have a look at the [GitHub Repository](https://github.com/openvenues/libpostal/). On Mac, do the following:
```bash
brew install curl autoconf automake libtool pkg-config

git clone https://github.com/openvenues/libpostal
cd libpostal
./bootstrap.sh
./configure --datadir=[...some dir with a few GB of space...]
make -j4
sudo make install

# On Linux it's probably a good idea to run
sudo ldconfig
```

If `pip install postal` throws an error, install `pip install nose` first.

## Procedure
### Step 1 - Export data
In the Folder [data/1. pdfexport/files](data/1.%20pdfexport/files/) you will find a subfolder for each pharmaceutical company. Put the PDFs (if available) there. Each folder needs to files:
* 0. Lists.ipynb
* 1. Accumulations.ipynb

`0. Lists.ipynb` extracts all doctors and organisations. `1. Accumulations.ipynb` extracts the accumulations - all the anonym doctors and organisations.

The exported files will be stored in the folder [data/1. pdfexport/export/](data/1.%20pdfexport/export/). Do never change something directly in this csv-files. Use the python-notebooks or do it later on google spreadsheets.

#### How to extract
As mentioned before, each pharmaceutical company gets two python notebooks. Update them (or copy them) to export another company. There are plenty of helper functions for extracting the data.
Everything documented in [data/README.md](data/README.md). The code ist stored in [data/lib](data/lib)

**Read the Code Documentation [data/README.md](data/README.md)!**

There are different kind of exports:
* Readble PDFs -> Use tabulaPy
* Scanned PDFs -> Use Abbeyy to generate CSV and then Pandas
* Excel -> Use Pandas
* Website -> Copy the source code, then use Beautiful Soup

You will find many examples in the [data/1. pdfexport/files](data/1.%20pdfexport/files/) folder.

### Step 2 - Manually Cleaning
After everything is extraced, create a google spreadsheet for each file. Be aware: During import, set number recognition to False. We made for `lists` and `accummulations` a folder each.
Then you need a table where you store the IDs of each file. Then you are able to sync google spreadsheet with Git.

See the detailed documentation in [tasks/2. spreadsheet_to_github/0. Download Spreadsheets.ipynb](tasks/2.%20spreadsheet_to_github/0.%20Download%20Spreadsheets.ipynb)
There are two files in the folder [tasks/2. spreadsheet_to_github/](tasks/2.%20spreadsheet_to_github/)
* [0. Download Spreadsheets.ipynb](tasks/2.%20spreadsheet_to_github/0.%20Download%20Spreadsheets.ipynb) use this to trigger the sync manually per jupyter notebook
* [0. Download Spreadsheets.py](tasks/2.%20spreadsheet_to_github/0.%20Download%20Spreadsheets.py) use this if you like to automate the sync. You need to edit it!

Now everyone can edit the files, make fixes while your git repository is always up to date. The files will be stored in the folder `data/2. manual check`

### Step 3 - Export live DB
We take our "old" data from the live database, not old csv files. Take a dump of your live database and import it to your own mysql database.  
Nor export the data: `3. export livedata/0. export database.ipynb`. This file exports the data to a csv.  
**Be aware: To not use this data for calculations! The export drops duplicates and merges different tables. The generated files are only for matching purpose later!**

### Step 4 - Concatenate Files
Now you need to concatenate all files, clean them and prepare them for fuzzy matching. Therefore run each notebook in the folder `tasks/4. transform files`.  
Have a look at `4. check dataset.ipynb`. If there are addresses witouth a source (eq pharma company), add them to the csv `tasks/6. database export/sources/liste_companies.csv` and `pharma_source.csv``

### Step 5 - Matching
Now we need to find pairs. We do this in four steps:

1. Compare the data to the exported live data. It uses fuzzy matching and looks for the most similar address.
`0_match_to_livedb.ipynb`  
**Run it twice and change `run_for = 'hcp'`!**
2. There are some tricky address. We force them to pairs. There are two google spreadsheets, for hcp and hco each. There we put the tricky candidats. The following scripts will use this spread sheets and creates the matching  
`1_overright_parent_by_force_matching.ipynb`  
**You need to update the spread sheet url!**
3. Now we compare all addresses without a sibling to each others and create a network  
`2_match_missing.ipynb`  
**Run it twice and change `run_for = 'hcp'`!**
4. Lets group everything. After that, our data is ready.  
`3_group_matches.ipynb`

### Step 6 - Build Database Dump
Now we create a new database dump **with only the new data**. You can run this on your live database and the update queries will do the rest.  
`6. database export/0. create database import.ipynb`  
`data/4. database/data_dump.sql` is your file. If the import fails, you can import file by file and find the problem.

### Step 7 - Summarize the data and create Excel sheets
To check your data, there are some notebooks. This notebooks will create excel sheets.  
To do this, your local mysql database needs to be up to date, so if you have not imported `data_dump.sql` yet, do it know!  
* `tasks/99. Analyzes/Summarize Pharmas by disclosure.ipynb` will create a table with information about each company and its disclosure
* `tasks/99. Analyzes/Summarize Pharmas by Recipient Type.ipynb` does the same, but categorizes by hcp and hco.
* `Export Recipients 2018 Clean.ipynb` exports all recipients from year 2018
* `Export Recipients 2018.ipynb` does the same, will give you each address and group, the address is in it. Be patient...
* `Export all Recipients.ipynb` exports everything