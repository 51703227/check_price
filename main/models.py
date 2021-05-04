from django.db import models

# Create your models here.
class LoaiSanPham(models.Model):
    MaLoai = models.CharField(max_length=30)
    TenLoai = models.CharField(max_length=100)
    
    def __str__(self):
        return self.TenLoai

class SanPham(models.Model):
    MaSP = models.CharField(max_length=30)
    TenSP = models.CharField(max_length=100)
    MoTa = models.TextField()
    MaLoai = models.ForeignKey(LoaiSanPham,on_delete=models.CASCADE)

    def __str__(self):
        return self.TenSP

class Url(models.Model):
    Url = models.URLField() 
    Domain = models.URLField(null=True)
    MaSP = models.ForeignKey(SanPham,on_delete=models.CASCADE)
    Gia = models.FloatField()
    GiaCu = models.FloatField()
    UrlImage = models.URLField(null=True)

    def __str__(self):
        return self.Url

class NguonBan(models.Model):
    TenNB = models.CharField(max_length=100)
    Domain = models.URLField(null=True)
    Logo = models.URLField(null=True)

    def __str__(self):
        return self.TenNB






