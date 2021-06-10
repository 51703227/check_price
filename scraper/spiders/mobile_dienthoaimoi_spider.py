import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))

# Xử lý tên sản phẩm
# Danh sách các từ cần loại bỏ
black_list = ['Chính', 'hãng', 'I', 'VN/A', 'chính','128GB','64GB','256GB','(','Fan', 'Edition',')',
              '4GB','8GB','3GB','-','32GB','6GB','Ram','2GB','5GB','(2021)','(6GB','128GB)',
              '(Đã', 'kích', 'hoạt','hành)','Điện','thoại','2018',
              'Mi','Festival)','(Fan','Edition)','Mỹ', '(','Chưa', 'Active', ')','Mới',
             '100%','Nguyên','Seal','mới','nguyên','seal','chưa','active','Full', 'VAT','4G','Wifi',
              '-', 'Mới', '100%', 'Đã', 'kích','hoạt','ATO-','ATO', 'Quà', 'tặng', '2', 'triệu', 'đồng',
              'Hãng', '(VN/A)','100%-', 'Kích', 'Hoạt','cũ' ,'Quốc' ,'tế','quốc','Pin','pin','Tế','512GB'
              ,'siêu', 'lướt','6GB/128GB','DGW','8GB/128GB','8GB/256GB','(4G)','6GB/64GB','6GB/128GB',
              '3GB/64GB','4GB/128GB','(8GB/128GB)','(6GB/128GB)','(6GB/64GB)','3GB/32GB','2GB/32GB','4GB/64GB',
              '(8GB','siêu', 'lướt','LL/A','bản','16GB','(4G)', ' đẹp', 'như',
              '12GB/256GB','(Plus)']

# Hàm xử lý tên sản phẩm
def name_processing(name):
  unprocess_name = name.split()
  processed_name = []
  for i in unprocess_name:
    if i not in black_list:
      processed_name.append(i)
  return ' '.join(processed_name)


# Lớp crawl dữ liệu
class CellPhonesMobileSpider(scrapy.Spider):
    name = 'mobile_dienthoaimoi'
    start_urls = ['https://dienthoaimoi.vn/dien-thoai-pc135.html', ]

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.products-cat > section > div > div > div.item.cls')

        self.log('products ' + str(len(products)))
        for product in products:

            title = name_processing(product.css('div.frame_inner > h2 > a::text').get())
            item_link = product.css('div.frame_inner > figure > a::attr(href)').get()
            thuong_hieu = item_link.split('/')[3].split('-')[0]
            image1 = product.css('div.frame_inner > figure > a > img::attr(src)').get()

            item = {
                'ten': title,
                'url': item_link,
                'image': image1,
                'ngay': date.today().strftime("%Y/%m/%d"),
                'loaisanpham': 'dienthoai',
                'thuonghieu': thuong_hieu
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)


        next_page_url = response.css('div.products-cat > div.pagination > a.next-page::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = response.css('div.frame_center > div > div.price.cls > div.price_current::text').get().replace('\t','').replace('\r','').replace('\n','')
        option_rom = response.css('div._attributes.clearfix.cls > ul > li > a.active::text').get().replace('\t','').replace('\r','').replace('\n','')

        option_color = response.css('div.box_price > div > div > a.Selector.active::attr(data-name)').get()
        option_new_price = option_old_price
        active = True

        # image2 = response.css('div.frame_img > div > div.magic_zoom_area > a::attr(href)').get()

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