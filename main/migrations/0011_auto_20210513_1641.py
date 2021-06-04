# Generated by Django 3.1.7 on 2021-05-13 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_thuoctinh_sanpham'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thuoctinh',
            name='GiaGoc',
        ),
        migrations.RemoveField(
            model_name='thuoctinh',
            name='GiaMoi',
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='GiaGoc1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='GiaGoc2',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='GiaGoc3',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='GiaGoc4',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='GiaGoc5',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='GiaMoi1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='GiaMoi2',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='GiaMoi3',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='GiaMoi4',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='GiaMoi5',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='Ngay1',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='Ngay2',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='Ngay3',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='Ngay4',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='Ngay5',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='GiaGoc',
        ),
        migrations.DeleteModel(
            name='GiaMoi',
        ),
    ]