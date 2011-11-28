from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from cors.items import CorsItem

class CorsSpider(CrawlSpider):
	name = "cors"
	allowed_domains = ["nus.edu.sg"]
	start_urls = [
		"https://aces01.nus.edu.sg/cors/jsp/report/ModuleInfoListing.jsp",
        "https://aces01.nus.edu.sg/cors/jsp/report/GEMInfoListing.jsp",
        "https://aces01.nus.edu.sg/cors/jsp/report/SSMInfoListing.jsp"
	]

	# Follow links that contain the following rule (in this case to individual module pages)
	rules = (
		Rule(SgmlLinkExtractor(allow=('ModuleDetailedInfo\.jsp', )), callback='parse_module'),
	)

	def parse_module(self, response):
		"""Scrapes each individual module page. Scraped items are passed to pipelines.py,
		where they are processed and save to mongodb
		"""
		hxs = HtmlXPathSelector(response)
		module = hxs.select('id("wrapper")/table/tr[2]/td/table[1]/tr[3]/td/table')

		item = CorsItem()

		# XPath selectors
		code = module.select('tr[position()=2]/td[position()=2]/text()').extract()
		name = module.select('tr[position()=3]/td[position()=2]/text()').extract()
		desc = module.select('tr[position()=4]/td[position()=2]/text()').extract()
		mc = module.select('tr[position()=7]/td[position()=2]/text()').extract()
		lecture = module.select('tr[position()=2]/td/div/table/tr/td/text()').extract()
		exam = module.select('tr[position()=6]/td[position()=2]/text()').extract()
		prereq = module.select('tr[position()=8]/td[position()=2]/text()').extract()
		preclu = module.select('tr[position()=9]/td[position()=2]/text()').extract()
		workload = module.select('tr[position()=10]/td[position()=2]/text()').extract()

		# strip() removes \n and \r; also note that lecture returns multiple strings in a list
		item['code'] = code[0].strip() if code else u'null'
		item['name'] = name[0].strip() if name else u'null'
		item['desc'] = desc[0].strip() if desc else u'null'
		item['mc'] = mc[0].strip() if mc else u'null'
		item['lecture_time_table'] = u' '.join([w.strip() for w in lecture]) if lecture else u'null'
		item['exam'] = exam[0].strip() if exam else u'null'
		item['prerequisite'] = prereq[0].strip() if prereq else u'null'
		item['preclusion'] = preclu[0].strip() if preclu else u'null'
		item['workload'] = workload[0].strip() if workload else u'null'

		return item
