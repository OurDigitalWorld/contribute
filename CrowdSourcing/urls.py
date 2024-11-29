from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import include
from django.contrib import admin
# from django.urls import re_path
from django.urls.conf import re_path, include
from tastypie.api import Api
from DataEntry.api import RecordResource, RecordObjectResource, GeographyResource, RightsResource
from DataEntry import views

v1_api = Api(api_name='v1')
v1_api.register(RecordResource())
v1_api.register(RecordObjectResource())
v1_api.register(GeographyResource())
v1_api.register(RightsResource())

admin.autodiscover()

urlpatterns = [
       re_path(r'^$', views.upload),
       # url(r'^api/', include(v1_api.urls)),
       re_path(r'^admin/', admin.site.urls),

       ##########  if site has a path ####
       # ex: /contribute/5/update/
       re_path(r'^.*?/(?P<record_id>\d+)/update/$', views.update),
       # ex: /contribute/5/delete/
       re_path(r'^.*?/(?P<record_id>\d+)/delete/$', views.delete),
       # ex: /contribute/5/confirm/
       re_path(r'^.*?/(?P<record_id>\d+)/confirm/$', views.confirm),
       # ex: /contribute/5/[optional slug]/
       re_path(r'^.*?/(?P<record_id>\d+)/(?P<slug>[\w-]+)/$', views.detail),
       re_path(r'^.*?/(?P<record_id>\d+)/$', views.detail),
       # ex: /contribute/5/[optional slug]/full
       re_path(r'^.*?/(?P<record_id>\d+)/[\w-]+/full/$', views.full),
       re_path(r'^.*?/(?P<record_id>\d+)/full/$', views.full),
       # ex: /contribute/upload/
       re_path(r'^.*?/upload/$', views.upload),
       # ex: /contribute/upload/
       re_path(r'^.*?/rotate/(?P<record_id>\d+)/(?P<orientation>\d+)$', views.rotate),
       # ex: /contribute/geosearch/
       re_path(r'^.*?/conf/(?P<vita_set>\w+)/(?P<vita_site_id>\d+)/$', views.configure),
       # ex: /contribute/geosearch/
       re_path(r'^.*?/geosearch$', views.geosearch),
        # ex: /contribute/getsize
       re_path(r'^.*?/getsize$', views.getsize),
       re_path(r'^.*?/api/', include(v1_api.urls)),
       # re_path(r'^.*?/api/entry/schema/', include(v1_api.urls)),

       ##########  if site has no path ####

       # ex: 5/update/
       re_path(r'^(?P<record_id>\d+)/update/$', views.update),
       # ex: 5/delete/
       re_path(r'^(?P<record_id>\d+)/delete/$', views.delete),
       # ex: 5/confirm/
       re_path(r'^(?P<record_id>\d+)/confirm/$', views.confirm),
       # ex: 5/[optional slug]/
       re_path(r'^(?P<record_id>\d+)/(?P<slug>[\w-]+)/$', views.detail),
       re_path(r'^(?P<record_id>\d+)/$', views.detail),
       # ex: 5/[optional slug]/full
       re_path(r'^(?P<record_id>\d+)/[\w-]+/full/$', views.full),
       re_path(r'^(?P<record_id>\d+)/full/$', views.full),
       # ex: upload/
       re_path(r'^upload/$', views.upload),
       # ex: rotate/5/3
       re_path(r'^rotate/(?P<record_id>\d+)/(?P<orientation>\d+)$', views.rotate),
       # ex: conf/[stuff]
       re_path(r'^conf/(?P<vita_set>\w+)/(?P<vita_site_id>\d+)/$', views.configure),
       # ex: geosearch
       re_path(r'^geosearch$', views.geosearch),
        # ex: getsize
       re_path(r'^getsize$', views.getsize),
       re_path(r'^copyfile$', views.copyfile),
       re_path(r'^api/', include(v1_api.urls)),
       ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
