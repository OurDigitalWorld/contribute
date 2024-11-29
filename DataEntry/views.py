import os.path
import urllib.request
from urllib.parse import quote_plus
from time import sleep
from django.shortcuts import render, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from CrowdSourcing.hostdiscovery import site_settings
from CrowdSourcing.customlog import log_request
from DataEntry.commit import commit
from DataEntry.forms import UploadForm
from DataEntry.models import Record, RecordObject, Geography, site_contribute_geography
from DataEntry.image import process_image, get_image_size, get_image_size2, rotate_image, copy_file
from DataEntry.text import process_text
from DataEntry.audio import process_audio
from DataEntry.video import process_video
from DataEntry.solr import solr_search_query, geosolrsearch
from DataEntry.record_object_utilities import delete_record, file_ext
from DataEntry.configure import configure_site


# ==================================


def index(request):
    """
    default page for site
    @param request: not expecting many at the default level
    @return: default start page
    """
    return HttpResponseRedirect('upload')


def detail(request, record_id, slug=''):
    """
    @param request:
    @param record_id:
    @param slug:
    @return:

    Render a detail version of all the fields that were contributed asking for confirmation, deletion or further editing
    If slug == 'edit', then pass the variables to an editable form which returns to the main rendering for confirmation again.
    If slug == 'redit', then pass to edit with a flag for 'this has just been rotated'.
    """

    geodata = {}
    message = request.GET.get('m', '')
    site_values = site_settings(request)
    site_identifier = site_values['site_url']
    allowed_extensions = list_extensions(site_values)
    record = get_object_or_404(Record, pk=record_id)
    geography = Geography.objects.filter(record_id=record_id)
    geoids = ""
    geo_list = []
    geodata = ''
    for geo in geography:
        if geoids == "":
            geoids = "id:%s" % (str(geo.geonameid))
        else:
            geoids += " OR id:%s" % (str(geo.geonameid))
        geoids = "%s" % geoids
        geo_list.append(str(geo.geonameid))

    if slug == 'edit' or slug == 'redit':
        geo_checklist = site_contribute_geography.objects.using('vita').filter(site_id=site_values['VitaSiteID'])
        for geo in geo_checklist:
            if geoids == "":
                geoids = "id:%s" % (str(geo.geonameid))
            else:
                geoids += " OR id:%s" % (str(geo.geonameid))
            geoids = "%s" % geoids
    if geoids:
        geodata = solr_search_query(geoids, 'geonames')
    rotate_image_plan = ''
    if slug == 'edit' or slug == 'redit':
        rotate_image_plan = 'offer'
    # print('rotate: ', rotate)
    #log_request('64:geodata:', geodata)
    try:
        recordobject = RecordObject.objects.filter(record_id=record_id).order_by('record_object_category_id')
    except RecordObject.DoesNotExist:
        recordobject = ''
        google_map_canvas = '300'
    do_rotate = True
    for file_object in recordobject:
        file_role = int(file_object.record_object_category_id)
        # print(file_role)
        if file_role > 6:
            do_rotate = False
        elif file_role == 4 and slug == 'redit':
            rotate_image_plan = 'undo'
    # TODO: break up context elements between shared and unique to either edit or detail
    context = {
        'site_settings': site_values,
        'record': record,
        'recordobject': recordobject,
        'full': False,
        'geodata': geodata,
        'gMap': True,
        'geo_check': True,
        'geo_list': geo_list,
        'showProvince': True,
        'jQuery': True,
        'delete_dialog': True,
        'message': message,
        'rotate': rotate_image_plan,
        'do_rotate': do_rotate,
        'site_identifier': site_identifier,
        'allowed_extensions': allowed_extensions,
    }
    if slug == 'edit' or slug == 'redit':
        return render(request, 'DataEntry/edit.html', context)
    else:
        return render(request, 'DataEntry/detail.html', context)


def full(request, record_id):
    site_values = site_settings(request)
    site_identifier = site_values['site_url']
    record = get_object_or_404(Record, pk=record_id)
    try:
        recordobject = RecordObject.objects.filter(record_id=record_id, record_object_category_id=2)
        context = {
            'site_settings': site_values,
            'record': record,
            'recordobject': recordobject,
            'site_identifier': site_identifier,
            'full': True}
        return render(request, 'DataEntry/detail.html', context)
    except RecordObject.DoesNotExist:
        target = "{}{}/{}/".format(site_identifier, record_id, record.slug)
        return HttpResponseRedirect(target)


