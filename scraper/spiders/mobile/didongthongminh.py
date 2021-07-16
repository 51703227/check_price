import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))


# Xử lý tên sản phẩm

# Hàm xử lý tên sản phẩm
def name_processing(name):

    f = open("blacklist.txt", "r", encoding='utf-8')
    lines = f.read().splitlines()

    if name == None:
        return ''
    for character in lines:
        if character in name or character.lower() in name or character.title() in name or character.upper():
            name = name.replace(character,'')
            name = name.replace(character.lower(),'')
            name = name.replace(character.title(),'')
            name = name.replace(character.upper(),'')

    black_list1 = ['Chính', 'hãng', 'I', 'VN/A', 'chính', '|', '-', 'Hãng', 'Cũ', 'Nobox',
                   '1', '1|', 'Chip', 'Snapdragon', '865', '865+', 'Hongkong', 'Fan', 'Edition',
                   'Hộp', 'Trải', 'Nghiệm', 'Đã', 'Kích', 'Phép', 'Hoạt', 'Ng', 'Pin', 'Siêu',
                   'Dùng', 'Siêu', 'Chụp', 'Ảnh', 'Nguyên', 'Nhập', 'Khẩu', 'Màn', 'Hình', '2K',
                   'Nhám', 'Cấu', 'Hiệu', 'Năng', 'Đầy', 'Giá', 'Tiên', 'Máy', 'Thiết', 'Kế',
                   'Tử', 'HàN', 'QuốC', 'Như', 'Vna', 'Điện', 'Thoại', 'Ng', 'Racing', 'Youth',
                   'Zoom', '64', '128', 'Tay', 'Phân', 'Quốc', 'Chống', ]

    unprocess_name = name.split()
    processed_name = []
    for i in unprocess_name:
        if i not in black_list1:
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


# Lớp crawl dữ liệu didongthongminh
class didongthongminh(scrapy.Spider):
    name = 'didongthongminh'
    base_url = 'https://didongthongminh.vn/dien-thoai?q=collections:2586189&page=1&view=grid'
    start_urls = [base_url]

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.category-products> section > div.col-lg-15')

        self.log('products ' + str(len(products)))
        for product in products:
            title11 = product.css('div.evo-product-block-item > a.product__box-name::text').get()
            temp_title1 = title11.split(' ')[0:6]
            temp_title2 = ' '.join(temp_title1).title()
            title = name_processing(temp_title2)

            link__ = product.css('div.evo-product-block-item > a.product__box-name::attr(href)').get()

            item_link = 'https://didongthongminh.vn' + link__
            thuong_hieu = link__.split('/')[1].split('-')[0]

            item = {
                'ten': title,
                'url': item_link,
                'image': '',
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'dienthoai',
                'thuonghieu': thuong_hieu
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        next_page_number = int(response.url.split('page=')[1].split('&')[0]) + 1
        if next_page_number <= 31:
            next_page_url = 'https://didongthongminh.vn/dien-thoai?q=collections:2586189&page={}&view=grid'.format(
                next_page_number)

            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited main ' + response.url)
        item = response.meta['item']

        option_old_price = format_price(response.css('div.price-box.clearfix > span.old-price > del::text').get())
        option_rom = format_bonho(response.css('div.col-lg-12 > h1::text').get())

        option_color = ''
        if response.css('div.swatch-element > div::text').get():
            option_color = response.css('div.swatch-element > div::text').get().title()

        option_new_price = response.css('div.price-box.clearfix > span.special-price > span::text').get()
        active = True

        image1 = response.css('div.swiper-wrapper > a.swiper-slide > img::attr(data-src)').get()

        attributes = []
        attributes.append({
            'bonho': option_rom,
            'mausac': option_color,
            'giagoc': option_old_price,
            'giamoi': option_new_price,
            'active': active
        })

        item['image'] = image1
        item['thuoctinh'] = attributes
        item['tskt'] = response.css('div.col-lg-5 > div.shadow-sm').get()
        item['mota'] = response.css('div.evo-product-review-content').get()
        return item