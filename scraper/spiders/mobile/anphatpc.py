import scrapy
import os
from datetime import date
from ..productspider import get_attr_from_name,name_processing,format_price,format_bonho,format_mausac

basedir = os.path.dirname(os.path.realpath('__file__'))


#class crawl data from www.anphatpc.com.vn
class anphatpc(scrapy.Spider):
    name = 'anphatpc'
    start_urls = ['https://www.anphatpc.com.vn/dien-thoai-di-dong.html', ]

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.p-list-container > div.p-item')


        self.log('products ' + str(len(products)))
        for product in products:
            temp_title = product.css('div.p-item > div.p-text > a::text').get()

            title = ''
            if temp_title:
                title = name_processing(temp_title).title()

            item_link = 'https://www.anphatpc.com.vn' + str(product.css('div.p-text > a::attr(href)').get())
            image = product.css('div.p-item > a > img::attr(data-src)').get()

            item = {
                'ten': title,
                'url': item_link,
                'image': image,
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'dienthoai',
                'thuonghieu': 'apple'
            }

            option_rom = None
            temp_option_rom = product.css('div.p-item > div.p-text > a::text').get()
            if temp_option_rom:
                option_rom = format_bonho(temp_option_rom)

            option_new_price = format_price(product.css('div.price-container > span.p-price::text').get())
            option_old_price = format_price(product.css('div.price-container > del::text').get())

            attributes = []
            attributes.append({
                'bonho': option_rom,
                'mausac': None,
                'giagoc': option_old_price,
                'giamoi': option_new_price,
                'active': True
            })
            item['thuoctinh'] = attributes
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        item['tskt'] = response.css('div.product-spec-group.mb-4.font-300 > div > table').get()
        item['mota'] = response.css('div.pro-desc-spec-container.bg-white.clearfix > div.item.item-desc').get()
        yield item
