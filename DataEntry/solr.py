__author__ = 'walter'

import pysolr
from django.conf import settings


def solrsearch(request, index):
    """
    A lightweight function for passing simple general field searches to a solr index for results
    """

    solr_index = "%s%s" % (settings.SOLR_INDEX_URL, index)
    solr = pysolr.Solr(solr_index, timeout=10)
    query = request.GET['term'] + '*'
    if request.GET.get('c'):
        country = request.GET['c']
    else:
        country = ''
    if request.GET.get('p'):
        province_state = request.GET['p']
    else:
        province_state = ''
    if country:
            query = '%s countryCode:"%s"' % (query, country)
    if province_state:
            query = '%s admin1text:"%s"' % (query, province_state)
    if index == 'geonames':
        results = solr.search(query, sort='priority asc, name asc', row='1000')
    else:
        results = solr.search(query)
    return results


def solr_search_query(query, index):
    """
    A lightweight function for passing simple general field searches to a solr index for results
    """

    solr_index = "%s%s" % (settings.SOLR_INDEX_URL, index)
    solr = pysolr.Solr(solr_index, timeout=10)
    results = solr.search(query, wt='json')
    return results


def solr_by_field(field, value, index):
    """
    A lightweight function for passing simple field searches to a solr index for results
    """

    solr_index = "%s%s" % (settings.SOLR_INDEX_URL, index)
    solr = pysolr.Solr(solr_index, timeout=10)
    query = '(%s:%s)' % (field, value)
    results = solr.search(query)
    return results