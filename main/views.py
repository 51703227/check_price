from os import pipe
from django.conf.urls import url
from django.db.models.fields import NullBooleanField
from django.shortcuts import render,redirect
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect 
from django.http import JsonResponse
from django.urls import reverse

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError,MultipleObjectsReturned

from urllib.parse import urlparse

import json

from .models import *

from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

from django.db import IntegrityError

# Create your views here.
def product_supplier(request,id):
    san_pham = SanPham.objects.get(pk = id)    #lấy obj sản phẩm từ request
    list_url = Url.objects.filter(SanPham = san_pham)   #lấy list url có chung sản phẩm đầu vào 
    
    data = []
    list_nguon_ban = []

    #tạo list nguồn bán 
    for each_url in list_url:
        #lọc nguồn bán
        if each_url.NguonBan not in list_nguon_ban:
            list_nguon_ban.append(NguonBan.objects.get(pk = each_url.NguonBan.pk)) 
        else:
            continue
    
    for each_nguonban in list_nguon_ban:
        #lọc url
        list_url = Url.objects.filter(SanPham = san_pham).filter(NguonBan= each_nguonban)
        min_price = 0.0
        max_price = 0.0
        for each_url in list_url:
            if is_valid_url(each_url.UrlImage):
                san_pham_img = each_url.UrlImage
                break

        for each_url in list_url:
            list_thuoc_tinh = ThuocTinh.objects.filter(Url = each_url)

            for each_thuoc_tinh in list_thuoc_tinh:
                if each_thuoc_tinh.GiaMoi1 == 0:
                    continue
                if min_price ==0.0 and max_price == 0.0:
                    min_price = each_thuoc_tinh.GiaMoi1
                    max_price = each_thuoc_tinh.GiaMoi1
                print(min_price,'+',max_price)
                if each_thuoc_tinh.GiaMoi1 < min_price:
                    min_price = each_thuoc_tinh.GiaMoi1
                if each_thuoc_tinh.GiaMoi1 > max_price:
                    max_price = each_thuoc_tinh.GiaMoi1
            
        data.append({
            'nguon_ban': each_nguonban,
            'list_url': list_url,
            'anh_san_pham': san_pham_img,
            'length_list_url': len(list_url),
            'min_price':min_price,
            'max_price':max_price ,
            'san_pham':san_pham
        })

    return render(request,'pages/product-supplier.html',{'list_nguon_ban':data,'san_pham':san_pham})

def get_attribute(request):
    if request.method == "POST":
        data_pk = request.POST.get('data_pk', None) #get data from user input
        list_pk = data_pk.split() 
        nguon_ban = NguonBan.objects.get(pk=list_pk[0]) #truy xuất URL = url đã nhập
        san_pham = SanPham.objects.get(pk=list_pk[1])
        anh_san_pham = list_pk[2]

        list_thuoc_tinh_url = ThuocTinh.objects.filter( SanPham = san_pham,NguonBan = nguon_ban)

        #tạo form nhập thuộc tính
        mausac =[]
        bonho = []

        for attr in list_thuoc_tinh_url:
            if (attr.MauSac,attr.MauSac) not in mausac:
                mausac.append((attr.MauSac,attr.MauSac))
            if (attr.BoNho,attr.BoNho) not in bonho:
                bonho.append((attr.BoNho,attr.BoNho))

        form = GetAttribForm(mausac=mausac,bonho=bonho)

        data= {
            'san_pham': san_pham,
            'nguon_ban':nguon_ban,
            'anh_san_pham': anh_san_pham,
            'form': form
        }
        
        #a = Url.objects.get(Url=url)
        return render(request,'pages/get-attribute.html',{'data':data})

