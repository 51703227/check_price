import scrapy
from datetime import date
import os
from scrapy_splash import SplashRequest

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
    name = 'nguyenkim1'
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

class phucanhSpider(scrapy.Spider):
    name = 'phucanh'
    start_urls = ['https://www.phucanh.vn/dien-thoai-thong-minh.html']

    def parse(self,response):
        
        def get_attr_from_name(name):
            attr_bonho = 'None'
            attr_mausac = 'None'
            list_attr_bonho = ['512GB','256GB','128GB','64GB','16GB','32GB','512Gb','256Gb','128Gb','64Gb','16Gb','32Gb']
            
            for i in list_attr_bonho:
                if i in name:
                    attr_bonho = i

            list_attr_mausac = ['Xám','Đỏ' ,'Đen' ,'Lục' ,'Lam','Đồng','Vàng','Xanh','Đen','Trắng','Thạch','Anh','lá','ngọc','lam','Sapphire']
            for b in list_attr_mausac:
                if b in name:
                    attr_mausac = b
                    print('_+_+_+',attr_mausac)
            return {'bonho':attr_bonho,'mausac':attr_mausac}
        
        def name_processing(name):
            black_list = ['Chính', 'hãng', 'I', 'VN/A', 'chính','128GB','64GB','256GB','(','Fan', 'Edition',')',
                    '4GB','8GB','3GB','-','32GB','6GB','Ram','2GB','5GB','(2021)','(6GB','128GB)',
                    '(Đã', 'kích', 'hoạt','hành)','(Phiên', 'bản','mùa','hè)','Điện','thoại','2018','Trắng','thiên','vân',
                    'xuân)','Mi','Festival)','(Fan','Edition),'
                    'độc',' đáo',
                    '6GB/128GB','Tím','Xám','Đen']
            bl_list = ['(' , ')' , '-' ,'/',
            '512GB','256GB','128GB','64GB','8GB','16GB','32GB','4GB','512Gb','256Gb','128Gb','64Gb','8Gb','16Gb','32Gb','4Gb',
            'Dương','Lá','Đỏ' ,'Đen' ,'Lục' ,'Cực' ,'Quang', 'tinh' ,'thạch', 'Ngọc', 'Trai','Bạc' ,'Hà','Lam', 'Thủy', 'Triều','Đồng','Vàng','Xanh','Đen','Trắng','Thạch','Anh','lá','ngọc','lam','Sapphire',
            'Black','Gold','Graphite','Silver','Blue','Tím','Green','Sliver','Trắng','Xám','Pacific','Blue','White','Gray','Violet',
            'độc','đáo','hạt','tiêu','(KHÔNG KÈM THẺ NHỚ)','Thoại','(2019)',
            '6.67Inch','6.5Inch','Đồng ánh kim','6.9Inch','2 sim','6.1Inch','2 Sim','VNA','hải' ,'quân' ,'san' ,'hô' ,'trai','dương','cẩm','KHÔNG KÈM THẺ NHỚ','San','Hô','Nhật','Thực','Sương','Mai','Đam','Mê','lục','bảo','Bảo','sương','hồng','Bích','tú','thủy','Hải','Âu','Hồng','pha','lê','quang','cực','Cam','hà','Phong','Vân'
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

        for product in response.css('#content-left .category-pro-list ul.product-list li'):
            item_link = 'https://www.phucanh.vn/' + product.css('a::attr(href)').get()
            #if item_link == 'https://www.phucanh.vn//xiaomi-redmi-note-10-4gb/64gb-xam.html':
                
            ten = product.css('h3::text').get()
            attr = get_attr_from_name(ten)
            ten = name_processing(ten)

            if item_link == None:
                continue
            item = {
                'ten': ten ,
                'url': item_link,
                'image': product.css('img::attr(data-original)').get(),
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham':'dienthoai',
                'thuonghieu':'iphone',
            }
            yield scrapy.Request(url=item_link, meta={'item': item,'attr':attr}, callback=self.get_detail)
            

        next_page = 'https://www.phucanh.vn/'+ response.css('.category-pro-list .paging a:last-child::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)
    


    def get_detail(self, response):
        
        def check_bonho(attr):
            list_attr = ['GB','Gb','gb']
            for a in list_attr:
                if a in attr:
                    return True    
            return False

        item = response.meta['item']
        attr = response.meta['attr']

        option_old_price = response.css('#product-info-price span.detail-product-old-price::text').get()
        option_new_price = response.css('#product-info-price span.detail-product-best-price::text').get()

        #color_active = response.css('div#overview .config-attribute span.item.color.current::attr(data-name)').get()
        #bonho_active = response.css('.config-attribute span.item.current::attr(data-name)').get()

        list_attr_active = response.css('.config-attribute span.item.current::attr(data-name)')

        
        bonho_active = attr['bonho']
        color_active = attr['mausac']
        print("------------attr--",attr['bonho'],attr['mausac'])

        for a in list_attr_active:
            print('++',a.get())
            if check_bonho(a.get()):
                bonho_active = a.get()
            else:
                color_active = a.get()
        
        print("------------",bonho_active,color_active)
        

        attributes = []
        attributes.append({
            'bonho': bonho_active if not attr['bonho'] else attr['bonho'],
            'mausac': color_active,
            'giagoc': option_old_price,
            'giamoi': option_new_price,
            'active': 'True'
        })
        item['thuoctinh'] = attributes

        return item


class hnamSpider(scrapy.Spider):
    name = 'hnam'
    start_urls = ['https://www.hnammobile.com/dien-thoai?filter=p-desc']

    def parse(self,response):
        
        def get_attr_from_name(name):
            attr_bonho = 'None'
            attr_mausac = 'None'
            list_attr_bonho = ['512GB','256GB','128GB','64GB','16GB','32GB','512Gb','256Gb','128Gb','64Gb','16Gb','32Gb']
            
            for i in list_attr_bonho:
                if i in name:
                    attr_bonho = i

            list_attr_mausac = ['Xám','Đỏ' ,'Đen' ,'Lục' ,'Lam','Đồng','Vàng','Xanh','Đen','Trắng','Thạch','Anh','lá','ngọc','lam','Sapphire']
            for b in list_attr_mausac:
                if b in name:
                    attr_mausac = b
                    print('_+_+_+',attr_mausac)
            return {'bonho':attr_bonho,'mausac':attr_mausac}
        
        def name_processing(name):
            black_list = ['Chính', 'hãng', 'I', 'VN/A', 'chính','128GB','64GB','256GB','(','Fan', 'Edition',')',
                    '4GB','8GB','3GB','-','32GB','6GB','Ram','2GB','5GB','(2021)','(6GB','128GB)',
                    '(Đã', 'kích', 'hoạt','hành)','(Phiên', 'bản','mùa','hè)','Điện','thoại','2018','Trắng','thiên','vân',
                    'xuân)','Mi','Festival)','(Fan','Edition),'
                    'độc',' đáo',
                    '6GB/128GB','Tím','Xám','Đen']
            bl_list = ['(' , ')' , '-' ,'/',
            '512GB','256GB','128GB','64GB','8GB','16GB','32GB','4GB','512Gb','256Gb','128Gb','64Gb','8Gb','16Gb','32Gb','4Gb',
            'Dương','Lá','Đỏ' ,'Đen' ,'Lục' ,'Cực' ,'Quang', 'tinh' ,'thạch', 'Ngọc', 'Trai','Bạc' ,'Hà','Lam', 'Thủy', 'Triều','Đồng','Vàng','Xanh','Đen','Trắng','Thạch','Anh','lá','ngọc','lam','Sapphire',
            'Black','Gold','Graphite','Silver','Blue','Tím','Green','Sliver','Trắng','Xám','Pacific','Blue','White','Gray','Violet',
            'độc','đáo','hạt','tiêu','(KHÔNG KÈM THẺ NHỚ)','Thoại','(2019)',
            '6.67Inch','6.5Inch','Đồng ánh kim','6.9Inch','2 sim','6.1Inch','2 Sim','VNA','hải' ,'quân' ,'san' ,'hô' ,'trai','dương','cẩm','KHÔNG KÈM THẺ NHỚ','San','Hô','Nhật','Thực','Sương','Mai','Đam','Mê','lục','bảo','Bảo','sương','hồng','Bích','tú','thủy','Hải','Âu','Hồng','pha','lê','quang','cực','Cam','hà','Phong','Vân'
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

        for product in response.css('.list-products div.product-item-list'):   #####
            item_link = product.css('.product-image a::attr(href)').get()       #####
            #if item_link == 'https://www.phucanh.vn//xiaomi-redmi-note-10-4gb/64gb-xam.html':
                
            ten = product.css('.product-name a::text').get()       #####
            attr = get_attr_from_name(ten)
            ten = name_processing(ten)

            o_price = product.css('.product-price del::text').get()
            n_price = product.css('.product-price b::text').get()
            price = {
                'o_price':o_price,
                'n_price':n_price
            }
            if item_link == None:
                continue
            item = {
                'ten': ten ,
                'url': item_link,
                'image': product.css('.product-image a source::attr(data-srcset)').get(), #####
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham':'dienthoai',
                'thuonghieu':'iphone',
            }
            yield scrapy.Request(url=item_link, meta={'item': item,'attr':attr,'price':price}, callback=self.get_detail)
            
            

        next_page = response.css('ul.global_pagination li.next-item a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)
    


    def get_detail(self, response):
        
        def check_bonho(attr):
            list_attr = ['GB','Gb','gb']
            for a in list_attr:
                if a in attr:
                    return True    
            return False

        item = response.meta['item']
        attr = response.meta['attr']
        price = response.meta['price']
        
        option_old_price = price['o_price']  #####
        option_new_price = price['n_price']     #####   

        color_active = response.css('.product-detail-wrapper .swiper-outer-wrapper div.option.active::attr(data-color)').get()
        bonho_active = response.css('.product-detail-wrapper .list-block-options a.active::text').get()

        #list_attr_active = response.css('.config-attribute span.item.current::attr(data-name)')

        
        #bonho_active = attr['bonho']
        #color_active = attr['mausac']
        print("------------attr--",attr['bonho'],attr['mausac'])

        #for a in list_attr_active:
        #    print('++',a.get())
        #    if check_bonho(a.get()):
        #        bonho_active = a.get()
        #    else:
        #        color_active = a.get()
        
        print("------------",bonho_active,color_active)
        

        attributes = []
        attributes.append({
            'bonho': bonho_active,
            'mausac': color_active,
            'giagoc': option_old_price,
            'giamoi': option_new_price,
            'active': 'True'
        })
        item['thuoctinh'] = attributes

        return item


class mediamartSpider(scrapy.Spider):
    name = 'mediamart'
    start_urls = ['https://mediamart.vn/smartphones/?&trang=%s'% page for page in range(1,9)]

    def parse(self,response):
        
        def get_attr_from_name(name):
            attr_bonho = 'None'
            attr_mausac = 'None'
            list_attr_bonho = ['512GB','256GB','128GB','64GB','16GB','32GB','512Gb','256Gb','128Gb','64Gb','16Gb','32Gb']
            
            for i in list_attr_bonho:
                if i in name:
                    attr_bonho = i

            list_attr_mausac = ['Xám','Đỏ' ,'Đen' ,'Lục' ,'Lam','Đồng','Vàng','Xanh','Đen','Trắng','Thạch','Anh','lá','ngọc','lam','Sapphire']
            for b in list_attr_mausac:
                if b in name:
                    attr_mausac = b
                    print('_+_+_+',attr_mausac)
            return {'bonho':attr_bonho,'mausac':attr_mausac}
        
        def name_processing(name):
            black_list = ['Chính', 'hãng', 'I', 'VN/A', 'chính','128GB','64GB','256GB','(','Fan', 'Edition',')',
                    '4GB','8GB','3GB','-','32GB','6GB','Ram','2GB','5GB','(2021)','(6GB','128GB)',
                    '(Đã', 'kích', 'hoạt','hành)','(Phiên', 'bản','mùa','hè)','Điện','thoại','2018','Trắng','thiên','vân',
                    'xuân)','Mi','Festival)','(Fan','Edition),'
                    'độc',' đáo',
                    '6GB/128GB','Tím','Xám','Đen']
            bl_list = ['(' , ')' , '-' ,'/',
            '512GB','256GB','128GB','64GB','8GB','16GB','32GB','4GB','512Gb','256Gb','128Gb','64Gb','8Gb','16Gb','32Gb','4Gb',
            'Dương','Lá','Đỏ' ,'Đen' ,'Lục' ,'Cực' ,'Quang', 'tinh' ,'thạch', 'Ngọc', 'Trai','Bạc' ,'Hà','Lam', 'Thủy', 'Triều','Đồng','Vàng','Xanh','Đen','Trắng','Thạch','Anh','lá','ngọc','lam','Sapphire',
            'Black','Gold','Graphite','Silver','Blue','Tím','Green','Sliver','Trắng','Xám','Pacific','Blue','White','Gray','Violet',
            'độc','đáo','hạt','tiêu','(KHÔNG KÈM THẺ NHỚ)','Thoại','2019','2020',
            '6.67Inch','6.5Inch','Đồng ánh kim','6.9Inch','2 sim','6.1Inch','2 Sim','VNA','hải' ,'quân' ,'san' ,'hô' ,'trai','dương','cẩm','KHÔNG KÈM THẺ NHỚ','San','Hô','Nhật','Thực','Sương','Mai','Đam','Mê','lục','bảo','Bảo','sương','hồng','Bích','tú','thủy','Hải','Âu','Hồng','pha','lê','quang','cực','Cam','hà','Phong','Vân'
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

        for product in response.css('.pl18-item-ul li'):   #####
            item_link = 'https://mediamart.vn/'+ product.css('.pl18-item-image a::attr(href)').get()       #####
            #if item_link == 'https://www.phucanh.vn//xiaomi-redmi-note-10-4gb/64gb-xam.html':
                
            ten = product.css('.pl18-item-name a::attr(title)').get()      #####
            attr = get_attr_from_name(ten)
            ten = name_processing(ten)

            o_price = product.css('.product-price del::text').get()
            n_price = product.css('.product-price b::text').get()
            price = {
                'o_price':o_price,
                'n_price':n_price
            }
            if item_link == None:
                continue
            item = {
                'ten': ten ,
                'url': item_link,
                'image': product.css('.pl18-item-image a img::attr(src)').get(), #####
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham':'dienthoai',
                'thuonghieu':'apple',
            }
            yield scrapy.Request(url=item_link, meta={'item': item,'attr':attr,'price':price}, callback=self.get_detail)
            
            
        
        #next_page = 'https://mediamart.vn/smartphones/?&trang='
        #if next_page is not None:
        #    yield response.follow(next_page,callback=self.parse)
    


    def get_detail(self, response):
        
        def check_bonho(attr):
            list_attr = ['GB','Gb','gb']
            for a in list_attr:
                if a in attr:
                    return True    
            return False
        def split_attr(attr):
            if not attr:
                return {'mausac':'None','bonho':'None'}
            list_attr = attr.split()
            mausac = 'None'
            bonho = 'None'
            list_mausac = [
                'Xám','Đỏ' ,'Đen' ,'Lục' ,'Lam','Đồng','Vàng','Xanh','Đen','Trắng','Thạch','Anh','lá','ngọc','lam','Sapphire',
                'Black','Gold','Graphite','Silver','Blue','Tím','Green','Sliver','Trắng','Xám','Pacific','Blue','White','Gray','Violet',
            ]
            list_bonho = [
                '512GB','256GB','128GB','64GB','16GB','32GB','512Gb','256Gb','128Gb','64Gb','16Gb','32Gb',
                '512G','256G','128G','64G','16G','32G'            
            ]
            for a in list_attr:
                if a in list_mausac:
                    mausac = a
                if a in list_bonho:
                    bonho = a + 'B'
            return {'mausac':mausac,'bonho':bonho}

        item = response.meta['item']
        attr = response.meta['attr']
        price = response.meta['price']
        
        option_old_price = response.css('.pdrrp-price::attr(content)').get()  #####
        option_new_price = response.css('.pd-evh-price b::text').get()    #####   

        #color_active = response.css('.product-detail-wrapper .swiper-outer-wrapper div.option.active::attr(data-color)').get()
        #bonho_active = response.css('.product-detail-wrapper .list-block-options a.active::text').get()

        #list_attr_active = response.css('.config-attribute span.item.current::attr(data-name)')
        attr_active = response.css('.pdv-list a.pdv-item-a.active span.name::text').get()
        
        attr = split_attr(attr_active)
        #bonho_active = attr['bonho']
        #color_active = attr['mausac']
        print("------------attr--",attr['bonho'],attr['mausac'])

        #for a in list_attr_active:
        #    print('++',a.get())
        #    if check_bonho(a.get()):
        #        bonho_active = a.get()
        #    else:
        #        color_active = a.get()
        
        #print("------------",bonho_active,color_active)
        

        attributes = []
        attributes.append({
            'bonho': attr['bonho'],
            'mausac': attr['mausac'],
            'giagoc': option_old_price,
            'giamoi': option_new_price,
            'active': 'True'
        })
        item['thuoctinh'] = attributes

        return item