def upload(request):
    geodata = {}
    geoids = ""
    site_values = site_settings(request)
    site_id = site_values['site_id']
    site_identifier = site_values['site_url']
    # print('site_id', site_id)
    display_public = site_values['ConPublicDisplay']
    allowed_extensions = list_extensions(site_values)
    vita_url = request.GET.get('u', '')
    vita_thumb_url = request.GET.get('t', '')
    upload_action = '{}upload/'.format(site_identifier)
    message = request.GET.get('m', '')
    if message == 'delete':
        message = site_values['ConLabelDeleteConfirm']
    elif message == 'confirm':
        if display_public == '1':
            message = site_values['ConPublicMessage2']
        else:
            message = site_values['ConNonPublicMessage']
    if site_values['ConSaveOriginal']:
        save_original = site_values['ConSaveOriginal']
    else:
        save_original = '0'
    # print('save_original: ', save_original)
    geo_checklist = site_contribute_geography.objects.using('vita').filter(site_id=site_values['VitaSiteID'])
    for geo in geo_checklist:
        if geoids == "":
            geoids = "id:%s" % (str(geo.geonameid))
        else:
            geoids += " OR id:%s" % (str(geo.geonameid))
        geoids = "%s" % geoids
        # log_request("127 geoids", geoids)
    if geoids:
        geodata = solr_search_query(geoids, 'geonames')
    # for geo in geodata:
    #    log_request("id", geo)
    # log_request("128 geodata", geodata)

    new_contribution_pk = 0
    if request.method == 'POST':  # If the form has been submitted...
        turing_subj = request.POST.get('subj',
                                       '')  # on the assumption that the comment form spammer will fill out the subj form
        if len(turing_subj) < 1:
            turing_test_passed = True
        else:
            turing_test_passed = False
    else:
        turing_test_passed = False  # not strictly true, but the point is to present (or re-present an empty form)
    if turing_test_passed:
        if 'image_file' in request.FILES:
            # print("Went via RequestFiles")
            # print(request.POST)
            form = UploadForm(request.POST)  # A form bound to the POST data
            # print("Back from RequestFiles UploadForm")
            if form.is_valid():  # All validation rules pass
                # TODO:  refactor the next three lines which are repeated below
                # print("Save please")
                new_contribution_pk = form.save(request, site_id, new_contribution_pk)
                # print("Back from RequestFiles UploadForm")
                image_file_name = get_object_or_404(Record, pk=new_contribution_pk).image_file.name
                # process the  uploaded file
                file_extension = file_ext(image_file_name)
                # print(file_extension)
                if file_extension in settings.IMAGE_EXTENSIONS:
                    process_image(new_contribution_pk, image_file_name, save_original, '')
                elif file_extension in settings.TEXT_EXTENSIONS:
                    process_text(new_contribution_pk, image_file_name)
                elif file_extension in settings.AUDIO_EXTENSIONS:
                    process_audio(new_contribution_pk, image_file_name)
                elif file_extension in settings.VIDEO_EXTENSIONS:
                    process_video(new_contribution_pk, image_file_name)
                target = "{}{}/".format(site_identifier, new_contribution_pk)
                return HttpResponseRedirect(target)  # Redirect after POST
        else:
            # print("Went via RequestPOST")
            form = UploadForm(request.POST, empty_permitted=True)
            # print("Back from RequestPOST UploadForm")
            if form.is_valid():  # All validation rules pass
                # print("Form was valid")
                new_contribution_pk = form.save(request, site_id, 0)
                target = "{}{}/".format(site_identifier, new_contribution_pk)
                return HttpResponseRedirect(target)  # Redirect after POST
        return render('DataEntry/form_errors.html', {'form': form})
    else:
        form = UploadForm()  # An unbound form
    context = {
        'site_settings': site_values,
        'form': form,
        'jQuery': True,
        'gMap': True,
        'geo_check': False,
        'geodata': geodata,
        'showProvince': True,
        'vita_url': vita_url,
        'vita_thumb_url': vita_thumb_url,
        'message': message,
        'upload': True,
        'upload_action': upload_action,
        'allowed_extensions': allowed_extensions,
        'site_identifier': site_identifier,
    }
    return render(request, 'DataEntry/upload.html', context)


