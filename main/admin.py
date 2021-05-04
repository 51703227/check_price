from django.contrib import admin
from .models import *

class LoaiSanPhamAdmin(admin.ModelAdmin):
    list_display = ['TenLoai']
    list_filter = ['MaLoai']
    search_fields = ['TenLoai']

class SanPhamAdmin(admin.ModelAdmin):
    list_display = ['TenSP', 'MaSP']
    list_filter = ['MaSP']
    search_fields = ['TenSP']

class UrlAdmin(admin.ModelAdmin):
    list_display = ['MaSP', 'Domain','Gia','GiaCu']
    list_filter = ['Domain']
    search_fields = ['MaSP']
    
# Register your models here.
admin.site.register(LoaiSanPham,LoaiSanPhamAdmin)
admin.site.register(SanPham,SanPhamAdmin)
admin.site.register(Url,UrlAdmin)