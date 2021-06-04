# Generated by Django 3.1.7 on 2021-05-13 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20210513_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loaisanpham',
            name='TenLoai',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='nguonban',
            name='Domain',
            field=models.URLField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='nguonban',
            name='TenNB',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='sanpham',
            name='TenSP',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='thuonghieu',
            name='TenTH',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]