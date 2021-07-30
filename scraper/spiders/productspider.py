from typing import Counter
from django.db.models.fields import NullBooleanField
import scrapy
from datetime import date
import os
from scrapy_splash import SplashRequest


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

    f = open("blacklist.txt", "r",encoding='utf-8')
    lines = f.read().splitlines()
    blacklist = sorted(lines,key=len,reverse=True)

    if name == None:
        return ''
    for character in blacklist:
        if character in name or character.lower() in name or character.title() in name or character.upper():
            name = name.replace(character,'')
            name = name.replace(character.lower(),'')
            name = name.replace(character.title(),'')
            name = name.replace(character.upper(),'')
    
    unprocess_name = name.split()
    processed_name = []
    for i in unprocess_name:
        if i not in black_list:
            processed_name.append(i)
    return ' '.join(processed_name).title()

def format_price(price):
    _list = ['đ','₫','.',',','VNĐ','VND','\r','\n','\t',' ']
    if not price:
        return 'None'
    else:
        for i in _list:
            price = price.replace(i,'')
    return price

def format_bonho(bonho):
    list_bo_nho= ['512GB','256GB','128GB','64GB','8GB','16GB','32GB','4GB']
    _list = [' ','Mới','100%']
    if not bonho or bonho in ['None','none','NONE','Actived','Active','Chưa Active','ChưaActive']:
        return 'None'
    else:
        for i in _list:
            bonho = bonho.replace(i,'')
            
        for i in list_bo_nho:
            if i in bonho:
                return i
    return bonho.upper()

def format_mausac(mausac):
    _list = ['\n','\t','99%','Mới','Màu','No AT','Đã AT']
    if not mausac or mausac in ['256G','2Sim','Hàn','Mỹ','Mĩ','128Gb','512G','512Gb Mới','256Gb Mới','128Gb Mới','Mới','Chưa Active','Mới 100%','Đã Active','Cũ 95%']:
        return 'None'
    else:
        for i in _list:
            mausac = mausac.replace(i,'')
    _dict = {
        'blue':'Xanh Dương',
        'graphite':'Xám',
        'gray':'Xám',
        'silver':'Bạc',
        'gold':'Vàng',
        'grey':'Xám',
        'white':'Trắng',
        'black':'Đen',
        'red':'Đỏ',
        'green':'Xanh Lá',
        'purple':'Tím',
        'yellow':'Vàng',
        'bronze':'Đồng',
        'pacific blue':'Xanh Dương',
        'balck':'Đen',
        'pacificblue':'Xanh Dương',
        'pink':'Hồng',
        'violet':'Tím',
        'xanh lục':'Xanh Lá',
        'xanh da trời':'Xanh Dương',
        'đen cuốn hút':'Đen',
        'green sapphire': 'Xanh Lá',
        'fullbox':'None',
        'tím':'Tím',
        'hồng':'Hồng',
        'vàng phù sa':'Vàng',
        'vàng đồng':'Vàng',
        'xanh biển':'Xanh Dương',
        'xanh blue':'Xanh Dương',
        'xám':'Xám',
        'xanh':'Xanh Dương',
        'xanh đậm':'Xanh Dương',
        'xanh đã at':'Xanh Dương',
        'pacificblue':'Xanh Dương',
        'xanh':'Xanh Dương',
        'tím bạc':'Tím',
        'tím hồng':'Tím',
        'tím đam mê':'Tím',
        'tím':'Tím',
        'da cam':'Cam',
        'bạc cá tính':'Bạc',
        'bạc ánh trăng':'Bạc',
        'bạc đa sắc':'Bạc',
        'hường':'Hồng',
        'dark blue':'Xanh Dương',
        'đen huyền bí':'Đen',
        'than':'Xám',
        'trắng':'Trắng',
        'trắng núi tuyết':'Trắng',
        'tím sương đêm':'Tím',
        'vàng':'Vàng',
        'xanh lam':'Xanh Lá',
        'xanh lục':'Xanh Lá',
        'cyan':'Xanh Lơ',
        'rose gold':'Hồng Vàng',
        'purple-fire':'Tím',
        'mirror purple':'Tím',
        'mirror black':'Đen',
        'fancy sky':'Xanh Dương',
        'dark blue':'Xanh Dương',
        'quartz black':'Đen',
        'emerald green':'Xanh Lá',
        'navy':'Xanh Dương',
        'dark blue':'Xanh Dương',
        'dark silver':'Bạc',
        'orange':'Cam',
        'blue coral':'Xanh Dương',
        'xanh thiên thạch':'Xanh Dương',
        'xanh lục bảo':'Xanh Lá',
        'copper':'Vàng',
        'charcoal':'Xám',
    }
    if not _dict.get(mausac.lower().strip()):
        return mausac.title().strip()
    else:
        return _dict.get(mausac.lower().strip())


