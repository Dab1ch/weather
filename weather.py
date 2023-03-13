from flask import Flask, session, request, redirect, url_for, render_template
import os
from bs4 import BeautifulSoup as bs
import requests

def choose_city():
	
	if request.method == 'POST':
		session['city'] = request.form.get('city')
		
		return redirect(url_for('view'))
	
	return render_template('start.html')

def view():
	
	URL_TEMPLATE = "https://meteoinfo.ru/forecasts/russia/moscow-area/moscow"
	r = requests.get(URL_TEMPLATE)
	
	index = r.text.find('<table')
	
	print(r.text[index + 20:index + 40])
	
	return render_template('finish.html', index = index)

folder = os.getcwd()
app = Flask(__name__, template_folder = folder, static_folder = folder)
app.config['SECRET_KEY'] = 'yapi'

app.add_url_rule('/', 'choose_city', choose_city, methods=['POST', 'GET'])
app.add_url_rule('/view', 'view', view, methods=['POST', 'GET'])

if __name__ == "__main__":
	app.run()