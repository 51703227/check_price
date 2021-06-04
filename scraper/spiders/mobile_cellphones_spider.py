import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))

# Xử lý tên sản phẩm
# Danh sách các từ cần loại bỏ
black_list = ['Chính', 'hãng', 'I', 'VN/A', 'chính']

# Hàm xử lý tên sản phẩm
def name_processing(name):
  unprocess_name = name.split()
  processed_name = []
  for i in unprocess_name:
    if i not in black_list:
      processed_name.append(i)
  return ' '.join(processed_name)


# Lớp crawl dữ liệu
class CellPhonesSpider(scrapy.Spider):
    name = 'mobile_cellphones'
    base_url = 'https://cellphones.com.vn/mobile.html?p=%s'
    start_urls = [base_url % 1]
    download_delay = 5

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('.products-container .cols-5 .cate-pro-short')

        self.log('products ' + str(len(products)))
        for product in products:

            title = name_processing(product.css('a > #product_link::text').get())
            item_link = product.css('li.cate-pro-short > div.lt-product-group-image > a::attr(href)').get()
            thuong_hieu = item_link.split('/')[3].split('-')[0]

            item = {
                'ten': title,
                'url': item_link,
                'image': product.css('li.cate-pro-short > div.lt-product-group-image > a > img::attr(data-src)').get(),
                'ngay': date.today().strftime("%d/%m/%Y"),
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

        option_old_price = response.css('p.old-price > span::text').get()
        option_rom = response.css('div.linked-products.f-left > div > a.active > span::text').get()

        attributes = []
        _attributes = response.css('ul#configurable_swatch_color > li')

        for attribute in _attributes:
            option_color = attribute.css('li > a > label > span.opt-name::text').get()
            option_new_price = attribute.css('a > label > span.opt-price::text').get()

            attributes.append({
                'bonho': option_rom,
                'mausac': option_color,
                'giagoc': option_old_price,
                'giamoi': option_new_price
            })
        item['thuoctinh'] = attributes

        return item

# câu lệnh chạy
#scrapy crawl mobile_cellphones -o mobile_cellphones_data.json