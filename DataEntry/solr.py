__author__ = 'walter'

# import pysolr
import requests
from CrowdSourcing.customlog import log_request
from django.conf import settings
SOLR_INDEX_URL = "http://localhost:8983/solr/"
GEO_URL = "http://localhost:8983/solr/geonames1/query?"
URL_EXTENDED_FIELD_LIST = '&fl=id,name,latitude,longitude,feature_text_ss,country_text_ss,admin1_text_ss,country_code'



def geosolrsearch(request):
    query = ''
    results = ''
    place_string = ''
    term_string = ''
    if request.GET.get('term'):
        query = 'allNames: ' + request.GET['term'] + '*'
    # log_request('query (GN:68: ', query)
    if request.GET.get('id'):
        query = '%s id:"%s"' % (query, request.GET.get('id'))
    if request.GET.get('c'):
        country = request.GET['c']
    else:
        country = ''
    if request.GET.get('p'):
        province_state = request.GET['p']
    else:
        province_state = ''
    if country:
        query = '%s+AND+country_code:"%s"' % (query, country)
    if province_state:
        query = '%s+AND+admin1_text_ss:"%s"' % (query, province_state)
    url = '%sq=%s&rows=200&sort=priority_i+asc,name+asc&wt=json%s' % (GEO_URL, query, URL_EXTENDED_FIELD_LIST)
    # log_request('url (GN:84: ', url)
    r = requests.get(url)
    # log_request('status code (GN:86: ', r.status_code)
    if r.status_code == 200:
        # log_request('r (GN:88: ', r)
        solr_response = r.json()
        # log_request('solr_response (GN:90: ', solr_response)
        number_found = solr_response['response']['numFound']
        if int(number_found) > 0:
            results =solr_response['response']['docs']
            log_request('results: ', results)
            for place in results:
                place_string = ''
                id = place['id']
                name = place['name']
                latitude = place['latitude']
                longitude = place['longitude']
                admin1 = place['admin1_text_ss'][0]
                country_text = place['country_text_ss'][0]
                country_code = place['country_code'][0]
                feature_text = place['feature_text_ss'][0]
                place_string = '{"id":"%s", "term":"%s"' % (id, name)
                if admin1:
                    place_string += ', %s' % admin1
                if country:
                    place_string += ', %s' % country_text
                place_string += ' (%s: %s, %s)", "latitude":"%s","longitude":"%s",' % \
                                (feature_text, latitude, longitude, latitude, longitude)
                place_string += '"name": "%s"}' % name
                # print(place_string)
                if term_string:
                    term_string += ', '
                term_string += place_string
        # print(term_string)
        final_results = '{"terms":[%s]}' % term_string
        print(final_results)
    return final_results


def solr_search_query(query, index):
    """
    A lightweight function for passing simple general field searches to a solr index for results
    """

    results = ''
    url = "%s%s/query?wt=json&q=%s" % (SOLR_INDEX_URL,index, query)
    if index =='geonames':
        url += URL_EXTENDED_FIELD_LIST
    r = requests.get(url)
    if r.status_code == 200:
        # log_request('r (GN:88: ', r)
        solr_response = r.json()
        # log_request('solr_response (GN:90: ', solr_response)
        number_found = solr_response['response']['numFound']
        if int(number_found) > 0:
            results =solr_response['response']['docs']
    # log_request('docs: ', docs)
    return results


def solr_by_field(field, value, index):
    """
    A lightweight function for passing simple field searches to a solr index for results
    """
    solr_index = "%s%s" % (settings.SOLR_INDEX_URL,index)
    solr = pysolr.Solr(solr_index, timeout=10)
    query = '(%s:%s)' % (field, value)
    results = solr.search(query)
    return results