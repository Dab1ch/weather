from flask import Flask, session, request, redirect, url_for, render_template
import os


def choose_city():
	
	if request.method == 'POST':
		session['city'] = request.form.get('city')
		
		if session['city'] == 0:
			return redirect(url_for('choose_city'))
		return redirect(url_for('view'))
	
	return render_template('start.html')

def view():
	pass

folder = os.getcwd()
app = Flask(__name__, template_folder = folder, static_folder = folder)
app.config['SECRET_KEY'] = 'yapi'

app.add_url_rule('/', 'choose_city', choose_city, methods=['POST', 'GET'])
app.add_url_rule('/view', 'view', view, methods=['POST', 'GET'])

if __name__ == "__main__":
	app.run()