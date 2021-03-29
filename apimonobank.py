import requests

from utils.exc import MonobankConnectError
from utils.util import find_code, encode_unix_time, max_time_range, get_accounts

from datetime import datetime

from pprint import pprint

import time
import os 


class monobank:
	
	def __init__(self, token=''):
		
		if token:
			self.token = token
			self.accounts = get_accounts(self.__request('personal/client-info', self.token))
		else:
			self.token = token



	def __request(self, url,token=''):
		"""Request to mono api, not use for methods self. Just call from cls methods"""

		base = 'https://api.monobank.ua/'
		headers = {
			'X-Token': token
		} 
		r = requests.get(base + url, headers=headers)
		if r.status_code == 200:
			return r.json()

		raise_exc = r.json()
		if raise_exc['errorDescription'] == 'Too many requests':
			raise MonobankConnectError('Слишком много запросов, попробуйте немного позже.')


		raise(MonobankConnectError(str(raise_exc['errorDescription'])))

	def get_mono_currency(self, *currency_value_from):
		""" Get current currency. You can input original code currency, look at utils.util.
		Return text info. Converting in *currency_value_from !Just in grivnas
		*currency_value_from = code currency

		Example: 
			mono.get_mono_currency(840, 978)

		"""

		url = 'bank/currency'
		try: 
			data_currency = self.__request(url, self.token)
		except Exception as error:
			return 'Возникла ошибка: '+ str(error)
		else:
			text = str('BUY  -  SELL') + '\n'
			for data in data_currency:
				for from_cv in currency_value_from:
					if  data['currencyCodeA']== from_cv:
						if data['currencyCodeB']==980:
							
							text = text +  str(round(data['rateBuy'],2)) + '  -  ' + str(round(data['rateSell'],2)) + str(find_code(data['currencyCodeA'])) + '\n'
			return text 


	def person_info(self):
		"""Displaying your personal info. Just working with your access token. 
			Example: 
			my_info = mono.personal_info()
			print(my_info)
		"""
		url  = 'personal/client-info' #url for request
		try:
			data = self.__request(url, self.token) # try to making request
		except Exception as error:
			return 'Возникла ошибка: ' + str(error) # return exception for error by time error or etc.
		else:
			text = ''
			for card in data['accounts']: # loop in your accounts 
				if card['balance'] > 0:
					text = text + '{}: {} \n'.format( 
						find_code(card['currencyCode'], formt=False),
						card['balance']/100
					)
				else:
					return 'На вашем счету 0.'
		return text
		

	def get_money_range(self, account, from_time='2021-02-16 13:00', to_time=''):
	""" Displaying a personal list of financial flows from interested date to current date. 
		Return tuple of string and list.
		Example: outputString, listOutput = mono.get_money_range(user_account_id, from_date, to_date)
		*account = your custom account from personal_info
		*from_time:str variable =  '2021-02-16 13:00'
		[optional]to_time:str variable   =  '2021-02-16 13:00'"""

		try:
			if to_time == '':

				url = '/personal/statement/{}/{}'.format(account,
					encode_unix_time(from_time)
					)
			else:

				url = '/personal/statement/{}/{}/'.format(
					account,
					encode_unix_time(from_time), 
					encode_unix_time(to_time)
					)
		except Exception as error: 
			print('Возникла ошибка: ', error)

		stat = self.__request(url, self.token)
		stat.reverse()
		str_stat  = ""
		list_stat = []

		for data in stat:
			str_stat+='{} {}\n'.format(data['description'], data['amount']/100)
			list_stat.append(list(data['description'],data['amount']/100))

		return (str_stat,list_stat)


""""
mono = monobank(<your monobank token>)
while True:
	intro_text = ''' 
	1. Показать курсы валют
	2. Получить данные по картам
	3. Получить выписку по карте 
	0. Выход
	'''
	print(intro_text)
	quiz = input()
	if quiz == '1':
		mono.get_mono_currency(840, 978)
	elif quiz == '2':
		mono.person_info()
	elif quiz == '3':
		print('Ваши доступные карты: ')		
		for account in mono.accounts:
			print(account['value'])

		loop = True
		while loop:
			print('Введите код вашей карты, например uah или usd')
			user_value = input()

			for account in mono.accounts:
				if user_value.lower() == account['value'].lower():
					user_account_id = account['id']
					loop = False
					break
				else:
					continue

		print('Пожалуйста введите дату начала периода выписки: 2021-02-14 13:00')
		print('Вы можете использовать максимум период до ', max_time_range())
		from_date = input()
		print('Введите до какой даты выводить выписку(автоматически ставится сегодняшняя дата): 2021-02-17 13:00')
		to_date = input()
		mono.get_money_range(user_account_id, from_date, to_date)
	else:
		break
		"""




