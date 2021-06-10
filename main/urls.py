from os import name
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import re_path
urlpatterns = [
    path('',views.url_input),
    re_path(r'^print-url/',views.print_url, name='print_url'),
    path('import-data/',views.import_data, name='import_data'),
    path('<int:id>', views.product_supplier, name= 'product_supplier' ),
    path('get-attribute/',views.get_attribute, name='get_attribute'),
]