class nguyenkimSpider(scrapy.Spider):
    name = 'nguyenkim'
    start_urls = ['https://www.nguyenkim.com/dien-thoai-di-dong/']

    def parse(self,response):
       
        for product in response.css('div.product'):
            item_link = product.css('.product-header a::attr(href)').get()
            if item_link: # == 'https://www.nguyenkim.com/dien-thoai-iphone-12-128gb-do.html':
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

        attr_active = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color .color a.opt-var.active::attr(title)')

        attributes = []
        _attributes = response.css('.NkPdp_productInfo .productInfo_col-23 .productInfo_col-2 .product_pick_color .color a.opt-var::attr(title)')
        
        if not _attributes:
            option_new_price = response.css('.product_info_price .product_info_price_value-final span::text').get()
            attributes.append({
                    'bonho': 'None',
                    'mausac': 'None',
                    'giagoc': format_price(option_old_price) ,
                    'giamoi': format_price(option_new_price) ,
                    'active': 'True'
                })
            item['thuoctinh'] = attributes
            item['tskt'] = response.css('.productSpecification_brief table').get()
            item['mota'] = response.css('.pdp-box #content_description.wysiwyg-content .productFeature_content').get().replace('display: none;','').replace('src','d-src').replace('data-d-src','src')
        else:
            rom_active = 'None'
            color_active ='None'
            for attr in attr_active:
                if check_bonho(attr.get()):
                    rom_active = attr.get()
                else:
                    color_active = attr.get()


            option_new_price = response.css('.product_info_price .product_info_price_value-final span::text').get()


            attributes.append({
                'bonho': format_bonho(rom_active) ,
                'mausac': format_mausac(color_active) ,
                'giagoc':  format_price(option_old_price),
                'giamoi':  format_price(option_new_price),
                'active': 'True'
            })
            item['thuoctinh'] = attributes
            item['tskt'] = response.css('.productSpecification_brief table').get()
            item['mota'] = response.css('.pdp-box #content_description.wysiwyg-content .productFeature_content').get().replace('display: none;','').replace('src','d-src').replace('data-d-src','src')
        return item


class phucanhSpider(scrapy.Spider):
    name = 'phucanh'
    start_urls = ['https://www.phucanh.vn/dien-thoai-thong-minh.html']

    def parse(self,response):

        for product in response.css('#content-left .category-pro-list ul.product-list li'):
            item_link = 'https://www.phucanh.vn' + product.css('a::attr(href)').get()
            #if item_link == 'https://www.phucanh.vn/samsung-galaxy-note-20-ultra-256gb-trang-huyen-bi-6.9inch/-256gb/-2-sim.html':
                
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
            
            

        next_page = 'https://www.phucanh.vn'+ response.css('.category-pro-list .paging a:last-child::attr(href)').get()
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

        for a in list_attr_active:
            if check_bonho(a.get()):
                bonho_active = a.get()
            else:
                color_active = a.get()
        
        attributes = []
        attributes.append({
            'bonho': format_bonho(bonho_active) if not attr['bonho'] else format_bonho(attr['bonho']),
            'mausac': format_mausac(color_active) ,
            'giagoc': format_price(option_old_price) ,
            'giamoi': format_price(option_new_price) ,
            'active': 'True'
        })
        item['thuoctinh'] = attributes
        item['tskt'] = response.css('.tbl-technical table').get()
        item['mota'] = response.css('.content-tab-left .nd').get().replace('height:450px;overflow: hidden;','').replace('display: none;','').replace('src','d-src').replace('data-src','src').replace('data-origin','src')
        return item

