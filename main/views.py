from django.shortcuts import render,redirect
from .forms import GetUrlForm
from django.http import HttpResponseRedirect 
from django.http import JsonResponse
from django.urls import reverse


from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from urllib.parse import urlparse

import json

from .models import *

from django.db.models import Q

# Create your views here.
def index(request):
    return render(request,'pages/base.html')

def url_input(request):
    if request.method == "POST":
        form = GetUrlForm(request.POST)
        if form.is_valid():
            url = request.POST.get('url', None) #get url from user input

            if not url:
                return JsonResponse({'error': 'Missing  args'})
            if not is_valid_url(url):
                return JsonResponse({'error': 'URL is invalid'})
            
            domain = urlparse(url).netloc #take netloc from urlparse to get domain
            data = exporturl(url)
            #a = Url.objects.get(Url=url)
            return render(request,'pages/printurl.html',{'data':data})
            # return redirect('.')
            #return HttpResponseRedirect('/print_url',url)
    else:
        print("GẺT")
        form = GetUrlForm()

    return render(request, 'pages/geturl.html',{'form':form})

def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url) # check if url format is valid
    except ValidationError:
        return False

    return True

def print_url(request,url):
    return render(request,'pages/printurl.html',{'url':url})

def import_data():
    f = open('data.json','r')
    data = json.loads(f.read())

    for items in data:
        
        product = SanPham()
        url = Url()
        
        product.TenSP = item['ten']
        product.MaSP = item['ma']
        product.MoTa = item['mota']
        product.MaLoai = item['maloai']

        product.save()

def exporturl(url):
    url_input = Url.objects.get(Url=url) #truy xuất URL = url đã nhập
    product = SanPham.objects.get(MaSP__exact = url_input.MaSP.MaSP) #select Sản phẩm của url
    #criterion1 = Q(MaSP = url_input.MaSP)
    #criterion2 = Q( Url != url)    
    list_url = Url.objects.filter( MaSP = url_input.MaSP) #select tất cả các url cùng sản phẩm

    #lưu dữ liệu truy xuất và data
    data = {
        'product': product, #obj
        'url_in': url_input, #obj
        'url_out': list_url #list obj
    } 

    return data
