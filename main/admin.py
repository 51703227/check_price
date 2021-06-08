from django.contrib import admin
from .models import *

class LoaiSanPhamAdmin(admin.ModelAdmin):
    list_display = ['TenLoai']
    list_filter = ['TenLoai']
    search_fields = ['TenLoai']

class SanPhamAdmin(admin.ModelAdmin):
    list_display = ['TenSP']
    list_filter = ['TenSP']
    search_fields = ['TenSP']

class UrlAdmin(admin.ModelAdmin):
    list_display = ['Url','SanPham']
    search_fields = ['Url']
    list_filter = ['NguonBan']

class ThuongHieuAdmin(admin.ModelAdmin):
    list_display = ['TenTH']
    list_filter = ['TenTH']
    search_fields = ['TenTH']

class NguonBanAdmin(admin.ModelAdmin):
    list_display = ['TenNB']
    list_filter = ['TenNB']
    search_fields = ['TenNB']

class ThuocTinhAdmin(admin.ModelAdmin):
    list_display = ['SanPham','MauSac','BoNho']
    search_fields = ['MauSac']
    list_filter = ['SanPham']
# Register your models here.
admin.site.register(LoaiSanPham,LoaiSanPhamAdmin)
admin.site.register(SanPham,SanPhamAdmin)
admin.site.register(Url,UrlAdmin)
admin.site.register(ThuongHieu,ThuongHieuAdmin)
admin.site.register(NguonBan,NguonBanAdmin)
#admin.site.register(GiaGoc)
#admin.site.register(GiaMoi)
admin.site.register(ThuocTinh,ThuocTinhAdmin)