def url_input(request):
    if request.method == "POST":
        form = GetUrlForm(request.POST)
        if form.is_valid():
            url = request.POST.get('url', None) #get url from user input

            if not url:
                return JsonResponse({'error': 'Missing  args'})
            if not is_valid_url(url):
                #return JsonResponse({'error': 'URL is invalid'})
                search_result = SanPham.objects.filter(TenSP__icontains=url)  
                data = []
                for san_pham in search_result:      #----1  

                    list_url = Url.objects.filter(SanPham = san_pham)

                    for each_url in list_url:
                        if is_valid_url(each_url.UrlImage):
                            san_pham_img = each_url.UrlImage
                            break
                    list_nguon_ban = []
                    #list_thuoc_tinh = []
                    for each_url in list_url:
                        if each_url.NguonBan not in list_nguon_ban:
                            list_nguon_ban.append(NguonBan.objects.get(pk = each_url.NguonBan.pk))
                        else:
                            continue
                    
                    data.append({
                        'san_pham': san_pham,
                        'san_pham_img': san_pham_img,
                        'list_nguon_ban':list_nguon_ban,
                        'length_list_nguon_ban': len(list_nguon_ban)
                    })


                return render(request,'pages/search-result.html',{'list_san_pham':data,'keyword':url})

            #truy xuất thuộc tính url
            try:
                url_input = Url.objects.get(Url=url) #truy xuất URL = url đã nhập
                try:
                    thuoc_tinh_active = ThuocTinh.objects.get(Url = url_input,Active = "True")
                except ThuocTinh.DoesNotExist:
                    thuoc_tinh_active = ThuocTinh.objects.filter(Url = url_input).first()
                list_thuoc_tinh_url = ThuocTinh.objects.filter( SanPham = url_input.SanPham,NguonBan = url_input.NguonBan)
            except Url.DoesNotExist:
                return render(request,'pages/404.html',{'type':'Url','data':url})
            
            list_sp_chung_nb = []
            list_url_chung_nb = Url.objects.filter(NguonBan = url_input.NguonBan)
            list_sp_chung_nb = list_url_chung_nb[0:8]
            
            print(list_sp_chung_nb)
            #tạo form nhập thuộc tính
            mausac =[]
            bonho = []

            for attr in list_thuoc_tinh_url:
                if (attr.MauSac,attr.MauSac) not in mausac:
                    mausac.append((attr.MauSac,attr.MauSac))
                if (attr.BoNho,attr.BoNho) not in bonho:
                    bonho.append((attr.BoNho,attr.BoNho))

            form = GetAttribForm(mausac=mausac,bonho=bonho)

            data= {
                'url_in': url_input,
                'thuoc_tinh_active':thuoc_tinh_active,
                'list_sp_chung_nb':list_sp_chung_nb,
                'form': form
            }
            
            #a = Url.objects.get(Url=url)
            return render(request,'pages/getattrib.html',{'data':data})
            #return redirect(getattrib)
            #return HttpResponseRedirect('/print_url',url)
    else:
        form = GetUrlForm()
        product_feature = SanPham.objects.filter(TenSP__icontains = 'Iphone 12')
        product_feature = product_feature[0:4]
        data = {
            'form':form,
            'product_feature':product_feature
        }   
    return render(request, 'pages/geturl.html',data)

def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url) # check if url format is valid
    except ValidationError:
        return False

    return True

def print_url(request):
    if request.method == "POST":
        #form = GetAttribForm(request.POST)
        #if form.is_valid():

        #lấy các thuộc tính của sản phẩm từ người dùng
        mausac = request.POST.get('mausac', None)
        print(mausac) 
        bonho = request.POST.get('bonho', None)
        print(bonho)
        url_in = request.POST.get('url', None)
    
        nguon_ban = request.POST.get('nguon_ban',None)
        san_pham = request.POST.get('san_pham',None)

        data = exporturl(url_in = url_in,mausac = mausac,bonho =bonho, nguon_ban=nguon_ban,san_pham=san_pham) #truy xuất database #
        print(data)
        if data == False:
            return HttpResponse("Không tìm thấy url")
        elif data == 'TT False':
            return render(request,'pages/404.html',{'type':'Thuộc tính'})
        else:
            print(data)
            return render(request,'pages/printurl.html',{'data':data})

    else:
        list_attr = [
        ]
        form = GetAttribForm(list_attr)