class hnamSpider(scrapy.Spider):
    name = 'hnam'
    start_urls = ['https://www.hnammobile.com/dien-thoai?filter=p-desc']

    def parse(self,response):

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
        #print("------------attr--",attr['bonho'],attr['mausac'])

        #for a in list_attr_active:
        #    print('++',a.get())
        #    if check_bonho(a.get()):
        #        bonho_active = a.get()
        #    else:
        #        color_active = a.get()
        
        #print("------------",bonho_active,color_active)
        

        attributes = []
        attributes.append({
            'bonho': format_bonho(bonho_active) ,
            'mausac': format_mausac(color_active) ,
            'giagoc': format_price(option_old_price),
            'giamoi': format_price(option_new_price) ,
            'active': 'True'
        })
        item['thuoctinh'] = attributes
        item['tskt'] = response.css('.section-open-box table').get()
        item['mota'] = response.css('.article-news .article-main-content').get().replace('display: none;','').replace('data-src','src')
        return item


class mediamartSpider(scrapy.Spider):
    name = 'mediamart'
    start_urls = ['https://mediamart.vn/smartphones/?&trang=%s'% page for page in range(1,9)]

    def parse(self,response):
        
        for product in response.css('.pl18-item-ul li'):   #####
            item_link = 'https://mediamart.vn'+ product.css('.pl18-item-image a::attr(href)').get()       #####
            if item_link: # == 'https://mediamart.vn/smartphones/apple/apple-iphone-12-pro-128g-blue-2020.htm':
                
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
                    'image': product.css('.pl18-item-image a img::attr(data-original)').get(), #####
                    'ngay': date.today().strftime("%Y-%m-%d"),
                    'loaisanpham':'dienthoai',
                    'thuonghieu':'apple',
                }
                yield scrapy.Request(url=item_link, meta={'item': item,'attr':attr,'price':price}, callback=self.get_detail)
                #break
            
        
        #next_page = 'https://mediamart.vn/smartphones/?&trang='
        #if next_page is not None:
        #    yield response.follow(next_page,callback=self.parse)

    def get_detail(self, response):
        
        def split_attr(attr):
            if not attr:
                return {'mausac':'None','bonho':'None'}
        
            mausac = 'None'
            bonho = 'None'
            list_mausac = [
                'Xám đậm','Xanh lá','Xanh dương','Xám','Đỏ' ,'Đen' ,'Lục' ,'Lam','Đồng','Vàng','Xanh','Đen','Trắng','Thạch','Anh','ngọc','lam','Sapphire',
                'Red','Purple','Yellow','Black','Gold','Graphite','Silver','Blue','Tím','Green','Sliver','Trắng','Xám','Pacific','Blue','White','Gray','Violet',
            ]
            list_bonho = [
                '512GB','256GB','128GB','64GB','16GB','32GB','512Gb','256Gb','128Gb','64Gb','16Gb','32Gb',
                '512G','256G','128G','64G','16G','32G'            
            ]
            for a in list_mausac:
                if a in attr:
                    mausac = a
                    break
            for a in list_bonho:
                if a in attr:
                    bonho = a.replace('G','').replace('B','').replace('b','') + 'GB'
                    break
            return {'mausac':mausac,'bonho':bonho}

        item = response.meta['item']
        attr_from_name = response.meta['attr']
        price = response.meta['price']
        
        
        pr = response.css('.pd-eventhot-bl').get()
        if pr:
            option_old_price = response.css('.pdrrp-price::attr(content)').get()
            option_new_price = response.css('.pd-evh-price b::text').get()  ##### 
        else:
            option_old_price = response.css('.pdrrp-pmarket::text').get()  #####
            option_new_price = response.css('.pdrrp-price::attr(content)').get()    #####   

        
        #color_active = response.css('.product-detail-wrapper .swiper-outer-wrapper div.option.active::attr(data-color)').get()
        #bonho_active = response.css('.product-detail-wrapper .list-block-options a.active::text').get()

        #list_attr_active = response.css('.config-attribute span.item.current::attr(data-name)')
        attr_active = response.css('.pdv-list a.pdv-item-a.active span.name::text').get()
        
        attr = split_attr(attr_active)
        #bonho_active = attr['bonho']
        #color_active = attr['mausac']
        print("------------attr--",attr_active, attr['bonho'],attr['mausac'])
        
        attributes = []
        attributes.append({
            'bonho': format_bonho(attr['bonho']) ,
            'mausac': format_mausac(attr['mausac']) ,
            'giagoc': format_price(option_old_price) ,
            'giamoi': format_price(option_new_price) ,
            'active': 'True'
        })
        item['thuoctinh'] = attributes
        item['tskt'] = response.css('.pd-tskt .pd-attrvalue').get()
        item['mota'] = response.css('.pd-info-left .pd-news-content').get().replace('display: none;','').replace('src','d-src').replace('data-src','src').replace('data-original','src')
        return item



