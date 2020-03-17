from flask import Flask, render_template, url_for, request
from mongoengine import *
import json

app = Flask(__name__, template_folder='templates')
connect('test')

class Country(Document):
	name = StringField()

@app.route('/')
@app.route('/home')
@app.route('/Home')
def index():
	return render_template('index.html')
	
@app.route('/inspirations')
@app.route('/inspiration')
def inspiration():
	return render_template('page_1.html')
	
@app.route('/about')
def about():
	return render_template('page_2.html')	

@app.route('/loadData')
def load():
	Country(name="New Zealand").save()
	Country(name="Australia").save()
	Country(name="Japan").save()
	
@app.route('/countries', methods=['GET'])
@app.route('/countries/<country_name>', methods=['GET'])
def getCountry(country_name=None):
	countries = None
	if country_name is None:
		return Country.objects.to_json()
	else:
		return Country.objects.get(name=country_name).to_json()
	

@app.route('/countries', methods=['POST'])
def addCountry():
	name = request.form['name']
	new_country = Country(name=name)
	new_country.save()
	return new_country.to_json()

if __name__ == "__main__":
	app.run(debug=True, port=8080)
