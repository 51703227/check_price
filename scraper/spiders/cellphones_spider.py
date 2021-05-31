import scrapy
import os
#import pandas as pd
#import numpy as np
import re
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))


class CellPhonesSpider(scrapy.Spider):
    name = 'cellphones'
    base_url = 'https://cellphones.com.vn/mobile.html?p=%s'
    start_urls = [base_url % 1]
    download_delay = 5

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('.products-container .cols-5 .cate-pro-short')

        self.log('products ' + str(len(products)))
        for product in products:
            title = self.name_processing(product.css('a > #product_link::text').get())
            item = {
                'ten': title,
                'url': response.url,
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

            yield item

        #
        #
        # next_page_url = response.css('div.row.searchPagination > div > nav > ul > li:nth-child(2) a::attr(href)').extract_first()
        # next_page_url = response.urljoin(next_page_url)
        # yield scrapy.Request(url=next_page_url, callback=self.parse)

    def name_processing(self, name_pd):
        pattern = r'([^Chính hãng,chính hãng,VN/A,Điện thoại,điện thoại,|])\w+'
        print(name_pd)

        matches = re.finditer(pattern, name_pd)
        name_pd = [x.group() for x in matches]
        name_pd = list(map(lambda p : '\t'.join(p.split('/')), name_pd))

        return ' '.join(name_pd)
