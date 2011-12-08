#!/usr/bin/env python
"""Flask webapp. Exposes a RESTful API.
"""
from flask import Flask, url_for, render_template, abort, Response
from pymongo import Connection
try:
	import simplejson as json
except ImportError:
	import json

app = Flask(__name__)

# mongoDB connection
connection = Connection('localhost', 34006) # the default is 27017
db = connection.corsdatabase

@app.route('/')
def main():
	return 'Hello World'

@app.route('/api/modules/', methods=['GET'])
def get_all_modules():
	"""Returns all the modules.
	"""
	entities = db['modules'].find()
	ls = []
	for e in entities:
		del e['_id']
		ls.append(e)
	return Response(json.dumps(ls), mimetype='application/json')

@app.route('/api/module/<modulecode>', methods=['GET'])
def get_module(modulecode):
	"""Returns details for a specific module
	:params string modulecode
	"""
	entity = db['modules'].find_one({'code': modulecode})
	if not entity:
		abort(404, 'Module %s not found' % modulecode)
	del entity['_id'] # the _id object isn't JSON serializable
	return Response(json.dumps(entity), mimetype='application/json')

@app.route('/api/timetable/<modulecode>', methods=['GET'])
def get_module_time(modulecode):
	"""Returns lecture and tutorial timetables
	"""
	entity = db['modules'].find_one({'code': modulecode})
	if not entity:
		abort(404, 'Module %s not found' % modulecode)
	return Response(json.dumps({'lecture_time_table': entity['lecture_time_table'],
	'tutorial_time_table': entity['tutorial_time_table']}),
		mimetype='application/json')

if __name__ == '__main__':
	app.run(debug=True)