from django.urls import path
from web03.views import w2c1,w2c2,w2c3
from django.conf.urls import url
urlpatterns = [
    path("2/",w2c1.show,name='index3'),
    url(r"^train/",w2c1.train,name='train'),
    url(r"^visual/",w2c1.visual,name='visual'),
    url(r"^cbdownload/",w2c2.cibiao_download,name='cibiao_download'),
    url(r"^pic_download/",w2c2.pic_download,name='pic_download'),
    url(r"^sim_visual/",w2c3.sim_visual,name='sim_visual'),
    url(r"^sim_visualdu/",w2c3.sim_visualdu,name='sim_visualdu'),
    url(r"^sim/",w2c3.sim,name='sim'),
    ]