def update(request, record_id):
    site_values = site_settings(request)
    site_identifier = site_values['site_url']
    site_id = site_values['site_id']
    record = Record.objects.get(pk=record_id)
    # print(request.method)
    if request.method == 'POST':  # If the form has been submitted...
        form = UploadForm(request.POST, instance=record)
        if form.is_valid():  # All validation rules pass
            #    print("Form was valid")
            form.save(request, site_id, record_id, instance=record)
            target = "{}{}/".format(site_identifier, record_id)
            return HttpResponseRedirect(target)  # Redirect after POST
        return render(request, 'DataEntry/form_errors.html', {'form': form})


def delete(request, record_id):
    # TODO:  in dev environment this is throwing "BrokenPipeError: [Errno 32] Broken pipe" errors
    # TODO: probably because the deletion of the file objects is lagging behind execution
    site_values = site_settings(request)
    site_identifier = site_values['site_url']
    are_we_done = delete_record(record_id)
    # redirect to /contribute/upload
    if are_we_done == 'done':
        redirect_url = '{}upload?m=delete'.format(site_identifier)
        return HttpResponseRedirect(redirect_url)


def confirm(request, record_id):
    site_values = site_settings(request)
    site_identifier = site_values['site_url']
    data_callback_base = site_values['VitaPath']
    group_id = site_values['ConGroupID']
    confirm_error = site_values['ConLabelConfirmError']
    vita_url, vita_thumb_url = commit(record_id, group_id)
    # quit()
    if vita_url:
        are_we_done = delete_record(record_id)
        # are_we_done = 'nope'
        if are_we_done == 'done':
            redirect = '{}/upload/?u={}&t={}&m=confirm'.format(site_identifier, vita_url, vita_thumb_url)
            return HttpResponseRedirect(redirect)
        else:
            return render(request, 'DataEntry/test.html', {'results': f})
    else:
        message = quote_plus(confirm_error)
        redirect_url = '{}{}?m={}'.format(site_identifier, record_id, message)
        return HttpResponseRedirect(redirect_url)


def configure(request, vita_set, vita_site_id):
    # print('db_identifier: ', vita_set)
    # print('vita_site_id: ', vita_site_id)
    results = configure_site(vita_set, vita_site_id)
    # results="did something, maybe"
    return render(request, 'DataEntry/test.html', {'results': results})


def geosearch(request):
    # TODO: configure scoping of places by country and optionally provinces/admin1
    results = geosolrsearch(request)
    # return render(request, 'DataEntry/geo.html', {'results': results})
    return HttpResponse(results, content_type='text/plain')


def getsize(request):
    results = get_image_size(request)
    return HttpResponse(results, content_type='text/plain')


def getsize2(request):
    results = get_image_size2(request)
    return HttpResponse(results, content_type='text/plain')


def rotate(request, record_id, orientation):
    site_values = site_settings(request)
    site_identifier = site_values['site_url']
    rotate_image(record_id, orientation)
    if orientation == '1':
        redirect_url = '{}{}/edit/'.format(site_identifier, record_id)
    else:
        redirect_url = '{}{}/redit/'.format(site_identifier, record_id)
    # print('redirect_url: ', redirect_url)
    return HttpResponseRedirect(redirect_url)


def copyfile(request):
    results = copy_file(request)
    return HttpResponse(results, content_type='text/plain')


def list_extensions(site_values):
    plan_audio = site_values['ConPlanAudio']
    plan_audio = '0'
    plan_video = site_values['ConPlanVideo']
    plan_video = '0'
    allowed_extensions = []
    image_extensions = settings.IMAGE_EXTENSIONS
    text_extensions = settings.TEXT_EXTENSIONS
    audio_extensions = settings.AUDIO_EXTENSIONS
    video_extensions = settings.VIDEO_EXTENSIONS
    allowed_extensions = image_extensions + text_extensions
    if plan_audio == '1':
        allowed_extensions += audio_extensions
    if plan_video == '1':
        allowed_extensions += video_extensions
    return allowed_extensions
