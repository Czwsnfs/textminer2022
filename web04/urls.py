from ast import Index
from django.urls import path

from web04.views import index
urlpatterns = [
    path("",index.LDA1,name="index"),
    path("analyze1",index.analyze1,name="analyze1"),
    path("analyze2",index.analyze2,name="analyze2"),
    path("analyze11",index.analyze11,name="analyze11"),
    path("analyze13",index.analyze13,name="analyze13"),
    path("analyze12",index.analyze12,name="analyze12"),
]