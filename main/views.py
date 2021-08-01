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
                except MultipleObjectsReturned:
                    thuoc_tinh_active = ThuocTinh.objects.filter(Url = url_input,Active = "True")[1]
                list_thuoc_tinh_url = ThuocTinh.objects.filter( SanPham = url_input.SanPham,NguonBan = url_input.NguonBan)
            except Url.DoesNotExist:
                return render(request,'pages/404.html',{'type':'Url','data':url})
            
            list_sp_chung_nb = []
            list_url_chung_nb = Url.objects.filter(NguonBan = url_input.NguonBan)
            list_sp_chung_nb = list_url_chung_nb[0:8]
            
            danhmuc ={
                
            }
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
                'danhmuc':danhmuc,
                'form': form
            }
            
            return render(request,'pages/getattrib.html',{'data':data})
    else:
        url = request.GET.get('url', None)
        print(url)
        form = GetUrlForm()
        product_feature = SanPham.objects.filter(TenSP__icontains = 'Iphone 12')
        product_feature = product_feature[0:4]
        list_nguon_ban = NguonBan.objects.filter()
        data = {
            'form':form,
            'product_feature':product_feature,
            'list_nguon_ban':list_nguon_ban,
        }   
    return render(request, 'pages/geturl.html',data)

def category(request,cat):
    loaisp = LoaiSanPham.objects.get(TenLoai =cat)
    search_result = SanPham.objects.filter(LoaiSanPham=loaisp)  
    data = []
    for san_pham in search_result:      
        list_url = Url.objects.filter(SanPham = san_pham)
        list_nguon_ban = []

        for each_url in list_url:
            if each_url.NguonBan not in list_nguon_ban:
                list_nguon_ban.append(NguonBan.objects.get(pk = each_url.NguonBan.pk))
            else:
                continue
        
        data.append({
            'san_pham': san_pham,
            'list_nguon_ban':list_nguon_ban,
            'length_list_nguon_ban': len(list_nguon_ban)
        })

    return render(request,'pages/search-result.html',{'list_san_pham':data,'keyword':url})    
    
