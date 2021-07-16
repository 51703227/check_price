import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))

# Xử lý tên sản phẩm
# Danh sách các từ cần loại bỏ
def name_processing(name):
    bl_list = ['(', ')', '-', '–', '/', '[', ']', ',',
               'camera kép', 'camera', 'còn bảo hành', 'Single Sim', 'Không Có Google', 'Pin 100%', 'qt',
               'bảo hành chính hãng', 'quốc tế mới 100%', 'mới 100%', 'nguyên seal', 'chưa active', 'Quốc tế', '95%',
               'QT', '100%', 'Chưa Active', '2017', 'Sạc Ít Lần', 'Fullbox', 'Phiên',
               'Bản', 'Mới 100%', 'Quốc Tế', 'Hàn Quốc', 'Bản Hàn Quốc', 'tím', 'màu', 'Đẹp', 'đẹp', 'Deep Gray',
               'Máy Người Già', 'Máy người già', 'Mùa Xuân',
               'mùa hè', 'huyền bí', 'Đồng ánh kim', 'Ánh Kim', 'Đen Than', 'Ánh Sao', 'Thiên',
               'Màu', 'Mới', 'mới', 'Rom',
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
               'bảo hành', 'độc', 'đáo', 'hạt', 'tiêu', '(KHÔNG KÈM THẺ NHỚ)', 'Thoại', '2019', '2020', '2018', '2017',
               'Bộ 3 Camera', 'Bộ 4 Camera Sau 48Mp', 'Siêu Màn Hình', 'Màn Hình Giọt Nước', 'Sạc Nhanh',
               '6.67Inch', '6.5Inch', '6.9Inch', '2 sim', '6.1Inch', '2 Sim', 'VNA', 'hải', 'quân', 'san hô', 'trai',
               'dương', 'cẩm', 'KHÔNG KÈM THẺ NHỚ', 'San Hô', 'Nhật Thực', 'Sương Mai', 'Đam Mê', 'lục', 'bảo', 'Bảo',
               'sương', 'hồng', 'Bích', 'tú', 'thủy', 'Hải', 'Âu', 'Hồng', 'pha', 'lê', 'quang', 'cực', 'Cam', 'hà',
               'Phong', 'Vân',
               '1 sim', '1 Sim', 'Mỹ', 'New', 'BH12T', 'Certified', 'PreOwned', 'Special', 'Product', 'ram', 'cty',
               'RAM', 'Edge', 'Batman', 'Injustice', 'Cty',
               'Apple', 'APPLE', '6.4Inch', '5.3Inch', '6.4Inch', '6.23Inch', '6.2Inch', '5.7Inch', '6.2Inch',
               '6.4Inch', 'Đại', 'like',
               'Đtdđ', 'ĐTDĐ', '8+128', '6 + 128',
               '2+32', '9798%', '98%', '97%', '99%', '95%', 'Camera Sau', 'Active | Pin 4000Ma, Chip Snap 835',
               'Pin 5000Mah', 'Pin 5000 Mah', 'Không Có Google', 'Fan Edition', 'Siêu Lướt', 'Đã Kích Hoạt',
               ' \t', '\t', '\r', '\n', 'Chính Hãng', '  ', 'chính Hãng', 'Chính hãng', 'chính hãng',
               'Cũ', 'Ato', 'Dgw', 'Như', 'Nh 12 Tháng 1 Đổi 1', 'Lte', 'Lla',
               '   ',
               ]

    if name == None:
        return ''
    for character in bl_list:
        name = name.replace(character, '')
        name = name.replace(character.lower(), '')
        name = name.replace(character.title(), '')
        name = name.replace(character.upper(), '')

    black_list1 = ['Siêu', 'Lướt', 'siêu', 'lướt', 'Xlnoboxtbh', 'V405Qa7', '101', 'V409N',
                   'xlnoboxtbh', 'v405Qa7', '101', 'v409N', 'nobox', 'tbh',
                   'Nobox', 'Tbh', 'V405', 'Qa7']

    unprocess_name = name.split()
    processed_name = []
    for i in unprocess_name:
        if i not in black_list1:
            processed_name.append(i)
    return ' '.join(processed_name).title()

#Xử lý price
def format_price(price):
    _list = ['đ','₫','.',',','VNĐ','VND','\r','\n','\t',' ']
    if not price:
        return None
    else:
        for i in _list:
            price = price.replace(i,'')
    return price

#Xử lý bộ nhớ
def format_bonho(name):
    attr_bonho = 'None'
    list_attr_bonho = ['512GB', '256GB', '128GB', '64GB', '16GB', '32GB', '512Gb', '256Gb', '128Gb', '64Gb', '16Gb',
                       '32Gb']

    for i in list_attr_bonho:
        if i in name:
            attr_bonho = i
    return attr_bonho

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
            'bonho': option_rom,
            'mausac': option_color,
            'giagoc': option_old_price,
            'giamoi': option_new_price,
            'active': active
        })

        item['thuoctinh'] = attributes
        item['tskt'] = response.css('div.option_focus').get()
        item['mota'] = response.css('#danh-gia').get()

        return item
