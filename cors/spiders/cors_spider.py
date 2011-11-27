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

	rules = (
		Rule(SgmlLinkExtractor(allow=('ModuleDetailedInfo\.jsp', )), callback='parse_module'),
	)

	def parse_module(self, response):
		hxs = HtmlXPathSelector(response)
		module = hxs.select('id("wrapper")/table/tr[2]/td/table[1]/tr[3]/td/table')

		item = CorsItem()

		item['code'] = module.select('tr[position()=2]/td[position()=2]/text()').extract()
		item['name'] = module.select('tr[position()=3]/td[position()=2]/text()').extract()
		item['desc'] = module.select('tr[position()=4]/td[position()=2]/text()').extract()
		item['mc'] = module.select('tr[position()=7]/td[position()=2]/text()').extract()
		item['lecture_time_table'] = module.select('tr[position()=2]/td/div/table/tr/td/text()').extract()
		item['exam'] = module.select('tr[position()=6]/td[position()=2]/text()').extract()
		item['prerequisite'] = module.select('tr[position()=8]/td[position()=2]/text()').extract()
		item['preclusion'] = module.select('tr[position()=9]/td[position()=2]/text()').extract()
		item['workload'] = module.select('tr[position()=10]/td[position()=2]/text()').extract()
		return item