class hoanghaSpider(scrapy.Spider):
    name = 'hoangha'
    start_urls = ['https://hoanghamobile.com/dien-thoai-di-dong?p=7']

    def parse(self,response):
        for product in response.css('div.list-product div.item'):   #####
            item_link = 'https://hoanghamobile.com'+ product.css('.info a::attr(href)').get()       #####
            if item_link:# == 'https://hoanghamobile.com/dien-thoai-di-dong/apple-iphone-12-pro-256gb-chinh-hang-vn-a':
                
                ten = product.css('.info a::attr(title)').get()      #####
                attr = get_attr_from_name(ten)
                ten = name_processing(ten)

                if item_link == None:
                    continue
                item = {
                    'ten': ten ,
                    'url': item_link,
                    'image': 'https://hoanghamobile.com'+product.css('.img img::attr(src)').get(), #####
                    'ngay': date.today().strftime("%Y-%m-%d"),
                    'loaisanpham':'dienthoai',
                    'thuonghieu':'apple',
                }
                yield scrapy.Request(url=item_link, meta={'item': item,'attr':attr}, callback=self.get_detail)
                #break
            
        
        #next_page = 'https://mediamart.vn/smartphones/?&trang='
        #if next_page is not None:
        #    yield response.follow(next_page,callback=self.parse)

    def get_detail(self, response):
        
        item = response.meta['item']
        attr_from_name = response.meta['attr']
        
        
        #option_new_price = response.css('.current-product-price strong::text').get()    #####   

        
        bonho_active = response.css('.product-details-container .product-option.version .options .item.selected strong::text').get()
        color_active = response.css('.product-details-container .product-option.color .options .item.selected span strong::text').get()
        list_color = response.css('.product-details-container .product-option.color .options .item')
        print("------------attr--", attr_from_name['bonho'],attr_from_name['mausac'])
        active = 'False'
        attributes = []
        for i in list_color:
            color = i.css('span strong::text').get()
            print('+++++++',color)

            option_old_price = i.css('::attr(data-lastprice)').get()  #####
            option_new_price = i.css('::attr(data-bestprice)').get()
            
            if color == color_active:
                active = 'True'
            else:
                active = 'False'
            
            
            attributes.append({
                'bonho': format_bonho(bonho_active) ,
                'mausac': format_mausac(color) ,
                'giagoc': format_price(option_old_price) ,
                'giamoi': format_price(option_new_price) ,
                'active': active
            })
        item['thuoctinh'] = attributes
        item['tskt'] = response.css('.product-layout .specs-special').get()
        item['mota'] = response.css('.product-layout .product-text').get().replace('display: none;','').replace('src="','src="https://hoanghamobile.com')
        return item


