""" 
Iterating through directories, list file path, year, company symbol and comapny name.
Save it as csv file to fetch report for QA-analysis asked by user.
Responsibility Reports were scrapped from responsibilityreports.com website and symbols were taken from Dailypik.
While saving reports, nomenclature was: year_companySymbol.pdf where symbol is the name listed in SP50 list.
I have created another csv file, extracting company name for their respective symbols.
Mount bucket using gcs utility.
"""

import os
import pandas as pd

# iterating throgh subdirectories, list year, report name (company symbol) and complete path to fetch that file.
dirpath = "./gcs-bucket/reports/"
filepath, year, docs = [],[], []
for subdir, dirs, files in os.walk(dirpath):
    for file in files:
        filepath.append(os.path.join(subdir, file))
        year.append(file.split('_')[0])
        docs.append(file.split('_')[1].split('.')[0])
        
# from the symbol, display company name
df = pd.read_csv('./gcs-bucket/SP50List.csv', index_col=0)
company_name = []
for doc in docs:
    ind = df.index[df['Symbol']==doc].tolist()
    company_name.append(df['Name'].iloc[int(ind[0])])
    
# save csv file with all details: filepath, year, company symbol and name
zipped = list(zip(filepath, year, docs, company_name))
df_detail = pd.DataFrame(zipped, columns=['filepath', 'year', 'company_symbol', 'company_name'])
#df_detail.to_csv('./gcs-bucket/ESG_Report_files.csv', index=False)