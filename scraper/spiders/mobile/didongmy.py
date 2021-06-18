import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))


# Xử lý tên sản phẩm

# Hàm xử lý tên sản phẩm
def name_processing(name):
    black_list = ['Chính', 'hãng', 'I', 'VN/A', 'chính', '|', '-', ]
    bl_list = ['(', ')', '-', '/', '[', ']',
               'Cty','12Gb|512Gb','Hongkong','Sim','Bản','Mỹ','New','Fullbox',
               'Chip','Snapdragon','Hàn','Quốc','Cũ','99%','12Gb128Gb','12Gb256Gb','12Gb|256Gb',
               '8Gb|256Gb','Nobox','New','6Gb128Gb','8Gb|128Gb','6Gb|128Gb','865',
               '12Gb256Gb','12Gb512Gb','12Gb|128Gb','12Gb|',
               'Cty','12Gb','97%','6Gb'
               '+512GB', '+256GB', '+128GB', '+64GB', '+8GB', '+16GB', '+32GB', '+4GB', '+512Gb', '+256Gb', '+128Gb',
               '+64Gb', '+8Gb', '+16Gb', '+32Gb', '+4Gb', '+512G', '+256G', '+128G', '+64G', '+16G', '+32G',
               '512GB', '256GB', '128GB', '64GB', '8GB', '16GB', '32GB', '4GB', '512Gb', '256Gb', '128Gb', '64Gb',
               '8Gb', '16Gb', '32Gb', '4Gb', '512G', '256G', '128G', '64G', '16G', '32G',
               ]

    if name == None:
        return ''
    for character in bl_list:
        name = name.replace(character, '')

    unprocess_name = name.split()
    processed_name = []
    for i in unprocess_name:
        if i not in black_list:
            processed_name.append(i)
    return ' '.join(processed_name).title()


# Xử lý price
def format_price(price):
    _list = ['đ', '₫', '.', ',', 'VNĐ', 'VND', '\r', '\n', '\t', ' ', ' ']
    if not price:
        return None
    else:
        for i in _list:
            price = price.replace(i, '')
    return price


# Xử lý bộ nhớ
def format_bonho(name):
    attr_bonho = 'None'
    list_attr_bonho = ['512GB', '256GB', '128GB', '64GB', '16GB', '32GB', '512Gb', '256Gb', '128Gb', '64Gb', '16Gb',
                       '32Gb']

    for i in list_attr_bonho:
        if i in name:
            attr_bonho = i
    return attr_bonho

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
            'mausac': option_color,
            'giagoc': option_old_price,
            'giamoi': option_new_price,
            'active': active
        })

        item['thuoctinh'] = attributes
        item['image'] = image2
        item['tskt'] = response.css('#parameter').get()
        item['mota'] = response.css('div.col-md-8 > div.box_desc').get()
        return item