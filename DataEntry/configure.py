__author__ = 'walter'

import json
import urllib.request
from DataEntry.models import Site, SiteSetup
from django.conf import settings


def configure_site(vita_set, vita_site_id):
    vita_path = ''
    if vita_set == 'OOT':
        vita_path = settings.OOT_PATH
    elif vita_set == 'OOTr':
        vita_path = settings.OOTR_PATH
    elif vita_set == 'OOM':
        vita_path = settings.OOM_PATH
    elif vita_set == 'OOI':
        vita_path = settings.OOV_PATH
    else:
        'Oh crap we did not pass the variable properly'

    vita_url = '%ssite2xa.asp?id=%s' % (vita_path, vita_site_id)
    response = urllib.request.urlopen(vita_url)
    data = response.read()
    f = data.decode('utf-8')
    datadict = json.loads(f)
    con_site_id = datadict['ConSiteID']
    con_site_name = datadict['SiteName']
    con_site_url = datadict['ConSiteURL']
    con_group_id = datadict['ConGroupID']
    # current_site = Site.objects.filter(id=con_site_id)
    current_site = Site.objects.filter(group_identifier=con_group_id)
    if current_site.count() < 1:
        add_site = Site(site_name=con_site_name, site_url=con_site_url, group_identifier=con_group_id)
        add_site.save()
        site_id = add_site.id
        # update the vita configuration with the new ConSiteID
        vita_url = '%ssite2xb.asp?id=%s&cid=%s' % (vita_path, vita_site_id, site_id)
        response = urllib.request.urlopen(vita_url)
    else:
        site_id = current_site[0].id
        existing_site = Site.objects.get(id=con_site_id)
        existing_site.site_name = con_site_name
        existing_site.site_url = con_site_url
        existing_site.group_identifier = con_group_id
        existing_site.save(update_fields=['site_name', 'site_url', 'group_identifier'])
    for item in datadict:
        try:
            existing_record = SiteSetup.objects.get(site_id=site_id, afield=item)
            data_value = datadict[item]
            existing_record.avalue = data_value
            existing_record.save()
        except SiteSetup.DoesNotExist:
            ss = SiteSetup(site_id=site_id, afield=item, avalue=datadict[item])
            ss.save()
    return data
