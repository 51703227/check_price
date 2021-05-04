import scrapy

class ProductSpider(scrapy.Spider):
    name = 'product'
    start_urls = ['https://cellphones.com.vn/mobile.html']

    def parse(self,response):
        for product in response.css('li.cate-pro-short'):
            try:
                yield{
                    'name' : product.css('h3::text').get().replace('\t',''),
                    'special-price' : product.css('.special-price span::text').get().replace('\xa0₫',''),
                    'old-price' : product.css('.old-price span::text').get().replace('\xa0₫',''),
                    'url' : product.css('.lt-product-group-info a').attrib['href'],
                    'img' : product.css('.lt-product-group-image img').attrib['data-src'],
                }
            except:
                yield{
                    'name' : product.css('h3::text').get().replace('\t',''),
                    'special-price' : 0,
                    'old-price' : 0,
                    'url' : product.css('.lt-product-group-info a').attrib['href'],
                    'img' : product.css('.lt-product-group-image img').attrib['data-src'],
                }
        next_page = response.css('div.pages ul:last-child li a').attrib['href']
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)

class fptshopSpider(scrapy.Spider):
    name = 'fptshop'
    start_urls = ['https://fptshop.com.vn/dien-thoai']

    def parse(self,response):
        for product in response.css('div.cdt-product.product-sale'):
            try:
                yield{
                    'name' : product.css('h3::text').get().replace('\t',''),
                    'special-price' : product.css('.special-price span::text').get().replace('\xa0₫',''),
                    'old-price' : product.css('.old-price span::text').get().replace('\xa0₫',''),
                    'url' : product.css('.lt-product-group-info a').attrib['href'],
                    'img' : product.css('.lt-product-group-image img').attrib['data-src'],
                }
            except:
                yield{
                    'name' : product.css('h3::text').get().replace('\t',''),
                    'special-price' : 0,
                    'old-price' : 0,
                    'url' : product.css('.lt-product-group-info a').attrib['href'],
                    'img' : product.css('.lt-product-group-image img').attrib['data-src'],
                }
        next_page = response.css('div.pages ul:last-child li a').attrib['href']
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)