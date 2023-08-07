import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "jsons/quotes.json"}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response, **kwargs):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": ''.join(quote.xpath("span/small/text()").extract()),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "jsons/authors.json"}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = base_urls = ['http://quotes.toscrape.com/']

    def parse(self, response, **kwargs):
        for author_div in response.css("div.quote"):
            author_info = {
                "fullname": author_div.css("small.author::text").get(),
            }
            author_about = response.urljoin(author_div.css("a::attr(href)").get())
            yield scrapy.Request(author_about, callback=self.parse_author_info, meta={"author_info": author_info})

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link, callback=self.parse)

    def parse_author_info(self, response):
        author_info = response.meta["author_info"]
        author_info.update({
            "born_date": response.css("span.author-born-date::text").get(),
            "born_location": response.css("span.author-born-location::text").get(),
            "description": response.css("div.author-description::text").get().strip(),
        })
        yield author_info


process = CrawlerProcess()
process.crawl(QuotesSpider)
process.crawl(AuthorsSpider)
process.start()
