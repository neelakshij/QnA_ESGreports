# scrap the table from webpage
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

company_name, company_symbol = [], []

# check response code is 200 to confirm whether request is successful.
url = "https://dailypik.com/top-50-companies-sp-500/?expand_article=1"
response = requests.get(url)
print(response.status_code) # check if it is 200

# Building the Parser Using Beautiful Soup
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')
# acess rows
for tx in table.find_all('tbody'):
    rows = tx.find_all('tr')

# save company names and respective symbols
for row in rows:
    name = row.find_all('td')[0].text
    symbol = row.find_all('td')[1].text
    company_name.append(name)
    company_symbol.append(symbol)

# construct dataframe and save    
df = pd.DataFrame({'Name': company_name, 'Symbol': company_symbol})
df.to_csv('SP50List.csv')

# OR save tabular data to json file
SnP50 = []
SnP50.append([{'Name': company_name,
              'Symbol': company_symbol}])

with open('SnP50_list_json', 'w') as json_file:
    json.dump(SnP50, json_file, indent=2)