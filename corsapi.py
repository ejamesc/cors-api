#!/usr/bin/env python
"""Flask webapp. Exposes a RESTful API.
"""
from flask import Flask, url_for, render_template, abort, Response, request
import gc
from pymongo import Connection
import re
try:
	import simplejson as json
except ImportError:
	import json

app = Flask(__name__)

def js_response_helper(data_json, mime):
	"""Assumes that callback is last arg.
	"""
	res = ""
	url = request.url
	cb_reg = re.compile('callback=([^&]*)')
	cb = cb_reg.search(url)
	if cb:
		res = cb.expand("\g<1>")
		res = res + "(" + data_json + ");"
		return Response(res, mimetype='application/javascript')
	else:
		res = data_json
		return Response(res, mimetype=mime)


# mongoDB connection
connection = Connection('localhost', 34006) # the default is 27017
db = connection.corsdatabase

errorjson = json.dumps({"message": "Not Found"})

@app.route('/')
def main():
	return render_template('front.html')

@app.route('/modules/', methods=['GET'])
def get_all_modules():
	"""Returns all the modules.
	"""
	entities = db['modules'].find()
	if not entities:
		return js_response_helper(errorjson, 'application/json')
	ls = []
	for e in entities:
		del e['_id']
		ls.append(e)
	return js_response_helper(json.dumps(ls), 'application/json')

@app.route('/module/<modulecode>', methods=['GET'])
def get_module(modulecode):
	"""Returns details for a specific module
	:params string modulecode
	"""
	entity = db['modules'].find_one({'code': modulecode})
	if not entity:
		return js_response_helper(errorjson, 'application/json')
	del entity['_id'] # the _id object isn't JSON serializable
	return js_response_helper(json.dumps(entity), 'application/json')

@app.route('/modules/search/<regex>', methods=['GET'])
def search_modules(regex):
	"""Returns details for all modules that match given regex
	:params string regex
	"""
	entities = db['modules'].find({'code': re.compile('%s'%regex) })
	ls = []
	for e in entities:
		del e['_id']
		ls.append(e)
	if not ls:
		return js_response_helper(errorjson, 'application/json')
	return js_response_helper(json.dumps(ls), 'application/json')

@app.route('/timetable/<modulecode>', methods=['GET'])
def get_module_time(modulecode):
	"""Returns lecture and tutorial timetables
	:params string modulecode
	"""
	entity = db['modules'].find_one({'code': modulecode})
	if not entity:
		return js_response_helper(errorjson, 'application/json')
	return js_response_helper(json.dumps({'lecture_time_table': entity['lecture_time_table'],
	'tutorial_time_table': entity['tutorial_time_table']}),
		'application/json')

if __name__ == '__main__':
	app.run(debug=True)