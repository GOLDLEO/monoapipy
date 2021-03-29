import json

from datetime import datetime, date

from utils.exc import DatetimeError
from pprint import pprint

import os

# ищем по кодам названия валют с опцией которая возвращает код или название кода				
def find_code(code, formt=True):

	f = open('utils/currency_code.json', 'r')
	values = json.loads(f.readline())
	if formt == True:
		for data in values:
			if int(code)==int(data['code_id']):
				return data['code']
	elif formt == False:
		for data in values:
			if int(code)==int(data['code_id']):
				return data['name']
	else: 
		return None

# Переводим в unix time 
def encode_unix_time(date):
	try:
		date = datetime.fromisoformat(date)
		print(int(datetime.timestamp(date)))
		return int(datetime.timestamp(date))
	except Exception as error:
		print(error)
		raise DatetimeError('Не верно указана дата или время.')

# Считаем самую крайнюю дату
def max_time_range():
	data = date.today().__str__()
	return str(data[:6]) + str(int(data[5:7]) - 1) + str(int(data[7:]) - 1)


# Функция выбора карты
def get_accounts(request_json):
	accounts = request_json
	data = []
	
	for account in accounts['accounts']:

		data.append(dict(
			id=account['id'], 
			code=account['currencyCode'], 
			value=find_code(account['currencyCode']
				)
			)
		)
	return data