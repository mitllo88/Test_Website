from flask import Flask, render_template, url_for
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
	Country(name="New Zealand").save()
	Country(name="Australia").save()
	Country(name="Japan").save()
	return render_template('index.html')
	
@app.route('/inspirations')
@app.route('/inspiration')
def inspiration():
	return render_template('page_1.html')
	
@app.route('/loadData')
def load():
	return 'Loaded!'
	
@app.route('/listCountriesTest')
def listCountriesTest():
	return Country.objects.to_json()
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)
