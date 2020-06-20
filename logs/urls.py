from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^errors/H12/$', views.generate_H12, name='generate_H12'),
    url(r'^errors/500/$', views.generate_500, name='generate_500'),
]
