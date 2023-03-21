from flask import Flask, session, request, redirect, url_for, render_template
import os
from bs4 import BeautifulSoup as bs
import requests
from datetime import date


months = ['январь', 'февраль', "март", "апрель", "май", "июнь", "июль",
"август", "сентябрь", "октябрь", "ноябрь", "декабрь"]

monthdays = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]


def choose_city():
	
	if request.method == 'POST':
		session['city'] = request.form.get('city')
		
		return redirect(url_for('view'))
	
	return render_template('start.html')

def view():

	current_date = date.today()
	print(current_date.day, current_date.month)

	day = current_date.day
	for i in range(current_date.month - 1):
		day += monthdays[i]

	URL_TEMPLATE = "https://meteoinfo.ru/forecasts/russia/moscow-area/moscow"
	r = requests.get(URL_TEMPLATE)
	
	r = bs(r.text, "html.parser")

	temps = r.findAll('span', class_ = 'fc_temp_short')
	temps = ''.join(map(str, temps))
	temps = temps.split('<i>')
	temps.pop(0)

	for i in range(len(temps)):
		temps[i] = temps[i][:temps[i].find('</i>')]
	print(temps)

	days = []

	for i in range(6):
		for j in range(len(monthdays)):
			day = day % 365
			if monthdays[j] > day:
				days.append(str(months[j]) + ' ' + str(day - monthdays[j - 1]))
				break 
		day+=1


	#print(r.text[index + 20:index + 40])	
	return render_template('finish.html', days = days, temps = temps)

folder = os.getcwd()
app = Flask(__name__, template_folder = folder, static_folder = folder)
app.config['SECRET_KEY'] = 'yapi'

app.add_url_rule('/', 'choose_city', choose_city, methods=['POST', 'GET'])
app.add_url_rule('/view', 'view', view, methods=['POST', 'GET'])

if __name__ == "__main__":
	app.run()