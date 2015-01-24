__author__ = 'walter'
from PIL import Image
_imaging = Image.core
import os
import urllib.request,io
import warnings
from django.conf import settings
from DataEntry.record_object_utilities import make_file_name, add_record_object


def process_image(record_id, upload_file_name):
    source_file = settings.MEDIA_ROOT +'/'+ upload_file_name

    target_file = make_file_name(record_id, 'thumb')
    make_alternate_image(source_file, target_file, 'thumb', record_id)

    target_file = make_file_name(record_id, 'regular')
    make_alternate_image(source_file, target_file, 'regular', record_id)

    target_file = make_file_name(record_id, 'full')
    make_alternate_image(source_file, target_file, 'full', record_id)


def make_alternate_image(source_file, target_file, type, record_id):
    if type == 'thumb':
        file_size = settings.THUMBNAIL_SIZE
        file_quality = settings.THUMBNAIL_QUALITY
        record_object_category_id = settings.THUMBNAIL_RECORD_OBJECT_CATEGORY
    elif type == 'regular':
        file_size = settings.REGULAR_SIZE
        file_quality = settings.REGULAR_QUALITY
        record_object_category_id = settings.REGULAR_RECORD_OBJECT_CATEGORY
    elif type == 'full':
        file_size = settings.FULL_SIZE
        file_quality = settings.FULL_QUALITY
        record_object_category_id = settings.FULL_RECORD_OBJECT_CATEGORY
    img = Image.open(source_file)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.thumbnail((file_size), Image.ANTIALIAS)
    img.save(target_file, 'JPEG', quality = file_quality)
    add_record_object(record_id, record_object_category_id, target_file, source_file, '')


def get_image_size(request):
    warnings.simplefilter('ignore', Image.DecompressionBombWarning)
    url = request.GET.get('url','')
    #url = 'http://www.maritimehistoryofthegreatlakes.ca/temp/36-4-1934.jp2'
    source_file = io.BytesIO(urllib.request.urlopen(url).read())
    img = Image.open(source_file)
    if img.mode != "RGB":
        img = img.convert("RGB")
    sizevalues = img.size
    #return height, then width
    return_string = '%s,%s' % (sizevalues[1], sizevalues[0])
    return return_string

