import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))

# Xử lý tên sản phẩm
# Hàm xử lý tên laptop
list_product_names = ['MacBook',
                      'Pro', 'Air', 'Macbook',
                      'Mac', 'Mini', 'Imac',

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
                      '348', '440',
                      'G7', '14S', 'G8', '15S', '14', '15s', '14s',

                      'Lenovo',
                      'IdeaPad', 'Ideapad', 'Slim', 'Gaming', 'Flex',
                      'Legion', 'V15', 'Yoga', 'Duet',
                      'ThinkBook', 'Thinkbook', 'Carbon', 'Notebook',
                      'ThinkPad', 'Thinkpad', 'Fold', 'NoteBook',
                      '7', '6',
                      'E14', 'E15', 'L14', 'L15',
                      'E13', 'L13', 'X390', 'P15s', '14', 'X390', 'X13',
                      'X12', 'P15v', 'X1', 'TP', 'X1', 'V330',
                      'T14', 'P15', 'P1', 'P17', 'T14S',

                      'Acer', 'ACER',
                      'Spin', 'Predator', 'Helios', 'Nitro', 'Aspire',
                      '3', '5', '7', '3X',
                      'Enduro', 'N3', 'Swift',
                      'One', 'ChromeBook', 'TravelMate', 'Extensa',

                      'Dell',
                      'Latitude', 'Education', 'Rugged', 'Vostro', 'Mobile',
                      'Inspiron', 'Precision', 'XPS', 'Alienware', 'Chromebook',
                      'Workstation', 'Gaming', 'Xps',
                      '13', '15', '11', '14',
                      'M15', 'M17',
                      'G3', 'G5', 'G7', 'M5550', 'M7550', 'N5505',
                      '3000', '5000', '7000', '7306', '5406', '7400',
                      '3410', '9310', '9500', '3401',
                      '3502', '3520', '7320',
                      '5405', '3501', '3593',
                      '3493', '7490', '5391', '5590', '3147',
                      '3148', '3158', '3168', '3162', '3180', '3452',
                      '3467', '3473', '3476', '3552', '3573',
                      '3576', '3583', '3584', '3555', '3541', '5368',
                      '5378', '5379', '5420', '5457', '5490',
                      '5520', '5521', '5537', '5545', 'N5502',
                      '5547', '5548', '5551', '5552', '5555', '5557',
                      '5558', '5559', '5566', '5567', '5570', '5593',
                      '5755', '5758', '5759', '5767', '5775',
                      '7380', '7348', '7353', '7359', '7368', '7375',
                      '7378', '7373', '7386', '7391', '7420', '7520',
                      '7559', '7577', '7570', '7580', '7501', '7558',
                      '7569', '7579', '7573', '7586', '7591', '7737',
                      '7746', '7778', '7786', '7790', '7566', '7567',
                      '7577', 'N3501', 'V5490C', 'V5502A', 'N5391',
                      '3558', '3578', '5370', '5459', '5471', '5481',
                      '5491', '5568', '5581', '5770', '1000', '1200',
                      '1220', '1320', '1500', '1720', 'A90', 'A90n',
                      'V13', '3300', '3400', '3500', '3550', '3560',
                      '3700', '3490', '3590',
                      '5301', '5310', '3400', '3405', '5402', '5410',
                      '5415', '3500', '3510', '5502', '5510', '5515',
                      '7750', '7740', '7730', '7720', '7000', '7710',
                      '7550', '7540', '7530', '7520', '7510', '5750',
                      '5550', '5540', '5530', '5520', '5510', '3560',
                      '3551', '3550', '3541', '3540', '3530', '3520',
                      '3510', 'V3500',
                      'M3800', 'M6800', 'M6700', 'M6600', 'M6500',
                      'M6400', 'M4800', 'M4700', 'M4600', 'M4500', 'M4400',
                      'M2800', 'M2400',

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

# Lớp crawl dữ liệu
class lt_dienmaythienhoa(scrapy.Spider):
    name = 'lt_dienmaythienhoa'
    start_urls = ['https://dienmaythienhoa.vn/laptop-notebook-netbook.html']

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.row.gridnew > div.col-md-4')

        self.log('products ' + str(len(products)))
        for product in products:
            item_link = str(product.css('div.box > a::attr(href)').get())

            proccessed_title = ''
            if item_link:
                temp_ten = item_link.split('/')[3].split('-')[0:9]
                title = ' '.join(temp_ten).title()
                proccessed_title = name_processing(title)

            thuong_hieu = item_link.split('/')[3].split('-')[1]

            item = {
                'ten': proccessed_title,
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