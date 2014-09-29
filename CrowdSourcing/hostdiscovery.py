__author__ = 'walter'

from django.http import HttpRequest
from DataEntry.models import Site, SiteSetup


def site_host(request):
    site_dict = {}
    host = HttpRequest.build_absolute_uri(request)
    #print('host: ', host)
    sites = Site.objects.order_by('-site_url')
    #print('sites: ', sites)
    for site in sites:
        test_site_url = site.site_url.lower()
        if host.lower().startswith(test_site_url):
            #print('got to line 15')
            site_dict['site_id'] = site.id
            site_dict['site_name'] = site.site_name
            site_dict['site_url'] = site.site_url
            break
    return site_dict

def site_settings(request):
    site_dict = site_host(request)
    site_id = site_dict['site_id']
    site_values = SiteSetup.objects.filter(site_id=site_id)
    for f in site_values:
        #print("function settings: " + f.afield + ":" + f.avalue)
        site_dict[f.afield] = f.avalue
    #print(site_dict)
    return site_dict

