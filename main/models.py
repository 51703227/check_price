from django.db import models

# Create your models here.


class LoaiSanPham(models.Model):
    TenLoai = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return self.TenLoai

class ThuongHieu(models.Model):
    TenTH = models.CharField(max_length=100,null=True,default='')

    def __str__(self):
        return self.TenTH

class NguonBan(models.Model):
    TenNB = models.CharField(max_length=100)
    Domain = models.URLField(null=True)
    Logo = models.URLField(null=True)

    def __str__(self):
        return self.TenNB

class GiaMoi(models.Model):
    Gia1 = models.FloatField(null=True,blank=True)
    Gia2 = models.FloatField(null=True,blank=True)
    Gia3 = models.FloatField(null=True,blank=True)
    Gia4 = models.FloatField(null=True,blank=True)
    Gia5 = models.FloatField(null=True,blank=True)
    Ngay1 = models.DateField(null=True,blank=True)
    Ngay2 = models.DateField(null=True,blank=True)
    Ngay3 = models.DateField(null=True,blank=True)
    Ngay4 = models.DateField(null=True,blank=True)
    Ngay5 = models.DateField(null=True,blank=True)

class GiaGoc(models.Model):
    Gia1 = models.FloatField(null=True,blank=True)
    Gia2 = models.FloatField(null=True,blank=True)
    Gia3 = models.FloatField(null=True,blank=True)
    Gia4 = models.FloatField(null=True,blank=True)
    Gia5 = models.FloatField(null=True,blank=True)
    Ngay1 = models.DateField(null=True,blank=True)
    Ngay2 = models.DateField(null=True,blank=True)
    Ngay3 = models.DateField(null=True,blank=True)
    Ngay4 = models.DateField(null=True,blank=True)
    Ngay5 = models.DateField(null=True,blank=True)


class SanPham(models.Model):
    TenSP = models.CharField(max_length=100,null=True,blank=True)
    LoaiSanPham = models.ForeignKey(LoaiSanPham,on_delete=models.CASCADE,null=True,blank=True)
    ThuongHieu = models.ForeignKey(ThuongHieu,on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.TenSP

class Url(models.Model):
    Url = models.URLField() 
    NguonBan = models.ForeignKey(NguonBan,on_delete=models.CASCADE,null=True,blank=True)
    SanPham = models.ForeignKey(SanPham,on_delete=models.CASCADE,null=True,blank=True)
    UrlImage = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.Url

class ThuocTinh(models.Model):
    MauSac = models.CharField(max_length=100,null=True,blank=True)
    BoNho = models.CharField(max_length=100,null=True,blank=True)
    GiaMoi = models.ForeignKey(GiaMoi,on_delete=models.CASCADE,null=True,blank=True)
    GiaGoc = models.ForeignKey(GiaGoc,on_delete=models.CASCADE,null=True,blank=True)
    Url = models.ForeignKey(Url,on_delete=models.CASCADE,null=True,blank=True)
    SanPham = models.ForeignKey(SanPham,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.MauSac 
    






