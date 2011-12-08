National University of Singapore Unofficial CORS API
====================================================

This is an unofficial CORS API. It consists of a Scrapy scraper project and a Flask webapp. The Flask webapp exposes a RESTful API.

The entirety of the webapp is contained in corsapi.py, a Flask app. Everything else is a Scrapy project. If you just want the scraper for your own needs, just delete corsapi.py.

There's nothing unusual about the scraper - it is a typical scrapy project. cors/items.py defines the fields needed for the Item object; cors/spiders/cors_spider.py defines the scraper and includes parsers for timetable data; pipelines.py contains the code to store the scraped data in MongoDB. Full information is available at the scrapy docs: http://doc.scrapy.org/en/0.14/index.html

Dependencies
------------
You need Flask, Scrapy, and MongoDB. If you have pip, run the following to install the first two (easy_install works as well):

    pip install Flask
    pip install scrapy

Install MongoDB by heading to the MongoDB website and following the instructions there.

Running a scrape job
--------------------
cd into the cors-api directory, and then (assuming you've installed scrapy) run:

    scrapy crawl cors

The scrapy project will start crawling the CORS website, and store all data scraped in a MongoDB collection called 'modules'.

API details
-----------
    GET /modules

Returns a full list of all the modules.

An example:

```json
 [
    {'code': 'CL3281',
	'desc': 'This module, designed for Level 2nd-4th year students (not necessarily majoring in Chinese Studies), deals with some problems not specified for attention under CL2280 or CL2281, requiring students to translate some literary works into Chinese and English respectively. Topics will include the relationship between contemporary translation theory and practice, the use of more specific semantic and cultural understanding of the text, as well as more complex formation of textual structures in the process of translation. Special attention will be paid to online resources for translators.',
	'exam': {'date': '2012-04-23', 'time': 'PM'},
	'lecture_time_table': [
		{'name': 'LECTURE Class [1]',
	    'sessions': [
	    	{'day': 2,
	        'endtime': '1700',
	        'starttime': '1400'
	        'location': 'AS7/0119',
	        'occurence': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
	        }]
	    }
	],
	'mc': '4',
	'name': 'Advanced Translation',
	'preclusion': 'Nil',
	'prerequisite': 'CL2280 or CL2281',
	'tutorial_time_table': 'null',
	'workload': '3-0-0-2-5'
	},
	{
		<another dict, representing another module>
	}
]
```

Note that it returns a list of dictionaries, each dictionary representing a module.

    GET /module/:modulecode

Returns the details for just that module code, as follows:

```json
{
	'code': 'CH2223',
	'mc': '4',
	'name': 'Chinese Fiction',
	'desc': 'This module is designed to acquaint students with the historical evolution and characteristics of ancient Chinese fiction. It covers different genres of the fictional narrative tradition, zhiguai, zhiren, Tang chuanqi short tale, huaben colloquial short story and full-length xiaoshuo. The course is open to students across the University with an interest in Chinese literary tradition and particularly in Chinese fiction.',
	'exam': {'date': '2012-04-30', 'time': 'EVENING'},
	'lecture_time_table': [
		{'name': 'LECTURE Class [1]',
	    'sessions': [
	    		{'day': 3,
	            'endtime': '1800',
	            'starttime': '1600',
	            'location': 'AS7/0101',
	            'occurence': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
	            }]
	    }],
	'tutorial_time_table': [
		{'name': 'TUTORIAL Class [E1]',
	    'sessions': [
	    	{'day': 3,
	        'endtime': '1400',
	        'location': 'AS7/0101',
	        'occurence': [2, 4, 6, 8, 10, 12],
	        'starttime': '1200'}
	        ]
	    },
	    {'name': 'TUTORIAL Class [E2]',
	    'sessions': [
	    	{'day': 4,
	        'endtime': '1400',
	        'location': 'AS3/0215',
	        'occurence': [2, 4, 6, 8, 10, 12],
	         'starttime': u'1200'}
	    	]
	    }
	],
	'preclusion': 'NIl',
	'prerequisite': u"Must obtain: 1) At least a B4 for (a) Higher Chinese at GCE 'O' Level, or (b) Chinese Language at GCE 'AO' Level (at GCE 'A' Level examination); OR 2) At least a pass for (a) Chinese at GCE 'A' Level, or (b) Higher Chinese at GCE 'A' Level; OR 3) At least C grade for Chinese Language (H1CL) at GCE 'A' Level; OR 4) At least a pass for (a) Chinese Language and Literature (H2CLL) at GCE 'A' Level, or (b) Chinese Language and Literature (H3CLL) at GCE 'A' Level. 5) Equivalent qualifications may be accepted.",
	'workload': '2-1-0-2-5'
}
```
Note that occurences are a list of numbers representing weeks in the semester. Most modules have classes every week, but some don't. For instance, odd weeks and even weeks are represented with [1,3,5,7,9,11,13] and [2,4,6,8,10,12] respectively.

Day represents the days of the week, with Monday being 1 and Sunday being 7.

    GET /timetable/:modulecode

Returns the lecture and tutorial timetables for the module code, like so:

```json
{
	"tutorial_time_table": [
		{"name": "TUTORIAL Class [1]",
		"sessions": [
			{"starttime": "1000",
			"endtime": "1200",
			"occurence": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
			"day": 2,
			"location": "I3/3-47"}
		]},
		{"name": "TUTORIAL Class [2]",
		"sessions": [
			{"starttime": "1200",
			"endtime": "1400",
			"occurence": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
			"day": 2,
			"location": "I3/3-47"}
		]}
	],
	"lecture_time_table": [
		{"name": "LECTURE Class [1]",
		"sessions": [
			{"starttime": "1000",
			"endtime": "1200",
			"occurence": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
			"day": 5,
			"location": "COM1/212"
			}
		]}
	]
}
```



Work-in-progress notes:
-----------------------
* The scraper takes about 18 minutes to run while on the NUS network.
* This project runs on MongoDB
* The scraper deletes everything in MongoDB before beginning a scrape job. #tofix