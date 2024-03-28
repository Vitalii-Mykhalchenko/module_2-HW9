import scrapy


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'authors.json'
    }
    
    def parse(self, response):
        for author_href in response.xpath("//div[@class='quote']//a[text()='(about)']/@href"):
            yield response.follow(author_href, callback=self.parse_author)
            
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(next_page,callback=self.parse)

    def parse_author(self, response):
        item =  {
            "fullname": response.xpath("//h3/text()").get(),
            "born_date": response.xpath('//span[@class="author-born-date"]/text()').get(),
            "born_location": response.xpath('//span[@class="author-born-location"]/text()').get(),
            "description": response.xpath('//div[@class="author-description"]/text()').get().strip()


            }
        yield item


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'quotes.json'
    }

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            item = self.parse_quote(quote)
            yield item
            
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_quote(self, quote):
        item = {
            'tags': quote.xpath("div[@class='tags']/a/text()").extract(),
            "author":  quote.xpath(".//small[@class='author']/text()").get(),
            "quote": quote.xpath(".//span[@class='text']/text()").get()
        }
        return item
          
