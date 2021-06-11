import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))

# Xử lý tên sản phẩm

# Hàm xử lý tên sản phẩm
def name_processing(name):
    black_list = ['Chính','hãng','I','VN/A','chính','|']
    bl_list = ['(', ')', '-', '/', '[', ']',
               'Deep Gray', 'Máy Người Già', 'Phiên bản', 'mùa hè', 'Chính Hãng', 'huyền bí', 'Đồng ánh kim',
               'Ánh Kim', 'Đen Than', 'Ánh Sao', 'Màu','Chinh', 'Hang','Chua','100','Activce','Fullbox',
               'Like','99','Te','Gia','Likenew','My','Nhan' ,'Ban',
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
               'Cam', 'hà', 'Phong', 'Vân',
               '1 sim', '1 Sim', 'Mỹ', 'New', 'BH12T', 'Certified', 'PreOwned', 'Special', 'Product', 'ram', 'cty',
               'RAM', 'Edge', 'Batman', 'Injustice', 'Cty',
               'Apple', 'APPLE', '6.4Inch', '5.3Inch', '6.4Inch', '6.23Inch', '6.2Inch', '5.7Inch', '6.2Inch',
               '6.4Inch', 'Đại',
               'Đtdđ', 'ĐTDĐ','Quoc','Moi','Ll','12Gb',
               '2+32','.','100%','Lbox'
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

#Xử lý price
def format_price(price):
    _list = ['đ','₫','.',',','VNĐ','VND','\r','\n','\t',' ',' ']
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

# # Lớp crawl dữ liệu didongmy
# class didongmy(scrapy.Spider):
#     name = 'mobile_didongmy'
#     start_urls = ['https://www.didongmy.com/dien-thoai',]
#
#     def parse(self, response):
#         self.log('Visited ' + response.url)
#
#         products = response.css('div.list_product_base > div.product-base-grid')
#
#         self.log('products ' + str(len(products)))
#         for product in products:
#
#             title = name_processing(product.css('div.list_product_base > div > div > h3 > a::text').get()).title()
#             item_link = product.css('div.list_product_base > div > div > h3 > a::attr(href)').get()
#             thuong_hieu = title.split(' ')[0]
#             image1 = ''
#
#             item = {
#                 'ten': title,
#                 'url': item_link,
#                 'image': image1,
#                 'ngay': date.today().strftime("%Y-%m-%d"),
#                 'loaisanpham': 'dienthoai',
#                 'thuonghieu': thuong_hieu
#             }
#             yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)
#
#         # next_page_url = response.css('div.products-cat > div.pagination > a.next-page::attr(href)').extract_first()
#         # next_page_url = response.urljoin(next_page_url)
#         # yield scrapy.Request(url=next_page_url, callback=self.parse)
#
#     def get_detail(self, response):
#         self.log('Visited ' + response.url)
#         item = response.meta['item']
#
#         option_old_price = format_price(response.css('div.col-detail-top2 > form > div > div.prod_dt_price > span.price_old::text').get())
#         option_rom = format_bonho(response.css('#parameter > div.option_focus > ul > li:nth-child(5) > strong::text').get())
#
#         option_color = response.css('ul.color-list-show > li > span::text').get().title()
#         option_new_price = format_price(response.css('div.col-detail-top2 > form > div > div.prod_dt_price > span.price::text').get())
#         active = True
#
#         image2 = response.css('div.fs-dtstd2 > div.easyzoom > a > img::attr(src)').get()
#
#         attributes = []
#         attributes.append({
#             'bonho': option_rom,
#             'mausac': option_color,
#             'giagoc': option_old_price,
#             'giamoi': option_new_price,
#             'active': active
#         })
#
#         item['thuoctinh'] = attributes
#         item['image'] = image2
#         return item


# Lớp crawl dữ liệu mionhducvn
class minhduc_vn(scrapy.Spider):
    name = 'mobile_minhducvn'
    start_urls = ['https://www.minhducvn.com/danh-muc/dien-thoai/', ]

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.products > div.product-small')

        self.log('products ' + str(len(products)))
        for product in products:

            title = name_processing(product.css('div.box-text > div.title-wrapper > p > a::text').get()).title()
            item_link = product.css('div.box-text > div.title-wrapper > p.name > a::attr(href)').get()
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

        next_page_url = response.css('ul.page-numbers > li:nth-child(5) > a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = format_price(response.css('div.price-wrapper > p.price > del > span > bdi::text').get())
        option_rom = format_bonho(response.css('div.product-info > h1.product-title::text').get())

        option_color = None
        option_new_price = format_price(response.css('div.price-wrapper > p.price > ins > span > bdi::text').get())
        active = True

        image2 = response.css('div.woocommerce-product-gallery__image > a > img::attr(src)').get()

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
        return item

#ham xu ly name mobileworld
def mobileworld_name(link):
    temp_name = link.split('/')[2].split('-')
    t = 0
    name = ''
    for i in temp_name:
        if t <= 4:
            name = name + i + ' '
            t = t + 1
    return name.title()

# Lớp crawl dữ liệu mobileworld
class mobile_world(scrapy.Spider):
    name = 'mobile_mobileworld'
    start_urls = ['https://mobileworld.com.vn/collections/dien-thoai', ]

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.collection-body > div.grid-uniform > div.grid__item')

        self.log('products ' + str(len(products)))
        for product in products:

            link__ = product.css('div.product-item-info > div.product-title > a::attr(href)').get()
            item_link = 'https://mobileworld.com.vn/collections/dien-thoai' + link__
            thuong_hieu = link__.split('/')[2].split('-')[0]
            image1 = product.css('div.product-item > div.product-img > a > img::attr(src)').get()
            image = 'https:' + image1

            title = name_processing(mobileworld_name(link__))



            if thuong_hieu=='galaxy':
                thuong_hieu = 'samsung'

            item = {
                'ten': title,
                'url': item_link,
                'image': image,
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'dienthoai',
                'thuonghieu': thuong_hieu
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        next_page_url_1 = 'https://mobileworld.com.vn' + response.css('#pagination- > div > span.nextPage > a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url_1)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = format_price(response.css('div.productInfo > div.grid > div.grid__item > div.pro-price > span::text').get())
        option_rom = format_bonho(response.css('div.productTitle > h1::text').get())

        option_color = response.css('div.n-sd.swatch-element.color.den > label > span::text').get().title()
        option_new_price = option_old_price
        active = True

        attributes = []
        attributes.append({
            'bonho': option_rom,
            'mausac': option_color,
            'giagoc': option_old_price,
            'giamoi': option_new_price,
            'active': active
        })

        item['thuoctinh'] = attributes
        return item

#class crawl data from http://didongsinhvien.com/dien-thoai-dm70.html
class didongsinhvien(scrapy.Spider):
    name = 'didongsinhvien'
    start_urls = ['http://didongsinhvien.com/dien-thoai-dm70.html', ]

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('#ngang_dm > ul > li.box_bc.box_bccu')

        self.log('products ' + str(len(products)))
        for product in products:

            title = name_processing(product.css('div.box_bccu > a.box_bc_name::text').get()).title()
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

        next_page_url = response.css('#vaotrong > div > div.box_main > div:nth-child(5) > ul > div > li:nth-child(11) > a::attr(href)').extract_first()
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
        return item