class didongmangoSpider(scrapy.Spider):
    name = 'didongmango'
    start_urls = ['https://didongmango.com/dien-thoai-pc58.html']

    def parse(self,response):
        for product in response.css('.products-cat-frame .product_grid .item'):   #####
            item_link = product.css('.product_image a::attr(href)').get()       #####
            if item_link:# == 'https://hoanghamobile.com/dien-thoai-di-dong/apple-iphone-12-pro-256gb-chinh-hang-vn-a':
                
                ten = product.css('h3 a::text').get()      #####
                attr = get_attr_from_name(ten)
                ten = name_processing(ten)

                if item_link == None:
                    continue
                item = {
                    'ten': ten ,
                    'url': item_link,
                    'image': product.css('.product_image img::attr(src)').get(), #####
                    'ngay': date.today().strftime("%Y-%m-%d"),
                    'loaisanpham':'dienthoai',
                    'thuonghieu':'apple',
                }
                yield scrapy.Request(url=item_link, meta={'item': item,'attr':attr}, callback=self.get_detail)
                #break
            
        
        next_page = 'https://didongmango.com' + response.css('.pagination a.next-page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)

    def get_detail(self, response):
        
        item = response.meta['item']
        attr_from_name = response.meta['attr']
        
        
        #option_new_price = response.css('.current-product-price strong::text').get()    #####   

        
        bonho_active = attr_from_name['bonho']
        color_active = response.css('.product_base ._color a.active .color_name::text').get()
        list_color = response.css('.product_base ._color a')
        print("------------attr--", attr_from_name['bonho'],attr_from_name['mausac'])
        active = 'False'
        option_old_price = response.css('.product_base .price .price_old::text').get()

        attributes = []
        for i in list_color:
            color = i.css('span.color_name::text').get()
            print('+++++++',color)

            option_new_price = i.css('span.price_follow_color::text').get()  #####
            
            if color == color_active:
                active = 'True'
            else:
                active = 'False'
            
            
            attributes.append({
                'bonho': format_bonho(bonho_active) ,
                'mausac': format_mausac(color) ,
                'giagoc': format_price(option_old_price) ,
                'giamoi': format_price(option_new_price) ,
                'active': active
            })
        item['thuoctinh'] = attributes
        item['tskt'] = response.css('.product table.charactestic_table').get()
        item['mota'] = response.css('.product .product_tab_content .box_conten_linfo_inner').get().replace('display: none;','').replace('src','d-src').replace('data-src','src').replace('data-origin','src')
        return item


class didonghanhphucSpider(scrapy.Spider):
    name = 'didonghanhphuc'
    start_urls = ['https://didonghanhphuc.vn/collections/dien-thoai']

    def parse(self,response):
        for product in response.css('.collection-body .product-item'):   #####
            item_link = 'https://didonghanhphuc.vn' + product.css('.product-title a::attr(href)').get()       #####
            if item_link:# == 'https://hoanghamobile.com/dien-thoai-di-dong/apple-iphone-12-pro-256gb-chinh-hang-vn-a':
                
                ten = product.css('.product-title a::text').get()      #####
                attr = get_attr_from_name(ten)
                ten = name_processing(ten)

                if item_link == None:
                    continue
                item = {
                    'ten': ten ,
                    'url': item_link,
                    'image': 'https://didonghanhphuc.vn' + product.css('.product-img img::attr(src)').get(), #####
                    'ngay': date.today().strftime("%Y-%m-%d"),
                    'loaisanpham':'dienthoai',
                    'thuonghieu':'apple',
                }
                yield scrapy.Request(url=item_link, meta={'item': item,'attr':attr}, callback=self.get_detail)
                #break
            
        
        next_page = 'https://didonghanhphuc.vn' + response.css('.pagination span.nextPage a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)

    def get_detail(self, response):
        
        item = response.meta['item']
        attr_from_name = response.meta['attr']
        
        
        #option_new_price = response.css('.current-product-price strong::text').get()    #####   

        
        bonho_active = attr_from_name['bonho']

        color_active = response.css('.select-swatch .swatch-product-single .select-swap .swatch-element.color label span::text').get()

        #list_color = response.css('.product_base ._color a')
        print("------------attr--", attr_from_name['bonho'],attr_from_name['mausac'])
        
        option_old_price = response.css('.product-content .original-price s::text').get()

        attributes = []

        option_new_price = response.css('.product-content .current-price::text').get()  #####

            
            
        attributes.append({
            'bonho': format_bonho(bonho_active) ,
            'mausac': format_mausac(color_active) ,
            'giagoc': format_price(option_old_price) ,
            'giamoi': format_price(option_new_price) ,
            'active': 'True'
        })
        item['thuoctinh'] = attributes
        item['tskt'] = response.css('.tskt table').get()
        item['mota'] = response.css('.pdTabs .pro-tabcontent').get().replace('display: none;','').replace('src','d-src').replace('data-src','src').replace('data-origin','src')
        return item

class didongmogiSpider(scrapy.Spider):
    name = 'didongmogi'
    start_urls = ['https://didongmogi.com/danh-muc-san-pham/dien-thoai/']

    def parse(self,response):
        for product in response.css('.products .product'):   #####
            item_link = product.css('p.name.product-title a::attr(href)').get()       #####
            if item_link:# == 'https://hoanghamobile.com/dien-thoai-di-dong/apple-iphone-12-pro-256gb-chinh-hang-vn-a':
                
                ten = product.css('p.name.product-title a::text').get()      #####
                attr = get_attr_from_name(ten)
                ten = name_processing(ten)

                if item_link == None:
                    continue
                item = {
                    'ten': ten ,
                    'url': item_link,
                    'image':  product.css('.box-image img::attr(src)').get(), #####
                    'ngay': date.today().strftime("%Y-%m-%d"),
                    'loaisanpham':'dienthoai',
                    'thuonghieu':'apple',
                }
                yield scrapy.Request(url=item_link, meta={'item': item,'attr':attr}, callback=self.get_detail)
                #break
            
        
        next_page = response.css('ul.page-numbers a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)

    def get_detail(self, response):
        
        item = response.meta['item']
        attr_from_name = response.meta['attr']
        
        option_old_price = response.css('.price.product-page-price del span.amount::text').get()

        attributes = []

        option_new_price = response.css('.price.product-page-price ins span.amount::text').get()  #####
    
        attributes.append({
            'bonho': format_bonho(attr_from_name['bonho']) ,
            'mausac': format_mausac(attr_from_name['mausac']) ,
            'giagoc': format_price(option_old_price) ,
            'giamoi': format_price(option_new_price) ,
            'active': 'True'
        })
        item['thuoctinh'] = attributes
        item['tskt'] = response.css('.product-short-description').get()    
        item['mota'] = response.css('.boxArticle article').get()
        return item

class galaxydidongSpider(scrapy.Spider):
    name = 'galaxydidong'
    start_urls = ['https://galaxydidong.vn/']

    def parse(self,response):
        for product in response.css('.motsanpham'):   #####
            item_link = product.css('.tieude-sanpham a::attr(href)').get()       #####
            if item_link:# == 'https://hoanghamobile.com/dien-thoai-di-dong/apple-iphone-12-pro-256gb-chinh-hang-vn-a':
                
                ten = product.css('.tieude-sanpham a::text').get()      #####
                attr = get_attr_from_name(ten)
                ten = name_processing(ten)

                if item_link == None:
                    continue
                item = {
                    'ten': ten ,
                    'url': item_link,
                    'image': product.css('.anhsanpham img::attr(style)').get().replace('background-image: url(','').replace(')',''), #####
                    'ngay': date.today().strftime("%Y-%m-%d"),
                    'loaisanpham':'dienthoai',
                    'thuonghieu':'apple',
                }
                yield scrapy.Request(url=item_link, meta={'item': item,'attr':attr}, callback=self.get_detail)
                #break
            
        
        #next_page = 'https://didongmango.com' + response.css('.pagination a.next-page::attr(href)').get()
        #if next_page is not None:
        #    yield response.follow(next_page,callback=self.parse)

    def get_detail(self, response):
        
        item = response.meta['item']
        attr_from_name = response.meta['attr']
        
        #option_new_price = response.css('.current-product-price strong::text').get()    #####   
        
        bonho_active = attr_from_name['bonho']
        color_active = response.css('.detail-product .detail-main .detail-product-right .choose-color ul li.active div.variable-wrap::text')[1].get()
        list_color = response.css('.detail-product .detail-main .detail-product-right .choose-color ul li')
        print("------------attr--", attr_from_name['bonho'],attr_from_name['mausac'])
        active = 'False'
        
        option_old_price = 'None'

        attributes = []
        for i in list_color:
            color = i.css(' div.variable-wrap::text')[1].get()
            print('+++++++',color)

            option_new_price = i.css(' div.variable-wrap p span::text').get()  #####
            
            if format_mausac(color) == format_mausac(color_active):
                active = 'True'
            else:
                active = 'False'
            
            attributes.append({
                'bonho': format_bonho(bonho_active) ,
                'mausac': format_mausac(color) ,
                'giagoc': format_price(option_old_price) ,
                'giamoi': format_price(option_new_price) ,
                'active': active
            })
        item['thuoctinh'] = attributes
        item['tskt'] = response.css('.feature-item table').get()
        item['mota'] = response.css('.description-content').get().replace('display: none;','').replace('src','d-src').replace('data-src','src').replace('data-origin','src')
        return item


class dienthoaigiasocSpider(scrapy.Spider):
    name = 'dienthoaigiasoc'
    start_urls = [
        'https://dienthoaigiasoc.vn/danh-muc/apple-iphone/',
        'https://dienthoaigiasoc.vn/danh-muc/samsung-galaxy-chinh-hang/',
        'https://dienthoaigiasoc.vn/danh-muc/oppo/',
        'https://dienthoaigiasoc.vn/danh-muc/xiaomi/',
        'https://dienthoaigiasoc.vn/danh-muc/dien-thoai-khac-realme-xiaomi-nokia-vsmart/',
    ]

    def parse(self,response):
        for product in response.css('div.full-section .item-st3'):   #####
            item_link = product.css('h4.name-item-st3 a::attr(href)').get()       #####
            if item_link:# == 'https://hoanghamobile.com/dien-thoai-di-dong/apple-iphone-12-pro-256gb-chinh-hang-vn-a':
                
                ten = product.css('h4.name-item-st3 a::text').get()      #####
                attr = get_attr_from_name(ten)
                ten = name_processing(ten)

                if item_link == None:
                    continue
                item = {
                    'ten': ten ,
                    'url': item_link,
                    'image':  product.css('.img-item-st3 img::attr(src)').get(), #####
                    'ngay': date.today().strftime("%Y-%m-%d"),
                    'loaisanpham':'dienthoai',
                    'thuonghieu':'apple',
                }
                yield scrapy.Request(url=item_link, meta={'item': item,'attr':attr}, callback=self.get_detail)
                #break
            
        
        next_page = response.css('div.nextpage li:last-child a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)

    def get_detail(self, response):
        
        item = response.meta['item']
        attr_from_name = response.meta['attr']
        
        option_old_price = response.css('.detail-product-top .price .price-old::text').get()

        attributes = []

        option_new_price = response.css('.detail-product-top .price .price-new::text').get()  #####
    
        attributes.append({
            'bonho': format_bonho(attr_from_name['bonho']) ,
            'mausac': format_mausac(attr_from_name['mausac']) ,
            'giagoc': format_price(option_old_price) ,
            'giamoi': format_price(option_new_price) ,
            'active': 'True'
        })
        item['thuoctinh'] = attributes
        item['tskt'] = response.css('.thongso').get()
        item['mota'] = response.css('.info-detail-product .des-content').get().replace('display: none;','').replace('src','d-src').replace('data-src','src').replace('data-origin','src')
        return item