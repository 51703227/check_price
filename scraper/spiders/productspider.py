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



class nguyenkimSpider(scrapy.Spider):
    name = 'nguyenkim'
    start_urls = ['https://www.nguyenkim.com/dien-thoai-di-dong/']

    def parse(self,response):
        def name_processing(name):
            black_list = ['Chính', 'hãng', 'I', 'VN/A', 'chính','128GB','64GB','256GB','(','Fan', 'Edition',')',
                    '4GB','8GB','3GB','-','32GB','6GB','Ram','2GB','5GB','(2021)','(6GB','128GB)',
                    '(Đã', 'kích', 'hoạt','hành)','(Phiên', 'bản','mùa','hè)','Điện','thoại','2018','Trắng','thiên','vân',
                    'xuân)','Mi','Festival)','(Fan','Edition),'
                    'độc',' đáo',
                    '6GB/128GB','Tím','Xám','Đen']
            bl_list = ['(' , ')' , '-' ,'/',
            '512GB','256GB','128GB','64GB','8GB','16GB','32GB','4GB',
            'Dương','Lá','Đỏ' ,'Đen' ,'Lục' ,'Cực' ,'Quang', 'tinh' ,'thạch', 'Ngọc', 'Trai','Bạc' ,'Hà','Lam', 'Thủy', 'Triều','Đồng','Vàng','Xanh','Đen','Trắng','Thạch','Anh','lá','ngọc','lam','Sapphire',
            'độc','đáo','hạt','tiêu','(KHÔNG KÈM THẺ NHỚ)','Thoại','(2019)',
            'hải' ,'quân' ,'san' ,'hô' ,'trai','dương','cẩm','KHÔNG KÈM THẺ NHỚ','San','Hô','Nhật','Thực','Sương','Mai','Đam','Mê','lục','bảo','Bảo','sương','hồng','Bích','tú','thủy','Hải','Âu','Hồng','pha','lê','quang','cực','Cam','hà','Phong','Vân'
            ]

            if name == None:
                return ''
            for character in bl_list:
                name = name.replace(character,'')
            
            unprocess_name = name.split()
            processed_name = []
            for i in unprocess_name:
                if i not in black_list:
                    processed_name.append(i)
            return ' '.join(processed_name)

        for product in response.css('div.item-list'):
            item_link = product.css('.product-header a::attr(href)').get()
            ten = name_processing(product.css('.product-body .product-title a::text').get()) 
            if item_link == None:
                continue
            item = {
                'ten': ten ,
                'url': item_link,
                'image': product.css('.product-image img::attr(data-src)').get(),
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham':'dienthoai',
                'thuonghieu':'iphone',
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        next_page = response.css('.ty-pagination a.btn_next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)
    


    def get_detail(self, response):
        def check_bonho(attr):
            if 'GB' in attr:
                return True
            else:
                return False
                
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = response.css('.product_info_price .product_info_price_value-real span::text').get()
#        option_rom = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color:nth-child(2) a.active span::text').get()

#        rom_active = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color:nth-child(2) a.active span::text').get()
#        color_active = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color:nth-child(1) a.active span::text').get()

        attr_active = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color .color a.opt-var.active::attr(title)')

        attributes = []
        _attributes = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color .color a.opt-var::attr(title)')
        
        if not _attributes:
            option_new_price = response.css('.product_info_price .product_info_price_value-final span::text').get()
            attributes.append({
                    'bonho': 'Null',
                    'mausac': 'Null',
                    'giagoc': option_old_price.replace('đ','').replace('.',''),
                    'giamoi': option_new_price.replace('đ','').replace('.',''),
                    'active': 'True'
                })
            item['thuoctinh'] = attributes
        else:
            rom_active = 'None'
            color_active ='None'
            for attr in attr_active:
                if check_bonho(attr.get()):
                    rom_active = attr.get()
                else:
                    color_active = attr.get()

            #for attribute in _attributes:
            #if check_bonho(attribute.get()):
            #    continue

            #option_color = attribute.get()
            option_new_price = response.css('.product_info_price .product_info_price_value-final span::text').get()

            #if option_color == color_active :
            #    active = True
            #else:
            #    active = False

            attributes.append({
                'bonho': rom_active,
                'mausac': color_active,
                'giagoc': option_old_price.replace('đ','').replace('.',''),
                'giamoi': option_new_price.replace('đ','').replace('.',''),
                'active': 'True'
            })
            item['thuoctinh'] = attributes

        return item


class nguyenkimSpider(scrapy.Spider):
    name = 'nguyenkim'
    start_urls = ['https://www.nguyenkim.com/dien-thoai-di-dong/']

    def parse(self,response):
        def name_processing(name):
            black_list = ['Chính', 'hãng', 'I', 'VN/A', 'chính','128GB','64GB','256GB','(','Fan', 'Edition',')',
                    '4GB','8GB','3GB','-','32GB','6GB','Ram','2GB','5GB','(2021)','(6GB','128GB)',
                    '(Đã', 'kích', 'hoạt','hành)','(Phiên', 'bản','mùa','hè)','Điện','thoại','2018','Trắng','thiên','vân',
                    'xuân)','Mi','Festival)','(Fan','Edition),'
                    'độc',' đáo',
                    '6GB/128GB','Tím','Xám','Đen']
            bl_list = ['(' , ')' , '-' ,'/',
            '512GB','256GB','128GB','64GB','8GB','16GB','32GB','4GB',
            'Dương','Lá','Đỏ' ,'Đen' ,'Lục' ,'Cực' ,'Quang', 'tinh' ,'thạch', 'Ngọc', 'Trai','Bạc' ,'Hà','Lam', 'Thủy', 'Triều','Đồng','Vàng','Xanh','Đen','Trắng','Thạch','Anh','lá','ngọc','lam','Sapphire',
            'độc','đáo','hạt','tiêu','(KHÔNG KÈM THẺ NHỚ)','Thoại','(2019)',
            'hải' ,'quân' ,'san' ,'hô' ,'trai','dương','cẩm','KHÔNG KÈM THẺ NHỚ','San','Hô','Nhật','Thực','Sương','Mai','Đam','Mê','lục','bảo','Bảo','sương','hồng','Bích','tú','thủy','Hải','Âu','Hồng','pha','lê','quang','cực','Cam','hà','Phong','Vân'
            ]

            if name == None:
                return ''
            for character in bl_list:
                name = name.replace(character,'')
            
            unprocess_name = name.split()
            processed_name = []
            for i in unprocess_name:
                if i not in black_list:
                    processed_name.append(i)
            return ' '.join(processed_name)

        for product in response.css('div.item-list'):
            item_link = product.css('.product-header a::attr(href)').get()
            ten = name_processing(product.css('.product-body .product-title a::text').get()) 
            if item_link == None:
                continue
            item = {
                'ten': ten ,
                'url': item_link,
                'image': product.css('.product-image img::attr(data-src)').get(),
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham':'dienthoai',
                'thuonghieu':'iphone',
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        next_page = response.css('.ty-pagination a.btn_next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)
    


    def get_detail(self, response):
        def check_bonho(attr):
            if 'GB' in attr:
                return True
            else:
                return False
                
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = response.css('.product_info_price .product_info_price_value-real span::text').get()
#        option_rom = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color:nth-child(2) a.active span::text').get()

#        rom_active = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color:nth-child(2) a.active span::text').get()
#        color_active = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color:nth-child(1) a.active span::text').get()

        attr_active = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color .color a.opt-var.active::attr(title)')

        attributes = []
        _attributes = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color .color a.opt-var::attr(title)')
        
        if not _attributes:
            option_new_price = response.css('.product_info_price .product_info_price_value-final span::text').get()
            attributes.append({
                    'bonho': 'Null',
                    'mausac': 'Null',
                    'giagoc': option_old_price.replace('đ','').replace('.',''),
                    'giamoi': option_new_price.replace('đ','').replace('.',''),
                    'active': 'True'
                })
            item['thuoctinh'] = attributes
        else:
            rom_active = 'None'
            color_active ='None'
            for attr in attr_active:
                if check_bonho(attr.get()):
                    rom_active = attr.get()
                else:
                    color_active = attr.get()

            #for attribute in _attributes:
            #if check_bonho(attribute.get()):
            #    continue

            #option_color = attribute.get()
            option_new_price = response.css('.product_info_price .product_info_price_value-final span::text').get()

            #if option_color == color_active :
            #    active = True
            #else:
            #    active = False

            attributes.append({
                'bonho': rom_active,
                'mausac': color_active,
                'giagoc': option_old_price.replace('đ','').replace('.',''),
                'giamoi': option_new_price.replace('đ','').replace('.',''),
                'active': 'True'
            })
            item['thuoctinh'] = attributes

        return item

class didongthongminhSpider(scrapy.Spider):
    name = 'didongthongminh'
    start_urls = ['https://www.nguyenkim.com/dien-thoai-di-dong/']

    def parse(self,response):
        
        def get_attr_from_name(name):
            attr_bonho = 'None'
            attr_mausac = 'None'
            list_attr_bonho = ['512GB','256GB','128GB','64GB','8GB','16GB','32GB','4GB']
            list_attr_mausac = ['Dương','Lá','Đỏ' ,'Đen' ,'Lục' ,'Cực' ,'Quang', 'tinh' ,'thạch', 'Ngọc', 'Trai','Bạc' ,'Hà','Lam', 'Thủy', 'Triều','Đồng','Vàng','Xanh','Đen','Trắng','Thạch','Anh','lá','ngọc','lam','Sapphire']
            for i in list_attr_bonho:
                if i in name:
                    attr_bonho = i
            for i in list_attr_mausac:
                if i in name:
                    attr_mausac = i
            return {'attr_bonho':attr_bonho,'attr_mausac':attr_mausac}
        
        def name_processing(name):
            black_list = ['Chính', 'hãng', 'I', 'VN/A', 'chính','128GB','64GB','256GB','(','Fan', 'Edition',')',
                    '4GB','8GB','3GB','-','32GB','6GB','Ram','2GB','5GB','(2021)','(6GB','128GB)',
                    '(Đã', 'kích', 'hoạt','hành)','(Phiên', 'bản','mùa','hè)','Điện','thoại','2018','Trắng','thiên','vân',
                    'xuân)','Mi','Festival)','(Fan','Edition),'
                    'độc',' đáo',
                    '6GB/128GB','Tím','Xám','Đen']
            bl_list = ['(' , ')' , '-' ,'/',
            '512GB','256GB','128GB','64GB','8GB','16GB','32GB','4GB',
            'Dương','Lá','Đỏ' ,'Đen' ,'Lục' ,'Cực' ,'Quang', 'tinh' ,'thạch', 'Ngọc', 'Trai','Bạc' ,'Hà','Lam', 'Thủy', 'Triều','Đồng','Vàng','Xanh','Đen','Trắng','Thạch','Anh','lá','ngọc','lam','Sapphire',
            'độc','đáo','hạt','tiêu','(KHÔNG KÈM THẺ NHỚ)','Thoại','(2019)',
            'hải' ,'quân' ,'san' ,'hô' ,'trai','dương','cẩm','KHÔNG KÈM THẺ NHỚ','San','Hô','Nhật','Thực','Sương','Mai','Đam','Mê','lục','bảo','Bảo','sương','hồng','Bích','tú','thủy','Hải','Âu','Hồng','pha','lê','quang','cực','Cam','hà','Phong','Vân'
            ]

            if name == None:
                return ''
            for character in bl_list:
                name = name.replace(character,'')
            
            unprocess_name = name.split()
            processed_name = []
            for i in unprocess_name:
                if i not in black_list:
                    processed_name.append(i)
            return ' '.join(processed_name)

        for product in response.css('div.product-item-list'):
            item_link = product.css('.product-name a::attr(href)').get()
            ten = product.css('.product-name a::text').get()
            attr = get_attr_from_name(ten)
            ten = name_processing(ten)
            if item_link == None:
                continue
            item = {
                'ten': ten ,
                'url': item_link,
                'image': product.css('.product-image a::attr(href)').get(),
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham':'dienthoai',
                'thuonghieu':'iphone',
            }
            yield scrapy.Request(url=item_link, meta={'item': item,'attr':attr}, callback=self.get_detail)

        next_page = response.css('ul.global_pagination li.next-item a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)
    


    def get_detail(self, response):
        
        def check_bonho(attr):
            if 'GB' in attr:
                return True
            else:
                return False

        #self.log('Visited ' + response.url)
        item = response.meta['item']
        attr = response.meta['attr']

        option_old_price = response.css('.product_info_price .product_info_price_value-real span::text').get()
#        option_rom = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color:nth-child(2) a.active span::text').get()

#        rom_active = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color:nth-child(2) a.active span::text').get()
#        color_active = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color:nth-child(1) a.active span::text').get()
        attr['mausac']
        attr['bonho']
        
        #active = response.css('.section-product-detail .swiper-outer-wrapper .itemi-p2 .option.active::attr(data-color)').get()
        #response.css('.section-product-detail .list-block-options a.active::text').get()
        attr_active = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color .color a.opt-var.active::attr(title)')

        attributes = []
        _attributes = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color .color a.opt-var::attr(title)')
        
        if not _attributes:
            option_new_price = response.css('.product_info_price .product_info_price_value-final span::text').get()
            attributes.append({
                    'bonho': 'Null',
                    'mausac': 'Null',
                    'giagoc': option_old_price.replace('đ','').replace('.',''),
                    'giamoi': option_new_price.replace('đ','').replace('.',''),
                    'active': 'True'
                })
            item['thuoctinh'] = attributes
        else:
            rom_active = 'None'
            color_active ='None'
            for attr in attr_active:
                if check_bonho(attr.get()):
                    rom_active = attr.get()
                else:
                    color_active = attr.get()

            #for attribute in _attributes:
            #if check_bonho(attribute.get()):
            #    continue

            #option_color = attribute.get()
            option_new_price = response.css('.product_info_price .product_info_price_value-final span::text').get()

            #if option_color == color_active :
            #    active = True
            #else:
            #    active = False

            attributes.append({
                'bonho': rom_active,
                'mausac': color_active,
                'giagoc': option_old_price.replace('đ','').replace('.',''),
                'giamoi': option_new_price.replace('đ','').replace('.',''),
                'active': 'True'
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