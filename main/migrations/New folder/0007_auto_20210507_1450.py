# Generated by Django 3.1.7 on 2021-05-07 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210507_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='url',
            name='ThuocTinh',
        ),
        migrations.AddField(
            model_name='thuoctinh',
            name='Url',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.url'),
        ),
    ]
