import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))


# Xử lý tên sản phẩm

# Hàm xử lý tên sản phẩm
def name_processing(name):
    black_list = ['Chính', 'hãng', 'I', 'VN/A', 'chính', '|', '-', ]
    bl_list = ['(', ')', '-', '/', '[', ']',
               'Điện','Thoại','Di','Động','128Gb', 'Pacific','Blue','Mgda3Vn/A','Chính','Hãng',
                '256Gb','Gold','Mgmr3Vn/A','512Gb','Gold', 'Silver','Graphite',
                'Thoại','Di','Động','Mgmr3','Mgd73','Mgmq3',''
               '+512GB', '+256GB', '+128GB', '+64GB', '+8GB', '+16GB', '+32GB', '+4GB', '+512Gb', '+256Gb', '+128Gb',
               '+64Gb', '+8Gb', '+16Gb', '+32Gb', '+4Gb', '+512G', '+256G', '+128G', '+64G', '+16G', '+32G',
               '512GB', '256GB', '128GB', '64GB', '8GB', '16GB', '32GB', '4GB', '512Gb', '256Gb', '128Gb', '64Gb',
               '8Gb', '16Gb', '32Gb', '4Gb', '512G', '256G', '128G', '64G', '16G', '32G',
               'Xanh lá', 'Vàng đồng', 'nước biển', 'Vàng đồng', 'lá', 'lục', 'Đồng', 'Khói', 'bích', 'huyền bí',
               'nhật thực', 'Biển', 'mận', 'Dương', 'Lá', 'Đỏ', 'Đen', 'Lục', 'Cực', 'Quang', 'tinh', 'thạch', 'Ngọc',
               'Trai', 'Bạc', 'Hà', 'Lam', 'Thủy', 'Triều', 'Đồng', 'Vàng', 'Xanh', 'Đen', 'Trắng', 'Thạch', 'Anh',
               'lá', 'ngọc', 'lam', 'Sapphire',
               'Deep Gray', 'Deep', 'Mint', 'Yellow', 'Champagne', 'Grey', 'Black', 'Gold', 'Graphite', 'Silver',
               'Blue', 'Tím', 'Green', 'Sliver', 'Trắng', 'Xám', 'Pacific', 'Blue', 'White', 'Gray', 'Violet',
               'Purple', 'Red', 'Browns',
               'độc', 'đáo', 'hạt', 'tiêu', '(KHÔNG KÈM THẺ NHỚ)', 'Thoại', '2019', '2020',
               '6.67Inch', '6.5Inch', '6.9Inch', '2 sim', '6.1Inch', '2 Sim', 'VNA', 'hải', 'quân', 'san', 'hô', 'trai',
               'dương', 'cẩm', 'KHÔNG KÈM THẺ NHỚ', 'San', 'Hô', 'Nhật', 'Thực', 'Sương', 'Mai', 'Đam', 'Mê', 'lục',
               'bảo', 'Bảo', 'sương', 'hồng', 'Bích', 'tú', 'thủy', 'Hải', 'Âu', 'Hồng', 'pha', 'lê', 'quang', 'cực',
               'Cam', 'hà', 'Phong', 'Vân', 'Màu', 'Điện', 'Ảnh',
               '1 sim', '1 Sim', 'Mỹ', 'New', 'BH12T', 'Certified', 'PreOwned', 'Special', 'Product', 'ram', 'cty',
               'RAM', 'Edge', 'Batman', 'Injustice', 'Cty',
               'Apple', 'APPLE', '6.4Inch', '5.3Inch', '6.4Inch', '6.23Inch', '6.2Inch', '5.7Inch', '6.2Inch',
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