def xu_ly_url(request,url):

    if not url:
        return JsonResponse({'error': 'Missing  args'})
    if not is_valid_url(url):
        #return JsonResponse({'error': 'URL is invalid'})
        search_result = SanPham.objects.filter(TenSP__icontains=url)  
        data = []
        for san_pham in search_result:      #----1  

            list_url = Url.objects.filter(SanPham = san_pham)

            #for each_url in list_url:
            #    if is_valid_url(each_url.UrlImage):
            #        san_pham_img = each_url.UrlImage
            #        break

            list_nguon_ban = []
            #list_thuoc_tinh = []
            for each_url in list_url:
                if each_url.NguonBan not in list_nguon_ban:
                    list_nguon_ban.append(NguonBan.objects.get(pk = each_url.NguonBan.pk))
                else:
                    continue
            
            data.append({
                'san_pham': san_pham,
            #    'san_pham_img': san_pham_img,
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
    
    return render(request,'pages/getattrib.html',{'data':data})

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
        
        bonho = request.POST.get('bonho', None)
        
        url_in = request.POST.get('url', None)
    
        nguon_ban = request.POST.get('nguon_ban',None)
        san_pham = request.POST.get('san_pham',None)

        data = exporturl(url_in = url_in,mausac = mausac,bonho =bonho, nguon_ban=nguon_ban,san_pham=san_pham) #truy xuất database #
        
        if data == False:
            return HttpResponse("Không tìm thấy url")
        elif data == 'TT False':
            return render(request,'pages/404.html',{'type':'Thuộc tính'})
        else:
            return render(request,'pages/printurl.html',{'data':data})
    return redirect('url_input')



def exporturl(url_in,mausac,bonho,**kwargs):     #Lấy dữ liệu trong database dựa vào thông tin đầu vào
  
    def checktrungthuc(list_gia_goc):
        r = 0
        
        for gia_goc in list_gia_goc:
            if gia_goc  == 0:
                list_gia_goc.remove(gia_goc)
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
            print('++',type(mausac),bonho)
            if mausac == '' and bonho == '':
                print('sometj')
                thuoc_tinh_urlin = ThuocTinh.objects.filter(SanPham = san_pham, NguonBan = nguon_ban).first() 
            else:
                thuoc_tinh_urlin = ThuocTinh.objects.filter(MauSac=mausac,BoNho=bonho,SanPham = san_pham, NguonBan = nguon_ban).first()
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
        if thuoc_tinh_urlin.GiaGoc1 == 0 or thuoc_tinh_urlin.GiaGoc1 == None:
            saleoff = 0
        else:
            saleoff = (thuoc_tinh_urlin.GiaMoi1 / thuoc_tinh_urlin.GiaGoc1)*100
        
        if mausac == ('None' or None ) and bonho == ('None' or None):
            list_thuoc_tinh_url = ThuocTinh.objects.filter(SanPham = san_pham) #list thuộc tính các sản phẩm giống input
        elif mausac==('None' or None ):
            list_thuoc_tinh_url = ThuocTinh.objects.filter(SanPham = san_pham).filter(BoNho = bonho) #list thuộc tính các sản phẩm giống input
        elif bonho == ('None' or None ):
            list_thuoc_tinh_url = ThuocTinh.objects.filter(SanPham = san_pham).filter(MauSac = mausac) #list thuộc tính các sản phẩm giống input
        else:
            list_thuoc_tinh_url = ThuocTinh.objects.filter(SanPham = san_pham).filter(MauSac = mausac).filter(BoNho = bonho) #list thuộc tính các sản phẩm giống input
        
        

        list_gia_moi_1 = []
        list_gia_goc_1 = []
        for each_thuoc_tinh in list_thuoc_tinh_url:
            if each_thuoc_tinh.GiaGoc1 != 0 and each_thuoc_tinh.GiaGoc1 !=None:
                list_gia_goc_1.append(each_thuoc_tinh.GiaGoc1)
            if each_thuoc_tinh.GiaMoi1 != 0 and each_thuoc_tinh.GiaMoi1 !=None:
                list_gia_moi_1.append(each_thuoc_tinh.GiaMoi1)
        if len(list_gia_goc_1) == 0:
            giagoctrungbinh1 =0
            cl_giagoctrungbinh = 100
        else:
            giagoctrungbinh1 = sum(list_gia_goc_1)/len(list_gia_goc_1)
            cl_giagoctrungbinh = (thuoc_tinh_urlin.GiaGoc1 / giagoctrungbinh1 ) *100

        if len(list_gia_moi_1)==0:
            giamoitrungbinh1=0
            cl_giamoitrungbinh = 100
        else:
            giamoitrungbinh1 = sum(list_gia_moi_1)/len(list_gia_moi_1)
            cl_giamoitrungbinh = (thuoc_tinh_urlin.GiaMoi1 / giamoitrungbinh1 ) *100




        list_gia_moi_2 = []
        list_gia_goc_2 = []
        for each_thuoc_tinh in list_thuoc_tinh_url:
            if each_thuoc_tinh.GiaGoc2 != 0 and each_thuoc_tinh.GiaGoc2 !=None:
                list_gia_goc_2.append(each_thuoc_tinh.GiaGoc2)
            if each_thuoc_tinh.GiaMoi2 != 0 and each_thuoc_tinh.GiaMoi2 !=None:
                list_gia_moi_2.append(each_thuoc_tinh.GiaMoi2)
        if len(list_gia_moi_2) == 0:
            giamoitrungbinh2 =0
        else:
            giamoitrungbinh2 = sum(list_gia_moi_2)/len(list_gia_moi_2)
        

        list_gia_moi_3 = []
        list_gia_goc_3 = []
        for each_thuoc_tinh in list_thuoc_tinh_url:
            if each_thuoc_tinh.GiaGoc3 != 0 and each_thuoc_tinh.GiaGoc3 !=None:
                list_gia_goc_3.append(each_thuoc_tinh.GiaGoc3)
            if each_thuoc_tinh.GiaMoi3 != 0 and each_thuoc_tinh.GiaMoi3 !=None:
                list_gia_moi_3.append(each_thuoc_tinh.GiaMoi3) 
        if len(list_gia_moi_3) == 0:
            giamoitrungbinh3 =0
        else:
            giamoitrungbinh3 = sum(list_gia_moi_3)/len(list_gia_moi_3)

        list_gia_moi_4 = []
        list_gia_goc_4 = []
        for each_thuoc_tinh in list_thuoc_tinh_url:
            if each_thuoc_tinh.GiaGoc4 != 0 and each_thuoc_tinh.GiaGoc4 !=None:
                list_gia_goc_4.append(each_thuoc_tinh.GiaGoc4)
            if each_thuoc_tinh.GiaMoi4 != 0 and each_thuoc_tinh.GiaMoi4 !=None:
                list_gia_moi_4.append(each_thuoc_tinh.GiaMoi4) 
        if len(list_gia_moi_4) == 0:
            giamoitrungbinh4 =0
        else:
            giamoitrungbinh4 = sum(list_gia_moi_4)/len(list_gia_moi_4)

        list_gia_moi_5 = []
        list_gia_goc_5 = []
        for each_thuoc_tinh in list_thuoc_tinh_url:
            if each_thuoc_tinh.GiaGoc5 != 0 and each_thuoc_tinh.GiaGoc5 !=None:
                list_gia_goc_5.append(each_thuoc_tinh.GiaGoc5)
            if each_thuoc_tinh.GiaMoi5 != 0 and each_thuoc_tinh.GiaMoi5 !=None:
                list_gia_moi_5.append(each_thuoc_tinh.GiaMoi5) 
        if len(list_gia_moi_5) == 0:
            giamoitrungbinh5 =0
        else:
            giamoitrungbinh5 = sum(list_gia_moi_5)/len(list_gia_moi_5)

        print(giamoitrungbinh1,giamoitrungbinh2,giamoitrungbinh3,giamoitrungbinh4,giamoitrungbinh5)

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
                'giagoctrungbinh': giagoctrungbinh1,
                'giamoitrungbinh':giamoitrungbinh1,
                'cl_giagoctrungbinh': cl_giagoctrungbinh,
                'cl_giamoitrungbinh': cl_giamoitrungbinh,
                'dotrungthuc':dotrungthuc,
            },
            'giamoitrungbinh':{
                'giamoi1':giamoitrungbinh1,
                'giamoi2':giamoitrungbinh2,
                'giamoi3':giamoitrungbinh3,
                'giamoi4':giamoitrungbinh4,
                'giamoi5':giamoitrungbinh5,
            }
        } 
        return data




