from flask import Flask, url_for, render_template, abort
from pymongo import Connection
try:
	import simplejson as json
except ImportError:
	import json

app = Flask(__name__)

@app.route('/')
def main():
	return 'Hello World'

@app.route('api/v1/<modulecode>', methods=['POST'])
def api_v1(modulecode):
	pass

if __name__ == '__main__':
	app.run()