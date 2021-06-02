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

# Create your views here.
def index(request):
    return render(request,'pages/base.html')

def getattrib(request):
    if request.method == "POST":
        #form = GetAttribForm(request.POST)
        print(request.POST)
        #if form.is_valid():
        attrib = request.POST.get('mausac', None) #get url from user inputư
        
        #a = Url.objects.get(Url=url)
        return render(request,'pages/printurl.html',{'data':attrib})
            # return redirect('.')
            #return HttpResponseRedirect('/print_url',url)
    else:
        list_attr = [
            ('FR', 'Freshman'),
            ('SO', 'Sophomore'),
            ('JR', 'Junior'),
            ('SR', 'Senior'),
            ('GR', 'Graduate'),
        ]
        form = GetAttribForm(list_attr)

    return render(request, 'pages/getattrib.html',{'form':form})  

def url_input(request):
    if request.method == "POST":
        form = GetUrlForm(request.POST)
        if form.is_valid():
            url = request.POST.get('url', None) #get url from user input

            if not url:
                return JsonResponse({'error': 'Missing  args'})
            if not is_valid_url(url):
                return JsonResponse({'error': 'URL is invalid'})
            
            #domain = urlparse(url).netloc #take netloc from urlparse to get domain
            
            #data = exporturl(url)

            #truy xuất thuộc tính url
            url_input = Url.objects.get(Url=url) #truy xuất URL = url đã nhập
            list_thuoc_tinh_url = ThuocTinh.objects.filter( Url = url_input)

            list_mau_sac = [#có thể sai phần màu sắc
                ('do', 'Đỏ'),
                ('xanh duong', 'Xanh dương'),
                ('vang', 'Vàng'),
                ('den', 'Đen'),
                ('xam', 'Xám'),
                ('bac', 'Bạc')
            ]

            list_bo_nho = [
                ('16GB', '16GB'),
                ('32GB', '32GB'),
                ('64GB', '64GB'),
                ('128GB', '128GB'),
                ('256GB', '256GB'),
                ('512GB', '512GB')             
            ]
            #tạo form nhập thuộc tính
            mausac =[]
            bonho = []

            for attr in list_thuoc_tinh_url:
                for item in list_mau_sac:
                    if (attr.MauSac in item) and (item not in mausac) :
                        mausac.append(item) 
                for item in list_bo_nho:
                    if attr.BoNho in item and (item not in bonho):
                        bonho.append(item) 
            form = GetAttribForm(mausac=mausac,bonho=bonho)

            data= {
                'url_in': url_input,
                'form': form
            }
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
        bonho = request.POST.get('bonho', None) 
        url_in = request.POST.get('url', None)

        data = exporturl(url_in = url_in,mausac = mausac,bonho =bonho) #truy xuất database #???có thể sai phần màu sắc

        #a = Url.objects.get(Url=url)
        return render(request,'pages/printurl.html',{'data':data})

    else:
        list_attr = [
        ]
        form = GetAttribForm(list_attr)


def exporturl(url_in,mausac,bonho):     #Lấy dữ liệu trong database dựa vào thông tin đầu vào
    url = Url.objects.get(Url=url_in)
    thuoc_tinh_urlin = ThuocTinh.objects.get(Url=url,MauSac=mausac,BoNho=bonho)
    
    sanpham = SanPham.objects.get(TenSP__exact = url.SanPham.TenSP) #select Sản phẩm của url
    #criterion1 = Q(MaSP = url_input.MaSP)
    #criterion2 = Q( Url != url)    

    list_thuoc_tinh_url = ThuocTinh.objects.filter(SanPham = sanpham).filter(MauSac = mausac).filter(BoNho = bonho) #list thuộc tính các sản phẩm giống input

    print(list_thuoc_tinh_url)
    
    #lưu dữ liệu truy xuất và data
    data = {
        #'product': product, #obj
        'thuoc_tinh_urlin': thuoc_tinh_urlin, #obj
        'thuoc_tinh_urlout': list_thuoc_tinh_url,
    } 

    return data

def import_data(request):   #Nạp data.json và database

    f = open('data.json','r')
    data = json.loads(f.read())

    for item in data:

        #obj = ThuocTinh.objects.get(Url=Url.objects.get(Url = item['url']), MauSac=item['mausac'],BoNho=item['bonho'])
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
                UrlImage = item['img']
            )
        except NguonBan.DoesNotExist:
            Url.objects.update_or_create(
                Url = item['url'],
                SanPham = SanPham.objects.get(TenSP=item['ten']) ,
                UrlImage = item['img']
            )            

        try:
            obj = ThuocTinh.objects.get(Url=Url.objects.get(Url = item['url']), MauSac=item['mausac'],BoNho=item['bonho'])
            obj.Ngay5 = obj.Ngay4
            obj.Ngay4 = obj.Ngay3
            obj.Ngay3 = obj.Ngay2
            obj.Ngay2 = obj.Ngay1
            obj.Ngay1 = item['ngay']

            obj.GiaGoc5 = obj.GiaGoc4
            obj.GiaGoc4 = obj.GiaGoc3
            obj.GiaGoc3 = obj.GiaGoc2
            obj.GiaGoc2 = obj.GiaGoc1
            obj.GiaGoc1 = item['giagoc'].replace('.','')

            obj.GiaMoi5 = obj.GiaMoi4
            obj.GiaMoi4 = obj.GiaMoi3
            obj.GiaMoi3 = obj.GiaMoi2
            obj.GiaMoi2 = obj.GiaMoi1
            obj.GiaMoi1 = item['giamoi'].replace('.','')
            
            obj.save()

        except ThuocTinh.DoesNotExist:      
            thuoctinh = ThuocTinh()
            thuoctinh.MauSac = item['mausac']
            thuoctinh.BoNho = item['bonho']
            thuoctinh.GiaGoc1 = float(item['giagoc'].replace('.',''))
            thuoctinh.GiaMoi1 = float(item['giamoi'].replace('.',''))
            thuoctinh.Ngay1 = item['ngay']
            thuoctinh.Url = Url.objects.get(Url = item['url'])
            thuoctinh.SanPham = SanPham.objects.get(TenSP = item['ten'])
            thuoctinh.save()

    return HttpResponse("Complete Import Data")
        
        
        
        
        


        
        
