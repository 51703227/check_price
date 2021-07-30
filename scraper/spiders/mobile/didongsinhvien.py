import scrapy
import os
from datetime import date
from ..productspider import get_attr_from_name,name_processing,format_price,format_bonho,format_mausac

basedir = os.path.dirname(os.path.realpath('__file__'))


# class crawl data from didongsinhvien.com
class didongsinhvien(scrapy.Spider):
    name = 'didongsinhvien'
    start_urls = ['http://didongsinhvien.com/dien-thoai-dm70.html', ]

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('#ngang_dm > ul > li.box_bc.box_bccu')

        self.log('products ' + str(len(products)))
        for product in products:
            title = name_processing(product.css('div.box_bccu > a.box_bc_name::text').get())
            item_link = product.css('div.box_bccu > a.box_bc_name::attr(href)').get()
            thuong_hieu = item_link.split('/')[3].split('-')[0]
            image1 = ''

            item = {
                'ten': title,
                'url': item_link,
                'image': image1,
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'dienthoai',
                'thuonghieu': thuong_hieu
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        next_page_url = response.css(
            '#vaotrong > div > div.box_main > div:nth-child(5) > ul > div > li:nth-child(11) > a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = format_price(response.css('#ndct > div.block_gia > p::text').get())
        option_rom = None
        option_color = None
        option_new_price = option_old_price
        active = True

        image2 = 'http://didongsinhvien.com/' + response.css('#img_ct > img::attr(src)').get()

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
        item['tskt'] = response.css('#bvt').get()
        item['mota'] = ''
        return item