import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))

# Xử lý tên sản phẩm
# Hàm xử lý tên sản phẩm
def name_processing(name):
    black_list = ['Chính', 'hãng', 'I', 'VN/A', 'chính', '|', '-', ]
    bl_list = ['(', ')', '-', '/', '[', ']',
               ' Chính hãng', ' Chính Hãng', ' Việt Nam', 'Apple', ' chính hãng',' chính Hãng', 'Laptop',
               '+512GB', '+256GB', '+128GB', '+64GB', '+8GB', '+16GB', '+32GB', '+4GB', '+512Gb', '+256Gb', '+128Gb',
               '+64Gb', '+8Gb', '+16Gb', '+32Gb', '+4Gb', '+512G', '+256G', '+128G', '+64G', '+16G', '+32G',
               '512GB', '256GB', '128GB', '64GB', '8GB', '16GB', '32GB', '4GB', '512Gb', '256Gb', '128Gb', '64Gb',
               '8Gb', '16Gb', '32Gb', '4Gb', '512G', '256G', '128G', '64G', '16G', '32G',
               '512 Gb', '256 Gb', '128 Gb', '64 Gb',
               '2015', '2016', '2017', '2018', '2019', '2020',
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

# Lớp crawl dữ liệu
class lt_dienmaythienhoa(scrapy.Spider):
    name = 'lt_dienmaythienhoa'
    start_urls = ['https://dienmaythienhoa.vn/laptop-notebook-netbook.html']

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.row.gridnew > div.col-md-4')

        self.log('products ' + str(len(products)))
        for product in products:
            title = name_processing(product.css('div.content > p::text').get()).title()
            item_link = str(product.css('div.box > a::attr(href)').get())

            thuong_hieu = item_link.split('/')[3].split('-')[1]

            item = {
                'ten': title,
                'url': item_link,
                'image': product.css('div.box > a > img.lazy::attr(data-src)').get(),
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'laptop',
                'thuonghieu': thuong_hieu
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        next_page_url = response.css('div.right > div.text > a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = format_price(response.css('div.online-sale-price > p:nth-child(3) > del > span::text').get())
        option_new_price = format_price(response.css('div.online-sale-price > p:nth-child(2) > span.price-real.color::text').get())

        tskt = response.css('#information-product').get()
        mota = response.css('#content_block_description').get()

        attributes = []
        attributes.append({
            'giagoc': option_old_price[:-2],
            'giamoi': option_new_price[:-2],
        })
        item['thuoctinh'] = attributes
        item['tskt'] = tskt
        item['mota'] = mota
        return item