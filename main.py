import requests # Модуль для обработки URL
from bs4 import BeautifulSoup # Модуль для работы с HTML
import time # Модуль для остановки программы
import smtplib # Модуль для работы с почтой

# Основной класс
class Currency:
	# Ссылка на нужную страницу
	virus = 'https://www.worldometers.info/coronavirus/'
	# Заголовки для передачи вместе с URL
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

	current_converted_price = 0
	difference = 5 # Разница после которой будет отправлено сообщение на почту

	def __init__(self):
		# Установка курса валюты при создании объекта
		self.current_converted_price = int(self.get_currency_price(0).replace(",", ""))

	# Метод для получения курса валюты
	def get_currency_price(self, val):
		# Парсим всю страницу
		full_page = requests.get(self.virus, headers=self.headers)

		# Разбираем через BeautifulSoup
		soup = BeautifulSoup(full_page.content, 'html.parser')

		# Получаем нужное для нас значение и возвращаем его
		convert = soup.findAll("div", {"class":"maincounter-number"})
		return convert[val].text

	# Проверка изменения валюты
	def check_currency(self):
		currency1 = int(self.get_currency_price(0).replace(",", ""))
		currency2 = int(self.get_currency_price(1).replace(",", ""))
		currency3 = int(self.get_currency_price(2).replace(",", ""))
		if currency1 >= self.current_converted_price + self.difference:
			print("\nКоличество больных возросло.")
			self.current_converted_price=currency1
		elif currency1 <= self.current_converted_price - self.difference:
			print("\nКоличество больных упало.")
			self.current_converted_price=currency1

		print("\nНа данный момент " + str(currency1) + " заболевших.")
		print("\nНа данный момент " + str(currency2) + " умерших.")
		print("\nНа данный момент " + str(currency3) + " вылеченных.")
		time.sleep(3) # Засыпание программы на 3 секунды
		self.check_currency()

	# Отправка почты через SMTP
	def send_mail(self):
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()

		server.login('ВАША ПОЧТА', 'ПАРОЛЬ')

		subject = 'Currency mail'
		body = 'Currency has been changed!'
		message = f'Subject: {subject}\n{body}'

		server.sendmail(
			'От кого',
			'Кому',
			message
		)
		server.quit()

# Создание объекта и вызов метода
currency = Currency()
currency.check_currency()
