from django.urls import path, re_path
from web01.views import read_file, to_dir, test, save_excel, index

urlpatterns = [
    path('read_file', read_file, name="read_file"),
    path('to_dir', to_dir, name="to_dir"),
    path('test', test, name="test"),
    path('wa_save', save_excel, name="wa_save"),
    path('', index, name="wa_index")
]