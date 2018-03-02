from django.conf.urls import url

from . import views
urlpatterns = [
    url('^$',views.uploadImg,name='index'),
    url('^api/detect$',views.detect),
    url(r'^api/upload$', views.upload),
    url(r'^api/upload_and_detect$',views.upload_and_detect),
    url(r'^test',views.uploadImg),
]