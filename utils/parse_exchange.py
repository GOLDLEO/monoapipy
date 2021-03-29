import requests
from bs4 import BeautifulSoup

from pprint import pprint

import json

def request_to_minfin():
	r = requests.get('https://index.minfin.com.ua/reference/currency/code/')
	soup = BeautifulSoup(r.text)
	tr = soup.find_all('tr')
	#pprint(data_tr)
	#print(data_tr[33].find_all('td')[2].get_text())
	lst = []
	for td in tr:
		data = td.find_all('td')
		try:
			if data[2]:
				lst.append(dict(code_id=data[1].get_text(), code=data[0].get_text(), name=data[2].get_text()))
		except Exception:
			continue
	return lst
		
#def save_json():
	#with open('currency_code.json', 'w') as file:
		#file.write(json.dumps(request_to_minfin()))




