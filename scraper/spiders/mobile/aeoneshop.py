import scrapy
import os
from datetime import date
from ..productspider import get_attr_from_name,name_processing,format_price,format_bonho,format_mausac

basedir = os.path.dirname(os.path.realpath('__file__'))

# crawl data from aeoneshop.com
class aeoneshop(scrapy.Spider):
    name = 'aeoneshop'
    start_urls = ['https://aeoneshop.com/collections/dien-thoai-di-dong', ]

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.product-list > div.col-sm-6')

        self.log('products ' + str(len(products)))
        for product in products:
            title = name_processing(product.css('div.box-pro-detail > h3.pro-name > a::text').get()).title()
            item_link = 'https://aeoneshop.com' + str(
                product.css('div.box-pro-detail > h3.pro-name > a::attr(href)').get())
            thuong_hieu = item_link.split('/')[6].split('-')[4]

            item = {
                'ten': title,
                'url': item_link,
                'image': '',
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'dienthoai',
                'thuonghieu': thuong_hieu
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        next_page_url = 'https://aeoneshop.com' + str(response.css(
            '#pagination > div.col-lg-2.col-md-2.col-sm-3.hidden-xs.controlArrow.text-right > a::attr(href)').extract_first())
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = format_price(
            response.css('#AddToCartForm > div.groupPriceDetail > span.price_max.detailDel > span::text').get())
        option_rom = None

        option_color = None
        option_new_price = format_price(
            response.css('#AddToCartForm > div.groupPriceDetail > span.price_min > span::text').get())
        active = True

        image2 = 'https:' + response.css(
            'div.col-xs-12.col-sm-4 > div > div.main-detail-product > img::attr(src)').get()

        attributes = []
        attributes.append({
            'bonho': option_rom,
            'mausac': option_color,
            'giagoc': option_old_price,
            'giamoi': option_new_price,
            'active': active
        })

        item['thuoctinh'] = attributes
        item['image'] = image2
        item['tskt'] = response.css('div.itemTab.active > table').get()
        item['mota'] = response.css('div.itemTab.active > p:nth-child(6)').get()
        return item
