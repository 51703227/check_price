import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))


# Xử lý tên sản phẩm

# Hàm xử lý tên sản phẩm
def name_processing(name):

    bl_list = ['(', ')', '-', '–', '/', '[', ']', ',',
               'Điện thoại',
               '+512GB', '+256GB', '+128GB', '+64GB', '+8GB', '+16GB', '+32GB', '+4GB', '+512Gb', '+256Gb', '+128Gb',
               '+64Gb', '+8Gb', '+16Gb', '+32Gb', '+4Gb',
               '512GB', '256GB', '128GB', '64GB', '8GB', '16GB', '32GB', '4GB', '512Gb', '256Gb', '128Gb', '64Gb',
               '8Gb', '16Gb', '32Gb', '4Gb',
               '512 GB', '256 GB', '128 GB', '64 GB', '8 GB', '16 GB', '32 GB', '4 GB', '+512G', '+256G', '+128G',
               '+64G', '+16G', '+32G',
               '512gb', '256gb', '128gb', '64gb', '8gb', '16gb', '32gb', '6gb', '4gb', '512G', '256G', '128G', '64G',
               '16G', '32G', '2GB', '3GB', '512g', '256g', '128g', '64g', '8g', '16g', '32g', '4g', '6g', '3g', '5g',
               'Xanh đại dương', 'đại dương', 'ánh sao', 'hoàng hôn', 'Xanh lá', 'Vàng đồng', 'nước biển',
               'Vàng đồng', 'lá', 'lục', 'Đồng', 'Khói', 'bích', 'huyền bí', 'nhật thực', 'Biển', 'mận', 'Dương',
               'Lá', 'Đỏ', 'Đen', 'Lục', 'Cực', 'Quang', 'tinh', 'thạch', 'Ngọc', 'Trai', 'Bạc', 'Hà', 'Lam', 'Thủy',
               'Triều', 'Đồng', 'Vàng', 'Xanh', 'Đen', 'Trắng', 'Thạch', 'Anh', 'lá', 'ngọc', 'lam', 'Sapphire',
               'Pink', 'Deep Gray', 'Deep', 'Mint', 'Yellow', 'Champagne', 'Grey', 'Black', 'Gold', 'Graphite',
               'Silver', 'Blue', 'Tím', 'Green', 'Sliver', 'Trắng', 'Xám', 'Pacific', 'Blue', 'White', 'Gray',
               'Violet', 'Purple', 'Red', 'Browns',
               '8Th', '10.2', 'Wifi', 'Gld Mylf2Zaa', 'Di động', 'Bút', 'Màu',
               'Ss 2019', 'Ds 2020  3', "  ", "   ", "    ", "     ", "      ",
               ]

    if name == None:
        return ''
    for character in bl_list:
            name = name.replace(character, '')
            name = name.replace(character.lower(), '')
            name = name.replace(character.title(), '')
            name = name.replace(character.upper(), '')

    return name


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
