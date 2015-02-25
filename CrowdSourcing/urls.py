from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from tastypie.api import Api

from CrowdSourcing.hostdiscovery import site_host
import DataEntry
from DataEntry.api import RecordResource, RecordObjectResource, GeographyResource, RightsResource
from DataEntry import views


v1_api = Api(api_name='v1')
v1_api.register(RecordResource())
v1_api.register(RecordObjectResource())
v1_api.register(GeographyResource())
v1_api.register(RightsResource())

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^(?P<site_identifier>\w+)/contribute/',
                           include('DataEntry.urls', namespace="DataEntry")),
                       url(r'geosearch$', DataEntry.views.geosearch, name='geosearch'),
                       url(r'^api/', include(v1_api.urls)),
                       url(r'^admin/', include(admin.site.urls)),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
