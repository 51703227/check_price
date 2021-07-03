import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))


# Xử lý tên sản phẩm
# Hàm xử lý tên laptop
list_product_names = ['MacBook',
                      'Pro', 'Air', 'Macbook',
                      'Mac', 'Mini', 'Imac', '24',

                      'Asus', 'ASUS',
                      'ProArt', 'StudioBook', 'Pro', 'X', 'One',
                      'ROG', 'Zephyrus', 'Strix', 'Flow', 'X13', 'Scar',
                      'TUF', 'Gaming', 'ExpertBook', 'Premium', 'Transformer',
                      'Tuf', 'Rog', 'Dash',
                      '17', '15',
                      'ZenBook', 'Pro', 'S', 'Flip', 'Duo',
                      'VivoBook', 'Pro', 'S', 'Flip', 'Vivobook',
                      'Zenbook', 'Studiobook', 'Expertbook',
                      'ChromeBook', 'Detachable',
                      'A17', 'G17', 'S14', 'S15', 'G14', 'F15',
                      'M415', 'M515', 'X415', 'X515', 'BR1100C',
                      'BR1100F', 'E510', 'M570', 'E210', 'E410',
                      'X509', 'M509', 'X545', 'X409', 'M409', 'X507',
                      'X407', 'E402', 'W202', 'X540', 'X543', 'X541',
                      'Mini', 'T102', 'E203', 'E200',
                      'E202', 'E403', 'X441', 'X555', 'X556', 'Book',
                      'T101', 'X751', 'X570', 'T103', 'X756', 'X401',


                      'HP', 'Hp',
                      'Spectre', 'Chromebook', 'ENVY',
                      '13', '15', '17', '14S'
                      'Pavilion', 'Clamshell', 'Folio', 'OMEN', 'Gaming',
                      'Envy', 'Elite', 'EliteBook', 'Elitebook', 'ProBook',
                      'Probook', 'Omen', 'Convertible', 'Studio',
                      'Pavilion',
                      'Zbook', 'ZBook', 'Firefly', 'Fury', 'Power',
                      '340S', 'X360', '430', '240', '450', '245',
                      '348',
                      'G7', '14S', 'G8', '15S', '14', '15s', '14s',

                      'Lenovo',
                      'IdeaPad', 'Ideapad', 'Slim', 'Gaming', 'Flex',
                      'Legion', 'V15', 'Yoga', 'Duet',
                      'ThinkBook', 'Thinkbook', 'Carbon', 'Notebook',
                      'ThinkPad', 'Thinkpad', 'Fold', 'NoteBook',
                      '7', '6',
                      'E14', 'E15', 'L14', 'L15',
                      'E13', 'L13', 'X390', 'P15s', '14', 'X390', 'X13',
                      'X12', 'P15v', 'X1', 'TP', 'X1',
                      'T14', 'P15', 'P1', 'P17', 'T14S',

                      'Acer', 'ACER',
                      'Spin', 'Predator', 'Helios', 'Nitro', 'Aspire',
                      '3', '5', '7', '3X',
                      'Enduro', 'N3', 'Swift',
                      'One', 'ChromeBook', 'TravelMate', 'Extensa',

                      'Dell',
                      'Latitude', 'Education', 'Rugged', 'Vostro', 'Mobile',
                      'Inspiron', 'Precision', 'XPS', 'Alienware', 'Chromebook',
                      'Workstation', 'Gaming',
                      '13', '15', '11', '14',
                      'M15', 'M17',
                      'G3', 'G5', 'G7', 'M5550', 'M7550', 'N5505',
                      '3000', '5000', '7000', '7306', '5406', '7400',
                      '3410', '5301', '9310', '3510', '9500', '3401',
                      '3502', '5520', '5420', '3520', '7320', '5520',
                      '7420', '5502', '5405', '3501', '5502', '3593',
                      '3493', '7490', '5402',

                      'LG', 'Lg',
                      'Gram', 'Thin', 'Ultra', 'PC',
                      '14', '16',

                      'MSI', 'Msi',
                      'Katana', 'Gaming', 'leopard', 'Titan', 'Stealth', 'Raider',
                      'Dragon', 'Edition', 'Tiamat', 'Leopard', 'Pulse', 'Crosshair',
                      'Sword', 'Thin', 'Alpha', 'Bravo', 'Modern', 'Prestige',
                      'Creator', 'EVO', 'Evo',
                      '17', '15', '14',
                      'GF65', 'GF63', 'GL65', 'GF66', 'GT76', 'GS76',
                      'GS66', '15M', 'GS75', 'GE76', 'GE66', 'GE75',
                      'GP76', 'GP66', 'GP75', 'GP65', 'GL76', 'GL66',
                      'GL75', 'GL65', 'GF76', 'GF66', 'GF75', 'GF65', 'GF63',
                      'Gf65', 'Gf63', 'Gl65', 'Gf66', 'Gt76', 'Gs76', 'Gs66', 'Gs75',
                      'Ge76', 'Ge75', 'Gp76', 'Gp66', 'Gp75', 'Gp65', 'Gl76', 'Gl66',
                      'Gl75', 'Gl65', 'Gf76', 'Gf66', 'Gf75', 'Gf65', 'Gf63',

                      'Gigabyte', 'GIGABYTE',
                      'Aorus', 'Aero',
                      '15P', '15',
                      'G5', 'KC', 'Kc', 'G7',

                      'Fujitsu', 'FUJITSU',
                      'LifeBook', 'Lifebook',
                      'U9311',

                      'Microsoft', 'MICROSOFT',
                      'Surface', 'Pro', 'X', 'Go',
                      '7',

                      'Huawei',
                      'MateBook', 'Matebook',
                      '13',

                      'Avita',
                      'Liber', 'V14',

                      'Ipad',
                      'Pro', '11', '12.9',

                      'VGS', 'Vgs',
                      'Imperium',
                      ]


def name_processing(name):
    unprocess_name = name.title()
    processed_name = []
    for i in unprocess_name.split(" "):
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



# crawl data from aeoneshop.com
class lt_aeoneshop(scrapy.Spider):
    name = 'lt_aeoneshop'
    start_urls = ['https://aeoneshop.com/collections/laptop-may-tinh-bang']

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.product-list > div.col-sm-6')

        self.log('products ' + str(len(products)))
        for product in products:
            title = name_processing(product.css('div.box-pro-detail > h3.pro-name > a::text').get()).title()
            item_link = 'https://aeoneshop.com' + str(
                product.css('div.box-pro-detail > h3.pro-name > a::attr(href)').get())

            thuong_hieu = ''
            if item_link:
                thuong_hieu = item_link.split('/')[6].split('-')[1]


            item = {
                'ten': title,
                'url': item_link,
                'image': '',
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'dienthoai',
                'thuonghieu': thuong_hieu
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        next_page_url = 'https://aeoneshop.com' + str(response.css('#pagination > div.col-lg-2.col-md-2.col-sm-3.hidden-xs.controlArrow.text-right > a::attr(href)').extract_first())
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = format_price(response.css('span.price_min > span.priceMin.price::text').get())
        option_new_price = format_price(response.css('div.pro-price > span.priceMin::text').get())

        image2 = 'https:' + response.css('div.col-xs-12.col-sm-4 > div > div.main-detail-product > img::attr(src)').get()

        attributes = []
        attributes.append({
            'giagoc': option_old_price,
            'giamoi': option_new_price,
        })
        item['thuoctinh'] = attributes
        item['image'] = image2
        item['tskt'] = response.css('div.tabContent').get()
        item['mota'] = ''
        return item