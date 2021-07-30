import scrapy
import os
from datetime import date
from ..productspider import get_attr_from_name,name_processing,format_price,format_bonho,format_mausac

basedir = os.path.dirname(os.path.realpath('__file__'))

# Lớp crawl dữ liệu
class cellphones(scrapy.Spider):
    name = 'cellphones'
    base_url = 'https://cellphones.com.vn/mobile.html?p=%s'
    start_urls = [base_url % 1]

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('.products-container .cols-5 .cate-pro-short')

        self.log('products ' + str(len(products)))
        for product in products:
            title = name_processing(product.css('div.lt-product-group-info > a > h3::text').get()).title()
            item_link = product.css('div.lt-product-group-info > a::attr(href)').get()
            thuong_hieu = item_link.split('/')[3].split('-')[0]

            item = {
                'ten': title,
                'url': item_link,
                'image': product.css('li.cate-pro-short > div.lt-product-group-image > a > img::attr(data-src)').get(),
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'dienthoai',
                'thuonghieu': thuong_hieu
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        [_, i] = response.url.split("=")
        n_child = 2 if int(i) < 2 else 3


        next_page_url = response.css('div.pages > ul:nth-child({}) > li > a::attr(href)'.format(n_child)).extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = format_price(response.css('p.old-price > span::text').get())
        option_rom = response.css('div.linked-products.f-left > div > a.active > span::text').get()

        option_rom_active = response.css('div.linked-products.f-left > div > a.active > span::text').get()
        option_color_active = response.css('ul#configurable_swatch_color > li > a > label > span.opt-name::text').get()

        tskt = response.css('div.lt-table-box.technical-info').get()
        mota = response.css('div.blog-content').get()

        attributes = []
        _attributes = response.css('ul#configurable_swatch_color > li')
        for attribute in _attributes:
            option_color = attribute.css('li > a > label > span.opt-name::text').get().title()
            option_new_price = format_price(attribute.css('a > label > span.opt-price::text').get())

            if option_color == option_color_active and option_rom == option_rom_active:
                active = True
            else:
                active = False

            attributes.append({
                'bonho': format_bonho(option_rom),
                'mausac': format_mausac(option_color),
                'giagoc': option_old_price,
                'giamoi': option_new_price,
                'active': active
            })
        item['thuoctinh'] = attributes
        item['tskt'] = tskt
        item['mota'] = mota
        return item
