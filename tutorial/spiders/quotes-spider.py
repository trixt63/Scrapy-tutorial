import scrapy
# II: Using item loader
from scrapy.loader import ItemLoader
from tutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/']


    def parse(self, response):
        self.logger.info('Parse function called on {}'.format(response.url))
        quotes = response.xpath("//div[@class='quote']")
        # quotes = response.css('div.quote')

        for quote in quotes:
            # initiate object 'loader':
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            # add data to object:
            loader.add_xpath('quote_content', ".//span[@class='text']/text()")
            loader.add_xpath('tags', './/div[@class="tag"]//text()')

            # Pass two fields 'quote_content' and 'tags' from quote page,
            # then issue another request to get the author page
            quote_item = loader.load_item() # 'quote_item' contain 2 fields that need to pass
            author_url = quote.xpath(".//a/@href").get() # partial url for author's about page
            yield response.follow(author_url, self.parse_author, meta={'quote_item': quote_item}) # add a meta data variable


        # go to Next page
        for a in response.css('li.next a'):
            yield response.follow(a, self.parse)

    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item=quote_item, response=response)
        loader.add_xpath('author_name', "//*[@class='author-title']/text()")
        loader.add_xpath('author_birthday', "//*[@class='author-born-date']/text()")
        loader.add_xpath('author_bornlocation', "//*[@class='author-born-location']/text()")
        loader.add_xpath('author_bio', '//div[@class="author-description"]/text()')

        yield loader.load_item()


