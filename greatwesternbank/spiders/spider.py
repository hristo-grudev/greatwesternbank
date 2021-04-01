import scrapy

from scrapy.loader import ItemLoader

from ..items import GreatwesternbankItem
from itemloaders.processors import TakeFirst


class GreatwesternbankSpider(scrapy.Spider):
	name = 'greatwesternbank'
	start_urls = ['https://www.greatwesternbank.com/blog/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="blog-post__body"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@aria-label="Next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="col-md-10 col-md-push-1 col-lg-8 col-lg-push-2"]//text()[normalize-space() and not(ancestor::h1 | ancestor::span | ancestor::div[@class="blog-post-category-list" or @class="blog-post-meta clearfix" or @class="blog-post-category-list blog-post-category-list--bottom" or @class="blog-post__body"] | ancestor::a | ancestor::h2[@class="h3 text-uppercase"])]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="blog-post-date"]/text()').get()

		item = ItemLoader(item=GreatwesternbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