def exporturl(url_in,mausac,bonho,**kwargs):     #Lấy dữ liệu trong database dựa vào thông tin đầu vào
  
    def checktrungthuc(list_gia_goc):
        r = 0
        for gia_goc in list_gia_goc:
            if gia_goc  == 0:
                list_gia_goc.remove(gia_goc)
        for gia_goc in list_gia_goc:        
            if list_gia_goc[0] <= gia_goc:
                r = r+1
        return (r/len(list_gia_goc))*100

    if url_in == None:
        nguon_ban = NguonBan.objects.get(pk = kwargs['nguon_ban'])
        san_pham = SanPham.objects.get(pk =kwargs['san_pham'])
        try:
            thuoc_tinh_urlin = ThuocTinh.objects.get(MauSac=mausac,BoNho=bonho,SanPham = san_pham, NguonBan = nguon_ban)
        except ThuocTinh.DoesNotExist:
            return 'TT False'        
    else:
        try:
            url = Url.objects.get(Url=url_in)
            
            try: 
                thuoc_tinh_urlin = ThuocTinh.objects.get(Url=url,MauSac=mausac,BoNho=bonho)
            except ThuocTinh.DoesNotExist:
                    if mausac == 'None' and bonho == 'None':
                        thuoc_tinh_urlin = ThuocTinh.objects.get(Url=url,Active="True")
                    elif mausac=='None':
                        thuoc_tinh_urlin = ThuocTinh.objects.get(Url=url,BoNho=bonho)
                    elif bonho == 'None':
                        thuoc_tinh_urlin = ThuocTinh.objects.get(Url=url,MauSac=mausac)
                    else:
                        try:
                            thuoc_tinh_urlin = ThuocTinh.objects.get(MauSac=mausac,BoNho=bonho,SanPham = url.SanPham, NguonBan = url.NguonBan)
                        except ThuocTinh.DoesNotExist:
                            return 'TT False'
            san_pham = SanPham.objects.get(TenSP__exact = url.SanPham.TenSP) #select Sản phẩm của url
        except Url.DoesNotExist:
            return False

    if  thuoc_tinh_urlin!=None:
        saleoff = (thuoc_tinh_urlin.GiaMoi1 / thuoc_tinh_urlin.GiaGoc1)*100
        
        

        if mausac == 'None' and bonho == 'None':
            list_thuoc_tinh_url = ThuocTinh.objects.filter(SanPham = san_pham) #list thuộc tính các sản phẩm giống input
        elif mausac=='None':
            list_thuoc_tinh_url = ThuocTinh.objects.filter(SanPham = san_pham).filter(BoNho = bonho) #list thuộc tính các sản phẩm giống input
        elif bonho == 'None':
            list_thuoc_tinh_url = ThuocTinh.objects.filter(SanPham = san_pham).filter(MauSac = mausac) #list thuộc tính các sản phẩm giống input
        else:
            list_thuoc_tinh_url = ThuocTinh.objects.filter(SanPham = san_pham).filter(MauSac = mausac).filter(BoNho = bonho) #list thuộc tính các sản phẩm giống input
        
        list_gia_moi_1 = []
        list_gia_goc_1 = []
        for each_thuoc_tinh in list_thuoc_tinh_url:
            if each_thuoc_tinh.GiaGoc1 != 0 and each_thuoc_tinh.GiaGoc1 !=None and each_thuoc_tinh.GiaMoi1 != 0 and each_thuoc_tinh.GiaMoi1 !=None:
                list_gia_goc_1.append(each_thuoc_tinh.GiaGoc1)
                list_gia_moi_1.append(each_thuoc_tinh.GiaMoi1) 

        giagoctrungbinh = (thuoc_tinh_urlin.GiaGoc1 / (sum(list_gia_goc_1)/len(list_gia_goc_1)) ) *100
        giamoitrungbinh = (thuoc_tinh_urlin.GiaMoi1 / (sum(list_gia_moi_1)/len(list_gia_moi_1)) ) *100

        list_gia_goc = [thuoc_tinh_urlin.GiaGoc1,thuoc_tinh_urlin.GiaGoc2,thuoc_tinh_urlin.GiaGoc3,thuoc_tinh_urlin.GiaGoc4,thuoc_tinh_urlin.GiaGoc5]
        dotrungthuc = checktrungthuc(list_gia_goc)


        list_url_chung_nb =[]
        if url_in == None:
            list_url_chung_nb = Url.objects.filter(NguonBan = nguon_ban)
            list_url_chung_nb = list_url_chung_nb[0:5]
        else:
            list_url_chung_nb = Url.objects.filter(NguonBan = url.NguonBan)
            list_url_chung_nb = list_url_chung_nb[0:5]
        
        #lưu dữ liệu truy xuất và data
        data = {
            #'product': product, #obj
            'thuoc_tinh_urlin': thuoc_tinh_urlin, #obj
            'thuoc_tinh_urlout': list_thuoc_tinh_url,
            'list_url_chung_nb':list_url_chung_nb,
            'analytics':{
                'saleoff':round(saleoff,2),
                'giagoctrungbinh': giagoctrungbinh,
                'giamoitrungbinh':giamoitrungbinh,
                'dotrungthuc':dotrungthuc,
            }
        } 
        return data
    else:
        return False






