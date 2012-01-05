# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from icalendar import Calendar, Event, vDatetime
from datetime import datetime, time, date, timedelta
import os
def display(cal):
	return cal.as_string().replace('\r\n','\n').strip()

SEM_START = datetime(2012,1,9,0,0)
RECESS_WEEK = 7
TOTAL_WEEKS = 14
WEEK2ACTUAL=[1,2,3,4,5,6,8,9,10,11,12,13,14]
week = timedelta(days=7)
day = timedelta(days=1)
hour = timedelta(hours=1)
minute = timedelta(minutes=1)

class CorsPipeline(object):
	def process_item(self, item, spider):
		cal = Calendar()
		cal.add('calscale','GREGORIAN')
		cal.add('version','2.0')
		
		if item['exam'] != 'null':
			exam = Event()
			exam.add('summary', '%s exam'%item['code'])
			exam.add('dtstart', datetime.combine(item['exam']['date'], time()))
			exam.add('dtend', 	datetime.combine(item['exam']['date'], time(12,0)))
			cal.add_component(exam)
			
		if item['lecture_time_table'] != 'null':
			for l in item['lecture_time_table']:
				for lec in l['sessions']:
					dow = lec['day']
					ts = int(lec['starttime'])
					te = int(lec['endtime'])
					ts_hr,ts_min = ts/100, ts%100
					te_hr,te_min = te/100, te%100
					for i in lec['occurence']:
						lectureday = SEM_START + (dow-1)*day  + (WEEK2ACTUAL[i-1]-1)*week
						lecture = Event()
						lecture.add('summary', '%s %s'%(item['code'],l['name']))
						setstartend(lecture,lectureday + ts_hr*hour + ts_min*minute,lectureday + te_hr*hour + te_min*minute)
						cal.add_component(lecture)
						
		if item['tutorial_time_table'] != 'null':
			for t in item['tutorial_time_table']:
				for tut in t['sessions']:
					dow = tut['day']
					ts = int(tut['starttime'])
					te = int(tut['endtime'])
					ts_hr,ts_min = ts/100, ts%100
					te_hr,te_min = te/100, te%100
					for i in tut['occurence']:
						tutday = SEM_START + (dow-1)*day  + (WEEK2ACTUAL[i-1]-1)*week
						tutorial = Event()
						tutorial.add('summary', '%s %s'%(item['code'],t['name']))
						setstartend(tutorial,tutday + ts_hr*hour + ts_min*minute,tutday + te_hr*hour + te_min*minute)
						cal.add_component(tutorial)
						
		f = open(os.path.join('ics','%s.ics'%item['code']),'wb')
		f.write(cal.as_string())
		f.close()
		
		return item
def setstartend(event,start,end):
	event['dtstart'] = vDatetime(start).ical()
	event['dtend'] = vDatetime(end).ical()