def import_data(request):   #Nạp data.json và database
    list_file =  [
        'xttmobile.json',
        #'aeoneshop.json',
        #'anphatpc.json',
        'cellphones.json',
        'didongmy.json',
        'didongsinhvien.json',
        'didongthongminh.json',
        'dienthoaimoi.json',
        'minhducvn.json',
        'mobileworld.json',

        'galaxydidong.json',
        'dienthoaigiasoc.json',
        'didongmango.json',
        'didongmogi.json',
        'didonghanhphuc.json',
        'mediamart.json',
        'hoangha.json',
        'hnam.json',
        'phucanh.json',
        'nguyenkim.json',
    ]
    list_file_lt = [
       'lt_24laptop.json',
        'lt_aeoneshop.json',
        'lt_ankhang.json',
        'lt_anphatpc.json',
        'lt_cellphones.json', 
        #'lt_dienmaythienhoa.json' ,
        'lt_hangchinhhieu.json',
        'lt_hanoicomputer.json',
        'lt_hnammobile.json' ,
        'lt_hoanghamobile.json' ,
        'lt_hoangphat.json' ,
        'lt_hoangphatgaming.json' ,
        'lt_hoanlong.json',
        'lt_laptop888.json',
        'lt_laptopnew.json',
        'lt_mediamart.json',
        'lt_nguyenkim.json',
        'lt_phucanh.json',
        #'lt_tmdpc.json',
        'lt_xttmobile.json',
    ]
    for ten_file in list_file:
        f = open('./data/mobile/'+ten_file,'r',encoding='utf-8')
        data = json.loads(f.read())

        for item in data:
            
            try:
                obj = SanPham.objects.get(TenSP = item['ten'])
                if item['image'] != None and item['image'] != '':
                    setattr(obj,'ImgSP',item['image'])
                    setattr(obj,'NgayKhoiTao',item['ngay'])
                obj.save()
            except SanPham.DoesNotExist:
                try:
                    obj = SanPham(
                        TenSP = item['ten'],
                        LoaiSanPham = LoaiSanPham.objects.get(TenLoai=item['loaisanpham']),
                        #ThuongHieu = ThuongHieu.objects.get(TenTH= item['thuonghieu']),
                        ImgSP = item['image'],
                        NgayKhoiTao = item['ngay']
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
                    if (gia==None) or (gia in ['liên hệ','liênhệ','Liên hệ','Liênhệ','None','none','NONE','','Hếthàng']):
                        return 0
                    else:
                        return gia.replace('.','').replace('₫','').replace('đ','').replace('vn','').replace('Đ','')
                try:
                    obj = ThuocTinh.objects.get(
                        Url=Url.objects.get(Url = item['url']), 
                        MauSac=i['mausac'] if item['loaisanpham'] == 'dienthoai' else 'None',
                        BoNho=i['bonho'] if item['loaisanpham'] == 'dienthoai' else 'None',
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
                    if item['loaisanpham'] == 'dienthoai':
                        thuoctinh.MauSac = i['mausac']#'None'#
                        thuoctinh.BoNho = i['bonho']#'None'#
                        thuoctinh.Active = i['active']#'True'#
                    else:
                        thuoctinh.MauSac = 'None'#
                        thuoctinh.BoNho = 'None'#
                        thuoctinh.Active = 'True'#
                    thuoctinh.GiaGoc1 =rp(i['giagoc'])
                    thuoctinh.GiaMoi1 =rp(i['giamoi'])
                    thuoctinh.Ngay1 = item['ngay']
                    thuoctinh.Url = Url.objects.get(Url = item['url'])
                    thuoctinh.SanPham = SanPham.objects.get(TenSP = item['ten'])
                    
                    thuoctinh.NguonBan = NguonBan.objects.get(Domain = urlparse(item['url']).netloc)

                    thuoctinh.save()

    return HttpResponse("Complete Import Data "+ str(list_file) +" <br> <a href='/'>Quay lại</a>")
        
        
        
        
        


        
        
