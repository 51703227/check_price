import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))

# Xử lý dữ liệu
# Hàm xử lý tên sản phẩm
def name_processing(name):
    list_product_names = ['chính hãng', 'Chính hãng']

    unprocess_name = name.title().split()
    processed_name = []
    for i in unprocess_name:
        if i in list_product_names:
            processed_name.append(i)
    return ' '.join(processed_name)

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

#class crawl data from www.anphatpc.com.vn
class lt_anphatpc(scrapy.Spider):
    name = 'lt_anphatpc'
    start_urls = ['https://www.anphatpc.com.vn/may-tinh-xach-tay-laptop.html']

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
            thuonghieu = item_link.split('/')[3].split('-')[1]

            item = {
                'ten': title,
                'url': item_link,
                'image': image,
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'laptop',
                'thuonghieu': thuonghieu
            }

            option_new_price = format_price(product.css('div.price-container > span.p-price::text').get())
            option_old_price = format_price(product.css('div.price-container > del::text').get())

            attributes = []
            attributes.append({
                'giagoc': option_old_price,
                'giamoi': option_new_price,
            })
            item['thuoctinh'] = attributes
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        next_page_url = 'https://www.anphatpc.com.vn' + str(response.css('div.paging > a:nth-child(8)::attr(href)').extract_first())
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        item['tskt'] = response.css('div.item-content.position-relative > table').get()
        item['mota'] = response.css('div.item.item-desc').get()
        yield item