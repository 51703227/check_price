import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))


# Xử lý tên sản phẩm
# Hàm xử lý tên sản phẩm
def name_processing(name):
    black_list = ['Chính', 'hãng', 'I', 'VN/A', 'chính', '|', '-', ]
    bl_list = ['(', ')', '-', '/', '[', ']',
               'Deep Gray', 'Máy Người Già', 'Phiên bản', 'mùa hè', 'Chính Hãng', 'huyền bí', 'Đồng ánh kim',
               'Ánh Kim', 'Đen Than', 'Ánh Sao', 'Màu', 'Chinh', 'Hang', 'Chua', '100', 'Activce', 'Fullbox',
               'Like', '99', 'Te', 'Gia', 'Likenew', 'My', 'Nhan', 'Ban', 'Ngiệm','Chính','hãng',
               'VN/A','\t',
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
               '6.4Inch', 'Đại', 'Điện', 'Di', 'Động','Obox'
               'Đtdđ', 'ĐTDĐ', 'Quoc', 'Moi', 'Ll', '12Gb', 'Cũ',
               '2+32', '.', '100%', 'Lbox', 'Hộp', 'Đã', 'Kích', 'Hoạt', 'Trải', 'Nghiệm',
               'Phép', 'Màu', 'Điện', 'Ảnh', 'Phiên', 'Bản', 'Mới',
               'Nhập', 'Khẩu','Hongkong','Quốc','N','|','Cty','%','Snapdragon','Chip','865+','Nobox',
               '6Gb','12Gb',
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
                'bonho': option_rom,
                'mausac': option_color,
                'giagoc': option_old_price,
                'giamoi': option_new_price,
                'active': active
            })
        item['thuoctinh'] = attributes
        item['tskt'] = tskt
        item['mota'] = mota
        return item