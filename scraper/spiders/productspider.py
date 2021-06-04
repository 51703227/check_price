import scrapy
from datetime import date

class cellphonetSpider(scrapy.Spider):
    name = 'cellphone'
    start_urls = ['https://cellphones.com.vn/mobile.html']

    def parse(self,response):
        for product in response.css('li.cate-pro-short'):
            try:
                yield{
                    'ten' : product.css('h3::text').get().replace('\t',''),
                    'giamoi' : product.css('.special-price span::text').get().replace('\xa0₫',''),
                    'giagoc' : product.css('.old-price span::text').get().replace('\xa0₫',''),
                    'url' : product.css('.lt-product-group-info a').attrib['href'],
                    'img' : product.css('.lt-product-group-image img').attrib['data-src'],
                    'ngay': product.css('.lt-product-group-image img').attrib['data-src'],
                    'loaisanpham':product.css('.lt-product-group-image img').attrib['data-src'],
                    'thuonghieu':product.css('.lt-product-group-image img').attrib['data-src'],
                    'mausac':product.css('.lt-product-group-image img').attrib['data-src'],
                    'bonho':product.css('.lt-product-group-image img').attrib['data-src'],

                }
            except:
                yield{
                    'ten' : product.css('h3::text').get().replace('\t',''),
                    'giamoi' : 0,
                    'giagoc' : 0,
                    'url' : product.css('.lt-product-group-info a').attrib['href'],
                    'img' : product.css('.lt-product-group-image img').attrib['data-src'],
                    'ngay': product.css('.lt-product-group-image img').attrib['data-src'],
                    'loaisanpham':product.css('.lt-product-group-image img').attrib['data-src'],
                    'thuonghieu':product.css('.lt-product-group-image img').attrib['data-src'],
                    'mausac':product.css('.lt-product-group-image img').attrib['data-src'],
                    'bonho':product.css('.lt-product-group-image img').attrib['data-src'],
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

class nguyenkimSpider(scrapy.Spider):
    name = 'nguyenkim'
    start_urls = ['https://www.nguyenkim.com/dien-thoai-di-dong/']

    def parse(self,response):
        for product in response.css('div.item-list'):
            try:
                yield{
                    'ten': product.css('.product-body .product-title a::text').get(),
                    'url': product.css('.product-header a').attrib['href'],
                    'image': product.css('.lt-product-group-image a > img::attr(src)').get(),
                    'ngay': date.today().strftime("%d/%m/%Y"),
                    'loaisanpham':'dienthoai',
                    'thuonghieu':'iphone',
                    'thuoctinh': 
                    [
                        {
                        'mausac': product.css('.lt-product-group-info .old-price .price::text').get(),
                        'bonho': product.css('.lt-product-group-info .old-price .price::text').get(),
                        'giamoi': product.css('.lt-product-group-info .price-box .special-price .price::text').get(),
                        'giagoc': product.css('.lt-product-group-info .old-price .price::text').get()
                        }
                    ]
                }
            except:
                yield{
         
                }
        next_page = response.css('div.pages ul:last-child li a').attrib['href']
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)