def import_data(request):   #Nạp data.json và database
    list_file =  [
        #'mediamart.json',
        #'hnam.json',
        #'phucanh.json',
        #'nguyenkim.json',
        #'hoangha.json',
        #'galaxydidong.json',
        #'dienthoaigiasoc.json',
        #'didongmango.json',
        #'didongmogi.json',
        #'didonghanhphuc.json',

        'xtmobile.json',
        'aeoneshop.json',
        'anphatpc.json',
        'cellphones.json',
        'didongmy.json',
        'didongsinhvien.json',
        'didongthongminh.json',
        'dienthoaimoi.json',
        'minhducvn.json',
        'mobileworld.json'
    ]
    for ten_file in list_file:
        f = open('./data/mobile/'+ten_file,'r',encoding='utf-8')
        data = json.loads(f.read())

        for item in data:
            
            try:
                obj = SanPham.objects.get(TenSP = item['ten'])
            except SanPham.DoesNotExist:
                try:
                    obj = SanPham(
                        TenSP = item['ten'],
                        LoaiSanPham = LoaiSanPham.objects.get(TenLoai=item['loaisanpham']),
                        ThuongHieu = ThuongHieu.objects.get(TenTH= item['thuonghieu']),
                        ImgSP = item['image']
                    )
                    obj.save()
                except ThuongHieu.DoesNotExist:
                    obj = SanPham(
                        TenSP = item['ten'],
                        LoaiSanPham = LoaiSanPham.objects.get(TenLoai=item['loaisanpham']),
                        
                        ImgSP = item['image']
                    )
                    obj.save()
            except MultipleObjectsReturned:
                return HttpResponse('Sản phẩm bị trùng lặp: ',item['ten']) 
            
            try:
                obj = Url.objects.get(Url = item['url'])
                setattr(obj,'SanPham',SanPham.objects.get(TenSP=item['ten']))
                setattr(obj,'NguonBan',NguonBan.objects.get(Domain = urlparse(item['url']).netloc))
                setattr(obj,'UrlImage',item['image'])
                setattr(obj,'Tskt',item['tskt'])
                setattr(obj,'MoTa',item['mota'])
                obj.save()
            except Url.DoesNotExist:
                obj = Url(
                    Url = item['url'],
                    SanPham = SanPham.objects.get(TenSP=item['ten']) ,
                    NguonBan = NguonBan.objects.get(Domain = urlparse(item['url']).netloc),
                    UrlImage = item['image'],
                    Tskt = item['tskt'],
                    MoTa = item['mota']
                )
                obj.save()         
            
            for i in item['thuoctinh']:
                def rp(gia):
                    if (gia==None) or (gia in ['liên hệ','liênhệ','Liên hệ','Liênhệ','None','none','NONE','']):
                        return 0
                    else:
                        return gia.replace('.','').replace('₫','').replace('đ','')
                try:
                    obj = ThuocTinh.objects.get(
                        Url=Url.objects.get(Url = item['url']), 
                        MauSac=i['mausac'],
                        BoNho=i['bonho'],
                        NguonBan = NguonBan.objects.get(Domain = urlparse(item['url']).netloc),
                        SanPham = SanPham.objects.get(TenSP=item['ten'])
                    )
                    obj.Ngay5 = obj.Ngay4
                    obj.Ngay4 = obj.Ngay3
                    obj.Ngay3 = obj.Ngay2
                    obj.Ngay2 = obj.Ngay1
                    obj.Ngay1 = item['ngay']

                    obj.GiaGoc5 = obj.GiaGoc4
                    obj.GiaGoc4 = obj.GiaGoc3
                    obj.GiaGoc3 = obj.GiaGoc2
                    obj.GiaGoc2 = obj.GiaGoc1
                    obj.GiaGoc1 = rp(i['giagoc'])  #0 if i['giagoc']==None else i['giamoi'].replace('.','').replace('₫','')

                    obj.GiaMoi5 = obj.GiaMoi4
                    obj.GiaMoi4 = obj.GiaMoi3
                    obj.GiaMoi3 = obj.GiaMoi2
                    obj.GiaMoi2 = obj.GiaMoi1
                    obj.GiaMoi1 = rp(i['giamoi'])  #0 if i['giamoi']==None else i['giamoi'].replace('.','').replace('₫','')
                    
                    obj.save()

                except ThuocTinh.DoesNotExist:      
                    thuoctinh = ThuocTinh()

                    thuoctinh.MauSac = i['mausac']
                    thuoctinh.BoNho = i['bonho']
                    thuoctinh.GiaGoc1 =rp(i['giagoc'])
                    thuoctinh.GiaMoi1 =rp(i['giamoi'])
                    thuoctinh.Ngay1 = item['ngay']
                    thuoctinh.Url = Url.objects.get(Url = item['url'])
                    thuoctinh.SanPham = SanPham.objects.get(TenSP = item['ten'])
                    thuoctinh.Active = i['active']
                    thuoctinh.NguonBan = NguonBan.objects.get(Domain = urlparse(item['url']).netloc)

                    thuoctinh.save()

    return HttpResponse("Complete Import Data "+ str(list_file) +" <br> <a href='/'>Quay lại</a>")
        
        
        
        
        


        
        
