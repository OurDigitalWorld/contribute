from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.utils.http import urlquote
import os.path
import urllib.request
from DataEntry.forms import UploadForm
from DataEntry.models import Record, RecordObject, Geography
from DataEntry.image import process_image, get_image_size
from DataEntry.text import process_text
from CrowdSourcing.hostdiscovery import site_settings
from DataEntry.solr import solrsearch, solr_search_query
from DataEntry.record_object_utilities import delete_record
from DataEntry.configure import configure_site

# ==================================


def index(request):
    """
    default page for site
    @param request: not expecting many at the default level
    @return: default start page
    """
    return HttpResponseRedirect('upload')


def detail(request, site_identifier, record_id, slug=''):
    """
    @param request:
    @param site_identifier:
    @param record_id:
    @param slug:
    @return:

    Render a detail version of all the fields that were contributed asking for confirmation, deletion or further editing
    If slug == 'edit', then pass the variables to an editable form which returns to the main rendering for confirmation again.
    """

    geodata = {}
    message = request.GET.get('m','')
    site_values = site_settings(request)
    record = get_object_or_404(Record, pk=record_id)
    geography = Geography.objects.filter(record_id=record_id)
    geoids = ""
    for geo in geography:
        if geoids == "":
            geoids = "id:%s" % (str(geo.geonameid))
        else:
            geoids += " OR id:%s" % (str(geo.geonameid))
        geoids = "%s" % geoids
        geodata = solr_search_query(geoids, 'geonames')
        print(geodata)
    try:
        recordobject = RecordObject.objects.filter(record_id=record_id).order_by('record_object_category_id')
    except RecordObject.DoesNotExist:
        recordobject = ''
        google_map_canvas = '300'
    #TODO: break up context elements between shared and unique to either edit or detail
    context = {
        'site_settings': site_values,
        'site_identifier': site_identifier,
        'record': record,
        'recordobject': recordobject,
        'full': False,
        'geodata': geodata,
        'gMap': True,
        'showProvince': True,
        'jQuery': True,
        'delete_dialog':True,
        'message': message,
    }
    if slug == 'edit':
        return render(request, 'DataEntry/edit.html', context)
    else:
        return render(request, 'DataEntry/detail.html', context)


def full(request, site_identifier, record_id):
    site_values = site_settings(request)
    record = get_object_or_404(Record, pk=record_id)
    try:
        recordobject = RecordObject.objects.filter(record_id=record_id, record_object_category_id=2)
        context = {
            'site_settings': site_values,
            'site_identifier': site_identifier,
            'record': record,
            'recordobject': recordobject,
            'full': True}
        return render(request, 'DataEntry/detail.html', context)
    except RecordObject.DoesNotExist:
        target = "/%s/contribute/%s/%s/" % (site_identifier, record_id, record.slug)
        return HttpResponseRedirect(target)


def upload(request, site_identifier):
    site_values = site_settings(request)
    site_id = site_values['site_id']
    display_public = site_values['ConPublicDisplay']
    vita_url = request.GET.get('u','')
    vita_thumb_url = request.GET.get('t','')
    upload_action = '/%s/contribute/upload/' % site_identifier
    message = request.GET.get('m','')
    if message == 'delete':
        message = site_values['ConLabelDeleteConfirm']
    elif message == 'confirm':
        if display_public == '1':
            message = site_values['ConPublicMessage2']
        else:
            message = site_values['ConNonPublicMessage']


    new_contribution_pk = 0
    if request.method == 'POST':  # If the form has been submitted...
        turing_subj = request.POST.get('subj', '') # on the assumption that the comment form spammer will fill out the subj form
        if len(turing_subj) < 1:
            turing_test_passed = True
        else:
            turing_test_passed = False
    else:
        turing_test_passed = False     #not strictly true, but the point is to present (or re-present an empty form)
    if (turing_test_passed):
        if 'image_file' in request.FILES:
            #print("Went via RequestFiles")
            #print(request.POST)
            #form = UploadForm(site_id, new_contribution_pk, request.POST, request.FILES, empty_permitted=True)  # A form bound to the POST data
            form = UploadForm(request.POST, empty_permitted=True)  # A form bound to the POST data
            #print("Back from RequestFiles UploadForm")
            if form.is_valid(): # All validation rules pass
                #TODO:  refactor the next three lines which are repeated below
               # print("Save please")
                new_contribution_pk = form.save(request, site_id, new_contribution_pk)
                #print("Back from RequestFiles UploadForm")
                image_file_name =  get_object_or_404(Record, pk=new_contribution_pk).image_file.name
                    #process the  uploaded file
                file_extension = os.path.splitext(image_file_name)[1][1:]
                #print(file_extension)
                if file_extension.lower() in ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'tif', 'tiff']:
                    process_image(new_contribution_pk, image_file_name)
                elif file_extension.lower() in ['txt', 'pdf', 'doc', 'docx']:
                    process_text(new_contribution_pk, image_file_name)
                target = "/%s/contribute/%s/" % (site_identifier, new_contribution_pk)
                return HttpResponseRedirect(target) # Redirect after POST
        else:
            #print("Went via RequestPOST")
            form = UploadForm(request.POST, empty_permitted=True)
            #print("Back from RequestPOST UploadForm")
            if form.is_valid():  # All validation rules pass
                #print("Form was valid")
                new_contribution_pk = form.save(request, site_id, 0)
                target = "/%s/contribute/%s/" % (site_identifier, new_contribution_pk)
                return HttpResponseRedirect(target) # Redirect after POST
        return render_to_response('DataEntry/form_errors.html', {'form': form})
    else:
        form = UploadForm()  # An unbound form
    context = {
        'site_settings': site_values,
        'site_identifier': site_identifier,
        'form': form,
        'jQuery': True,
        'gMap': True,
        'showProvince': True,
        'vita_url' : vita_url,
        'vita_thumb_url': vita_thumb_url,
        'message': message,
        'upload': True,
        'upload_action': upload_action,
    }
    return render(request, 'DataEntry/upload.html', context)


