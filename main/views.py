from os import pipe
from django.db.models.fields import NullBooleanField
from django.shortcuts import render,redirect
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect 
from django.http import JsonResponse
from django.urls import reverse

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from urllib.parse import urlparse

import json

from .models import *

from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

# Create your views here.

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
                for item in search_result:
                    print(item.TenSP)
            
            domain = urlparse(url).netloc #take netloc from urlparse to get domain
            print(domain)
            #truy xuất thuộc tính url
            url_input = Url.objects.get(Url=url) #truy xuất URL = url đã nhập
            thuoc_tinh_active = ThuocTinh.objects.get(Url = url_input,Active = "True")
            list_thuoc_tinh_url = ThuocTinh.objects.filter( Url = url_input)

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
                'form': form
            }
            print(data)
            #a = Url.objects.get(Url=url)
            return render(request,'pages/getattrib.html',{'data':data})
            #return redirect(getattrib)
            #return HttpResponseRedirect('/print_url',url)
    else:
        form = GetUrlForm()

    return render(request, 'pages/geturl.html',{'form':form})

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

        data = exporturl(url_in = url_in,mausac = mausac,bonho =bonho) #truy xuất database #
        if data == False:
            return HttpResponse("Không tìm thấy url")
        else:
            print(data)
            return render(request,'pages/printurl.html',{'data':data})

    else:
        list_attr = [
        ]
        form = GetAttribForm(list_attr)


def exporturl(url_in,mausac,bonho):     #Lấy dữ liệu trong database dựa vào thông tin đầu vào
    try:
        url = Url.objects.get(Url=url_in)
        try:
            thuoc_tinh_urlin = ThuocTinh.objects.get(Url=url,MauSac=mausac,BoNho=bonho)
        except ThuocTinh.DoesNotExist:
            print("ko có thuộc tính")
            thuoc_tinh_urlin = None
        sanpham = SanPham.objects.get(TenSP__exact = url.SanPham.TenSP) #select Sản phẩm của url
    except Url.DoesNotExist:
        url = None

    if url != None and thuoc_tinh_urlin!=None:
        saleoff = (thuoc_tinh_urlin.GiaGoc1 / thuoc_tinh_urlin.GiaMoi1)*100
        giagoctrungbinh = (thuoc_tinh_urlin.GiaGoc1 +thuoc_tinh_urlin.GiaGoc2 +thuoc_tinh_urlin.GiaGoc3 +thuoc_tinh_urlin.GiaGoc4 +thuoc_tinh_urlin.GiaGoc5 )/5
        giakhuyenmaitrungbinh = (thuoc_tinh_urlin.GiaMoi1 +thuoc_tinh_urlin.GiaMoi2 +thuoc_tinh_urlin.GiaMoi3 +thuoc_tinh_urlin.GiaMoi4 +thuoc_tinh_urlin.GiaMoi5 )/5
        dotrungthuc = 80

        list_thuoc_tinh_url = ThuocTinh.objects.filter(SanPham = sanpham).filter(MauSac = mausac).filter(BoNho = bonho) #list thuộc tính các sản phẩm giống input
        #lưu dữ liệu truy xuất và data
        data = {
            #'product': product, #obj
            'thuoc_tinh_urlin': thuoc_tinh_urlin, #obj
            'thuoc_tinh_urlout': list_thuoc_tinh_url,
            'analytics':{
                'saleoff':round(saleoff,2),
                'giagoctrungbinh': "{:,.2f} VNĐ".format(giagoctrungbinh),
                'giakhuyenmaitrungbinh':"{:,.2f} VNĐ".format(giakhuyenmaitrungbinh),
                'dotrungthuc':dotrungthuc,
            }
        } 
        return data
    else:
        return False

def import_data(request):   #Nạp data.json và database

    f = open('mobile_cellphones_data.json','r',encoding='utf-8')
    data = json.loads(f.read())

    for item in data:
        try:
            SanPham.objects.update_or_create(
                TenSP = item['ten'],
                LoaiSanPham = LoaiSanPham.objects.get(TenLoai=item['loaisanpham']),
                ThuongHieu = ThuongHieu.objects.get(TenTH= item['thuonghieu'])
            )
        except ThuongHieu.DoesNotExist:
            SanPham.objects.update_or_create(
                TenSP = item['ten'],
                LoaiSanPham = LoaiSanPham.objects.get(TenLoai=item['loaisanpham']),
                ThuongHieu = ThuongHieu.objects.create(TenTH=item['thuonghieu'])
            )
        try:
            Url.objects.update_or_create(
                Url = item['url'],
                SanPham = SanPham.objects.get(TenSP=item['ten']) ,
                NguonBan = NguonBan.objects.get(Domain = urlparse(item['url']).netloc),
                UrlImage = item['image']
            )
        except NguonBan.DoesNotExist:
            Url.objects.update_or_create(
                Url = item['url'],
                SanPham = SanPham.objects.get(TenSP=item['ten']) ,
                UrlImage = item['image']
            )            
        
        for i in item['thuoctinh']:
            
            try:
                obj = ThuocTinh.objects.get(
                    Url=Url.objects.get(Url = item['url']), 
                    MauSac=i['mausac'],
                    BoNho=i['bonho']
                )
                obj.Ngay5 = obj.Ngay4
                obj.Ngay4 = obj.Ngay3
                obj.Ngay3 = obj.Ngay2
                obj.Ngay2 = obj.Ngay1
                obj.Ngay1 = datetime.strptime(item['ngay'],'%d/%m/%Y').strftime('%Y-%m-%d')
                
                def rp(gia):
                    if gia==None:
                        return 0
                    else:
                        return gia.replace('.','').replace('₫','')

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
                thuoctinh.GiaGoc1 = 0 if i['giagoc']==None else i['giagoc'].replace('.','').replace('₫','')
                thuoctinh.GiaMoi1 = 0 if i['giamoi']==None else i['giamoi'].replace('.','').replace('₫','')
                thuoctinh.Ngay1 = datetime.strptime(item['ngay'],'%d/%m/%Y').strftime('%Y-%m-%d')
                thuoctinh.Url = Url.objects.get(Url = item['url'])
                thuoctinh.SanPham = SanPham.objects.get(TenSP = item['ten'])
                thuoctinh.Active = i['active']

                thuoctinh.save()

    return HttpResponse("Complete Import Data")
        
        
        
        
        


        
        
