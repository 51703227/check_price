from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.url_input),
    path('print-url/',views.print_url, name='print_url'),
    path('import-data/',views.import_data, name='import_data'),
]