def update(request, site_identifier, record_id):
    site_values = site_settings(request)
    site_id = site_values['site_id']
    record = Record.objects.get(pk=record_id)
    print(request.method)
    if request.method == 'POST':  # If the form has been submitted...
        form = UploadForm(request.POST, empty_permitted=True, instance=record)
        if form.is_valid():  # All validation rules pass
            #    print("Form was valid")
            form.save(request, site_id, record_id, instance=record)
            target = "/%s/contribute/%s/" % (site_identifier, record_id)
            return HttpResponseRedirect(target) # Redirect after POST
        return render_to_response('DataEntry/form_errors.html', {'form': form})


def delete(request, site_identifier, record_id):
    #TODO:  in dev environment this is throwing "BrokenPipeError: [Errno 32] Broken pipe" errors
    #TODO: probably because the deletion of the file objects is lagging behind execution
    are_we_done = delete_record(record_id)
    #redirect to /contribute/upload
    if are_we_done == 'done' :
        redirect_url = '/%s/contribute/upload?m=delete' % site_identifier
        return HttpResponseRedirect(redirect_url)


def confirm(request, site_identifier, record_id):
    site_values = site_settings(request)
    data_callback_base = site_values['VitaPath']
    group_id = site_values['ConGroupID']
    confirm_error = site_values['ConLabelConfirmError']
    data_callback_url = "%sUpdateContribute.asp?id=%s&gid=%s" % (data_callback_base, record_id, group_id)
    #print(data_callback_url)
    response = urllib.request.urlopen(data_callback_url)
    data = response.read()
    f = data.decode('utf-8')
    #print(f)
    if (f[:4] == 'http'):
        vita_url = ''
        vita_thumb_url = ''
        urls = f.split('|')
        if urls[0]:
            vita_url = urls[0]
        if urls[1]:
            vita_thumb_url = urls[1]
        are_we_done = delete_record(record_id)
        if are_we_done == 'done' :
            redirect = '/%s/contribute/upload?u=%s&t=%s&m=confirm' % (site_identifier, vita_url, vita_thumb_url)
            return HttpResponseRedirect(redirect)
        else:
            return render_to_response('DataEntry/test.html', {'results': f})
    else:
        message = urlquote(confirm_error)
        redirect_url = '/%s/contribute/%s?m=%s' % (site_identifier, record_id, message)
        return HttpResponseRedirect(redirect_url)


def configure(request, site_identifier, vita_set, vita_site_id):
    #print('db_identifier: ', vita_set)
    #print('vita_site_id: ', vita_site_id)
    results = configure_site(vita_set, vita_site_id)
    #results="did something, maybe"
    return render_to_response('DataEntry/test.html', {'results': results})


def geosearch(request):
    #TODO: configure scoping of places by country and optionally provinces/admin1
    results = solrsearch(request, 'geonames')
    return render_to_response('DataEntry/geo.html', {'results': results})


def getsize(request, site_identifier):
    #TODO: configure scoping of places by country and optionally provinces/admin1
    results = get_image_size(request)
    return HttpResponse(results, content_type='text/plain')