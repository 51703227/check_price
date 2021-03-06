# Generated by Django 3.1.7 on 2021-05-07 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210507_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thuoctinh',
            name='Gia1',
        ),
        migrations.AddField(
            model_name='giagoc',
            name='Ngay1',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='giagoc',
            name='Ngay2',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='giagoc',
            name='Ngay3',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='giagoc',
            name='Ngay4',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='giagoc',
            name='Ngay5',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='giamoi',
            name='Ngay1',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='giamoi',
            name='Ngay2',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='giamoi',
            name='Ngay3',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='giamoi',
            name='Ngay4',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='giamoi',
            name='Ngay5',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='GiaGoc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.giagoc'),
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='GiaMoi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.giamoi'),
        ),
        migrations.DeleteModel(
            name='Gia',
        ),
    ]
