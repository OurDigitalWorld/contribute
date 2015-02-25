__author__ = 'walter'

from django.conf.urls import patterns, url
from DataEntry import views


urlpatterns = patterns('',
                       # ex: /contribute/
                       url(r'^$', views.index, name='index'),
                       # ex: /contribute/5/update/
                       url(r'^(?P<record_id>\d+)/update/$', views.update, name='update'),
                       # ex: /contribute/5/delete/
                       url(r'^(?P<record_id>\d+)/delete/$', views.delete, name='delete'),
                       # ex: /contribute/5/confirm/
                       url(r'^(?P<record_id>\d+)/confirm/$', views.confirm, name='confirm'),
                       # ex: /contribute/5/[optional slug]/
                       url(r'^(?P<record_id>\d+)/(?P<slug>[\w-]+)/$', views.detail, name='detail'),
                       url(r'^(?P<record_id>\d+)/$', views.detail, name='detail'),
                       # ex: /contribute/5/[optional slug]/full
                       url(r'^(?P<record_id>\d+)/[\w-]+/full/$', views.full, name='full'),
                       url(r'^(?P<record_id>\d+)/full/$', views.full, name='full'),
                       # ex: /contribute/upload/
                       url(r'^upload/$', views.upload, name='upload'),
                       # ex: /contribute/geosearch/
                       url(r'^conf/(?P<vita_set>\w+)/(?P<vita_site_id>\d+)/$', views.configure, name='configure'),
                       # ex: /contribute/geosearch/
                       url(r'^geosearch$', views.geosearch, name='geosearch'),
        	               #ex: /contribute/getsize/
                       url(r'^getsize$', views.getsize, name='getsize'),

)