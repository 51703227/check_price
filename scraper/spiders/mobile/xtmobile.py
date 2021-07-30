import scrapy
import os
from datetime import date
from ..productspider import get_attr_from_name,name_processing,format_price,format_bonho,format_mausac

basedir = os.path.dirname(os.path.realpath('__file__'))

#crawl xtmobile website
class xtmobile_spider(scrapy.Spider):
    name = 'xttmobile'
    start_urls = ['https://www.xtmobile.vn/dien-thoai', ]

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.col-main-base-product > div.list_product_base > div.product-base-grid')

        self.log('products ' + str(len(products)))
        for product in products:

            title1 = name_processing(product.css('div.boxItem > div.pinfo > h3 > a::text').get())
            title = title1.split('|')[0]

            item_link = product.css('div.boxItem > div.pic > a::attr(href)').get()
            thuong_hieu = item_link.split('/')[3].split('-')[0]
            image1 = product.css('div.boxItem > div.pic a > img::attr(src)').get()

            item = {
                'ten': title,
                'url': item_link,
                'image': image1,
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'dienthoai',
                'thuonghieu': thuong_hieu
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)


        next_page_url = response.css('div.pagination-more > form > a.data-url::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = response.css('form#form_order > div.product-color > ul.color-list-show > li > b::text').get()
        option_rom = response.css('#parameter > div.option_focus > ul > li:nth-child(6) > strong::text').get()

        option_color = response.css('form#form_order > div.product-color > ul.color-list-show > li > p::text').get()
        option_new_price = option_old_price
        active = True

        # image2 = response.css('div.frame_img > div > div.magic_zoom_area > a::attr(href)').get()

        attributes = []

        attributes.append({
            'bonho': format_bonho(option_rom),
            'mausac': format_mausac(option_color),
            'giagoc': format_price(option_old_price),
            'giamoi': format_price(option_new_price),
            'active': active
        })

        item['thuoctinh'] = attributes
        item['tskt'] = response.css('div.option_focus').get()
        item['mota'] = response.css('#danh-gia').get()

        return item
