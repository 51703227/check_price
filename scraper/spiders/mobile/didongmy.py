import scrapy
import os
from datetime import date
from ..productspider import get_attr_from_name,name_processing,format_price,format_bonho,format_mausac

basedir = os.path.dirname(os.path.realpath('__file__'))


# # Lớp crawl dữ liệu didongmy
class didongmy(scrapy.Spider):
    name = 'didongmy'
    start_urls = ['https://www.didongmy.com/dien-thoai']
    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.list_product_base > div.product-base-grid')

        self.log('products ' + str(len(products)))
        for product in products:

            title = name_processing(product.css('div.boxItem > h3 > a::text').get()).title()
            item_link = product.css('div.boxItem > h3 > a::attr(href)').get()
            thuong_hieu = title.split(' ')[0]



            item = {
                'ten': title,
                'url': item_link,
                'image': '',
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'dienthoai',
                'thuonghieu': thuong_hieu
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        next_page_url = response.css('div.row_base_product.list_product_iphone > div.pagination > a.btnPage::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = format_price(response.css('div.col-detail-top2 > form > div > div.prod_dt_price > span.price_old::text').get())
        option_rom = format_bonho(response.css('#parameter > div.option_focus > ul > li:nth-child(5) > strong::text').get())

        option_color = response.css('ul.color-list-show > li > span::text').get().title()
        option_new_price = format_price(response.css('div.col-detail-top2 > form > div > div.prod_dt_price > span.price::text').get())
        active = True

        image2 = response.css('div.fs-dtstd2 > div.easyzoom > a > img::attr(src)').get()

        attributes = []
        attributes.append({
            'bonho': option_rom,
            'mausac': format_mausac(option_color),
            'giagoc': option_old_price,
            'giamoi': option_new_price,
            'active': active
        })

        item['thuoctinh'] = attributes
        item['image'] = image2
        item['tskt'] = response.css('#parameter').get()
        item['mota'] = response.css('div.col-md-8 > div.box_desc').get()
        return item