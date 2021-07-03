import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))

# Xử lý tên sản phẩm
# Danh sách các từ cần loại bỏ
black_list = ['(2020)', '13inch', '(16GB|512GB)', '(16GB|256GB)' ,'(8GB|512GB)','(8GB|256GB)']

# Hàm xử lý tên sản phẩm
def name_processing(name):
  unprocess_name = name.split()
  processed_name = []
  for i in unprocess_name:
    if i not in black_list:
      processed_name.append(i)
  return ' '.join(processed_name)

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
class lt_xttmobile(scrapy.Spider):
    name = 'lt_xttmobile'
    start_urls = ['https://www.xtmobile.vn/macbook', ]

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.list_product_base > div.product-base-grid')

        self.log('products ' + str(len(products)))
        for product in products:

            title = name_processing(product.css('div.boxItem > div.pinfo > h3 > a::text').get())
            item_link = product.css('div.boxItem > div.pic > a::attr(href)').get()
            image = product.css('div.boxItem > div.pic a > img::attr(src)').get()

            item = {
                'ten': title,
                'url': item_link,
                'image': image,
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'laptop',
                'thuonghieu': 'macbook'
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        next_page_url = response.css('div.pagination-more > form > a.data-url::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = response.css('form#form_order > div.product-color > ul.color-list-show > li > b::text').get()
        option_new_price = response.css('div.prod_dt_price > span.price_old > del::text').get()

        attributes = []

        attributes.append({
            'giagoc': option_old_price,
            'giamoi': option_new_price,
        })
        item['thuoctinh'] = attributes
        item['tskt'] = response.css('div.option_focus').get()
        item['mota'] = response.css('#danh-gia').get()

        return item