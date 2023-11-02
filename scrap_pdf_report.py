# take company name from saved csv/json file and request ESG report

import requests
from bs4 import BeautifulSoup
import pandas as pd

# dataframe has 2 columns: 'Name' & 'Symbol'
df = pd.read_csv('SP50List.csv')
company_name = df['Name']
company_symbol = df['Symbol']

url = "https://www.responsibilityreports.com"
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')
forms = soup.find_all('form')

payload = {'search': company_symbol[0]}
r = requests.post('https://www.responsibilityreports.com/Companies', data=payload)
print(r.status_code) # if 200, request is successful.

# get company name
search_req = BeautifulSoup(r.text, 'html.parser')
field_name = search_req.select_one('.companyName a')['href']

# link associated to company is not with company name. Find respective url.
url_with_comanyName = url + filedNm
req_withCompanyName = requests.post(url_with_comanyName)

search_req2 = BeautifulSoup(req_withCompanyName.text, 'html.parser')
link_for_companySearch = search_req2.select_one('.view_btn a')['href']

report_url = url + link_for_companySearch

# confirm status code
r = requests.get(report_url)  

# save pdf file with required nomenclature: year_companySymbol.pdf
year = '2022'
file_name = year+'_'+company_symbol[0]
with open(file_name+'.pdf', 'wb') as f:
    f.write(r.content)
    

    
###########
# best practice to handle exception
#post_request(url, payload)

#def post_request(url, payload):     
#    try:           
#        r = requests.post(url, data=payload)             
#        if r.status_code == 200:                 
#            return r
#        else:
#            print(r.status_code)
#    except Exception as e:             
#        print(e)