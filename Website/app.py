from flask import Flask, render_template, url_for, request
from mongoengine import *
import json
import os
import csv

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')
db = connect('test')

class Country(Document):
	name = StringField()
	data = DictField()

@app.route('/add_data')
def add_data():
	for file in os.listdir(app.config['FILES_FOLDER']):
		filename = os.fsdecode(file)
		path = os.path.join(app.config['FILES_FOLDER'], filename)
		f = open(path)
		r = csv.DictReader(f)
		d = list(r)
		count = 0
		for data in d:
			country = Country()
			dict = {}
			for key in data:
				if key == "country":
					country.name = d[count]['country']
					count += 1
				else:
					f = filename.replace(".csv","") # we want to trim off the ".csv" as we can't save anything with a "." as a mongodb field name
					if f in dict: # check if this filename is already a field in the dict
						dict[f][key] = data[key] # if it is, just add a new subfield which is key : data[key] (value)
					else:
						dict[f] = {key:data[key]} # if it is not, create a new object and assign it to the dict
				
				country.data = dict
	
			country.save()
	return render_template('index.html')

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
	try:
		if country_name is None:
			length = 2000
			country = Country.objects.all()
			labels = []
			data = []
			for c in country:
				labels.append(c.name)
				data.append(c["data"]["children"]["2020"])
			return render_template('country.html', title="Average children per family", max=10, labels=labels, data=data, length=length, country_name="All Countries")
		else:
			length = 500
			country = Country.objects.get(name=country_name)
			labels = []
			data = []
			for c in range(2000, 2021):
				labels.append(c)
				data.append(country["data"]["children"][str(c)])
			return render_template('country.html', title="Average children per family", max=10, labels=labels, data=data, length=length, country_name=country_name)
	except DoesNotExist:
		return "Not Found"
	

@app.route('/countries', methods=['POST'])
def addCountry():
	name = request.form['name']
	new_country = Country(name=name)
	new_country.save()
	return new_country.to_json()

if __name__ == "__main__":
	app.run(debug=True, port=8080)
	#app.run(host='0.0.0.0', debug=True, port=80)
