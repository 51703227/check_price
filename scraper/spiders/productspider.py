import scrapy
from datetime import date
import os

class cellphonetSpider(scrapy.Spider):
    name = 'cellphone'
    start_urls = ['https://cellphones.com.vn/mobile.html']

    def parse(self,response):
        for product in response.css('li.cate-pro-short'):
            try:
                yield{
                    'ten' : product.css('h3::text').get().replace('\t',''),
                    'giamoi' : product.css('.special-price span::text').get().replace('\xa0₫',''),
                    'giagoc' : product.css('.old-price span::text').get().replace('\xa0₫',''),
                    'url' : product.css('.lt-product-group-info a').attrib['href'],
                    'img' : product.css('.lt-product-group-image img').attrib['data-src'],
                    'ngay': product.css('.lt-product-group-image img').attrib['data-src'],
                    'loaisanpham':product.css('.lt-product-group-image img').attrib['data-src'],
                    'thuonghieu':product.css('.lt-product-group-image img').attrib['data-src'],
                    'mausac':product.css('.lt-product-group-image img').attrib['data-src'],
                    'bonho':product.css('.lt-product-group-image img').attrib['data-src'],

                }
            except:
                yield{
                    'ten' : product.css('h3::text').get().replace('\t',''),
                    'giamoi' : 0,
                    'giagoc' : 0,
                    'url' : product.css('.lt-product-group-info a').attrib['href'],
                    'img' : product.css('.lt-product-group-image img').attrib['data-src'],
                    'ngay': product.css('.lt-product-group-image img').attrib['data-src'],
                    'loaisanpham':product.css('.lt-product-group-image img').attrib['data-src'],
                    'thuonghieu':product.css('.lt-product-group-image img').attrib['data-src'],
                    'mausac':product.css('.lt-product-group-image img').attrib['data-src'],
                    'bonho':product.css('.lt-product-group-image img').attrib['data-src'],
                }
        next_page = response.css('div.pages ul:last-child li a').attrib['href']
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)

class fptshopSpider(scrapy.Spider):
    name = 'fptshop'
    start_urls = ['https://fptshop.com.vn/dien-thoai']

    def parse(self,response):
        for product in response.css('div.cdt-product.product-sale'):
            try:
                yield{
                    'name' : product.css('h3::text').get().replace('\t',''),
                    'special-price' : product.css('.special-price span::text').get().replace('\xa0₫',''),
                    'old-price' : product.css('.old-price span::text').get().replace('\xa0₫',''),
                    'url' : product.css('.lt-product-group-info a').attrib['href'],
                    'img' : product.css('.lt-product-group-image img').attrib['data-src'],
                }
            except:
                yield{
                    'name' : product.css('h3::text').get().replace('\t',''),
                    'special-price' : 0,
                    'old-price' : 0,
                    'url' : product.css('.lt-product-group-info a').attrib['href'],
                    'img' : product.css('.lt-product-group-image img').attrib['data-src'],
                }
        next_page = response.css('div.pages ul:last-child li a').attrib['href']
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)

# Xử lý tên sản phẩm
# Danh sách các từ cần loại bỏ
black_list = ['Chính', 'hãng', 'I', 'VN/A', 'chính','128GB','64GB','256GB','(','Fan', 'Edition',')',
              '4GB','8GB','3GB','-','32GB','6GB','Ram','2GB','5GB','(2021)','(6GB','128GB)',
              '(Đã', 'kích', 'hoạt','hành)','(Phiên', 'bản','mùa','hè)','Điện','thoại','2018','Trắng','thiên','vân',
              'xuân)','Mi','Festival)','(Fan','Edition)']

# Hàm xử lý tên sản phẩm
def name_processing(name):
  unprocess_name = name.split()
  processed_name = []
  for i in unprocess_name:
    if i not in black_list:
      processed_name.append(i)
  return ' '.join(processed_name)

class nguyenkimSpider(scrapy.Spider):
    name = 'nguyenkim'
    start_urls = ['https://www.nguyenkim.com/dien-thoai-di-dong/']

    def parse(self,response):
        for product in response.css('div.item-list'):
            item_link = product.css('.product-header a::attr(href)').get()
            
            item = {
                'ten': name_processing(product.css('.product-body .product-title a::text').get()) ,
                'url': item_link,
                'image': product.css('.product-image img::attr(data-src)').get(),
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham':'dienthoai',
                'thuonghieu':'iphone',
                'thuoctinh':  
                [

                    # {
                    # 'mausac': product.css('.lt-product-group-info .old-price .price::text').get(),
                    # 'bonho': product.css('.lt-product-group-info .old-price .price::text').get(),
                    # 'giamoi': product.css('.lt-product-group-info .price-box .special-price .price::text').get(),
                    # 'giagoc': product.css('.lt-product-group-info .old-price .price::text').get()
                    # }
                ]
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        #mau_active = .NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color a.active span::text
        next_page = response.css('.ty-pagination a.btn_next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = response.css('.product_info_price .product_info_price_value-real span::text').get()
        option_rom = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color:nth-child(2) a.active span::text').get()

        rom_active = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color:nth-child(2) a.active span::text').get()
        color_active = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color:nth-child(1) a.active span::text').get()

        attributes = []
        _attributes = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color:first-child .color a.opt-var::attr(title)')

        for attribute in _attributes:
            option_color = attribute.css('li > a > label > span.opt-name::text').get()
            option_new_price = attribute.css('a > label > span.opt-price::text').get()

            if option_color == color_active and option_rom == rom_active:
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

        return item





class shop24hstoreSpider(scrapy.Spider):
    name = '24hstore'
    start_urls = ['https://24hstore.vn/dien-thoai']

    def parse(self,response):
        for product in response.css('.product_cat .productlist #box_product div.product'):
            #try:
                yield{
                    'ten': product.css('h3::text').get(),
               #     'url': product.css('a').attrib['href'],
                #    'image': product.css('img').attrib['src'],
                #    'ngay': date.today().strftime("%Y-%m-%d"),
               #     'loaisanpham':'dienthoai',
                #    'thuonghieu':'iphone',
                #    'thuoctinh': []
                  
                }
      #      except:
      #          yield{
         
      #          }
        next_page = response.css('.product_cat a#load_more_button').attrib['href']
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)
    
    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = response.css('p.old-price > span::text').get()
        option_rom = response.css('div.linked-products.f-left > div > a.active > span::text').get()

        rom_active = response.css('div.linked-products.f-left > div > a.active > span::text').get()
        color_active = response.css('ul#configurable_swatch_color > li.selected > a > label > span.opt-name::text').get()

        attributes = []
        _attributes = response.css('ul#configurable_swatch_color > li')

        for attribute in _attributes:
            option_color = attribute.css('li > a > label > span.opt-name::text').get()
            option_new_price = attribute.css('a > label > span.opt-price::text').get()

            if option_color == color_active and option_rom == rom_active:
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

        return item

# Lớp crawl dữ liệu
class CellPhonesSpider(scrapy.Spider):
    name = 'mobile_cellphoneas'
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
                'ngay': date.today().strftime("%Y/%m/%d"),
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

        rom_active = response.css('div.linked-products.f-left > div > a.active > span::text').get()
        color_active = response.css('ul#configurable_swatch_color > li.selected > a > label > span.opt-name::text').get()

        attributes = []
        _attributes = response.css('ul#configurable_swatch_color > li')

        for attribute in _attributes:
            option_color = attribute.css('li > a > label > span.opt-name::text').get()
            option_new_price = attribute.css('a > label > span.opt-price::text').get()

            if option_color == color_active and option_rom == rom_active:
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

        return item