import scrapy
import os
from datetime import date
from ..productspider import get_attr_from_name,name_processing,format_price,format_bonho,format_mausac

basedir = os.path.dirname(os.path.realpath('__file__'))


def mobileworld_name(link):
    temp_name = link.split('/')[2].split('-')
    t = 0
    name = ''
    for i in temp_name:
        if t <= 4:
            name = name + i + ' '
            t = t + 1
    return name


# class crawl data from mobile world
class mobileworld(scrapy.Spider):
    name = 'mobileworld'
    start_urls = ['https://mobileworld.com.vn/collections/dien-thoai', ]

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.collection-body > div.grid-uniform > div.grid__item')

        self.log('products ' + str(len(products)))
        for product in products:

            link__ = product.css('div.product-item-info > div.product-title > a::attr(href)').get()
            item_link = 'https://mobileworld.com.vn/collections/dien-thoai' + link__
            thuong_hieu = link__.split('/')[2].split('-')[0]
            image1 = product.css('div.product-item > div.product-img > a > img::attr(src)').get()
            image = 'https:' + image1
            ten = product.css('div.product-item-info > div.product-title > a::text').get()
            title = mobileworld_name(link__)

            if thuong_hieu == 'galaxy':
                thuong_hieu = 'samsung'

            item = {
                'ten': name_processing(title),
                'url': item_link,
                'image': image,
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'dienthoai',
                'thuonghieu': thuong_hieu
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        next_page_url_1 = 'https://mobileworld.com.vn' + response.css(
            '#pagination- > div > span.nextPage > a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url_1)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = format_price(
            response.css('div.productInfo > div.grid > div.grid__item > div.pro-price > span::text').get())
        option_rom = format_bonho(response.css('div.productTitle > h1::text').get())

        option_color = response.css('div.n-sd.swatch-element.color.den > label > span::text').get()
        option_new_price = option_old_price
        active = True

        attributes = []
        attributes.append({
            'bonho': option_rom,
            'mausac': format_mausac(option_color),
            'giagoc': option_old_price,
            'giamoi': option_new_price,
            'active': active
        })

        item['thuoctinh'] = attributes
        item['tskt'] = response.css('div.info').get()
        item['mota'] = response.css('div.product-description-wrapper > div.pdDesscription').get()
        return item