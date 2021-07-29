from django.db import models
from django.db.models.fields import BooleanField

# Create your models here.

class LoaiSanPham(models.Model):
    TenLoai = models.CharField(max_length=100,null=True,unique=True)
    
    def __str__(self):
        return self.TenLoai

class ThuongHieu(models.Model):
    TenTH = models.CharField(max_length=100,null=True,default='',blank=True)

    def __str__(self):
        return self.TenTH

class NguonBan(models.Model):
    TenNB = models.CharField(max_length=100,unique=True)
    Domain = models.CharField(max_length=100,null=True,unique=True)
    Logo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.TenNB

#class GiaMoi(models.Model):
#    GiaMoi1 = models.FloatField(null=True,blank=True)
#    GiaMoi2 = models.FloatField(null=True,blank=True)
#    GiaMoi3 = models.FloatField(null=True,blank=True)
#    GiaMoi4 = models.FloatField(null=True,blank=True)
#    GiaMoi5 = models.FloatField(null=True,blank=True)
#    Ngay1 = models.DateField(null=True,blank=True)
#    Ngay2 = models.DateField(null=True,blank=True)
#    Ngay3 = models.DateField(null=True,blank=True)
#    Ngay4 = models.DateField(null=True,blank=True)
#    Ngay5 = models.DateField(null=True,blank=True)

#class GiaGoc(models.Model):
#    GiaGoc1 = models.FloatField(null=True,blank=True)
#    GiaGoc2 = models.FloatField(null=True,blank=True)
#    GiaGoc3 = models.FloatField(null=True,blank=True)
#    GiaGoc4 = models.FloatField(null=True,blank=True)
#    GiaGoc5 = models.FloatField(null=True,blank=True)
#    Ngay1 = models.DateField(null=True,blank=True)
#    Ngay2 = models.DateField(null=True,blank=True)
#    Ngay3 = models.DateField(null=True,blank=True)
#    Ngay4 = models.DateField(null=True,blank=True)
#    Ngay5 = models.DateField(null=True,blank=True)


class SanPham(models.Model):
    TenSP = models.CharField(max_length=100,null=True,blank=True)
    LoaiSanPham = models.ForeignKey(LoaiSanPham,on_delete=models.CASCADE,null=True,blank=True)
    ThuongHieu = models.ForeignKey(ThuongHieu,on_delete=models.CASCADE,null=True,blank=True)
    ImgSP = models.TextField(null=True,blank=True)
    NgayKhoiTao = models.DateField(null=True,blank=True)
    def __str__(self):
        return str(self.pk) + ' - ' + self.TenSP

class Url(models.Model):
    Url = models.URLField(unique=True) 
    NguonBan = models.ForeignKey(NguonBan,on_delete=models.CASCADE,null=True,blank=True)
    SanPham = models.ForeignKey(SanPham,on_delete=models.CASCADE,null=True,blank=True)
    UrlImage = models.URLField(null=True,blank=True)
    Tskt = models.TextField(null=True,blank=True)  
    MoTa = models.TextField(null=True,blank=True)  
    def __str__(self):
        return self.Url

class ThuocTinh(models.Model):
    MauSac = models.CharField(max_length=100,null=True,blank=True)
    BoNho = models.CharField(max_length=100,null=True,blank=True)
#    GiaMoi = models.ForeignKey(GiaMoi,on_delete=models.CASCADE,null=True,blank=True)
#    GiaGoc = models.ForeignKey(GiaGoc,on_delete=models.CASCADE,null=True,blank=True)
    Url = models.ForeignKey(Url,on_delete=models.CASCADE,null=True,blank=True)
    SanPham = models.ForeignKey(SanPham,on_delete=models.CASCADE,null=True,blank=True)
    NguonBan = models.ForeignKey(NguonBan,on_delete=models.CASCADE,null=True,blank=True)
    Active = models.BooleanField(null=True,blank=True)
    GiaGoc1 = models.FloatField(null=True,blank=True,default=0)
    GiaGoc2 = models.FloatField(null=True,blank=True,default=0)
    GiaGoc3 = models.FloatField(null=True,blank=True,default=0)
    GiaGoc4 = models.FloatField(null=True,blank=True,default=0)
    GiaGoc5 = models.FloatField(null=True,blank=True,default=0)
    GiaMoi1 = models.FloatField(null=True,blank=True,default=0)
    GiaMoi2 = models.FloatField(null=True,blank=True,default=0)
    GiaMoi3 = models.FloatField(null=True,blank=True,default=0)
    GiaMoi4 = models.FloatField(null=True,blank=True,default=0)
    GiaMoi5 = models.FloatField(null=True,blank=True,default=0)
    Ngay1 = models.DateField(null=True,blank=True)
    Ngay2 = models.DateField(null=True,blank=True)
    Ngay3 = models.DateField(null=True,blank=True)
    Ngay4 = models.DateField(null=True,blank=True)
    Ngay5 = models.DateField(null=True,blank=True)
    
    def __str__(self):
        return str(self.pk) 
    






