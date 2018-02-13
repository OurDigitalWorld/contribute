
import urllib.request
import io
import warnings
from django.conf import settings
from DataEntry.record_object_utilities import make_file_name, add_record_object
from PIL import Image
_imaging = Image.core


def process_image(record_id, upload_file_name):
    source_file = settings.MEDIA_ROOT + '/' + upload_file_name

    target_file = make_file_name(record_id, 'thumb')
    make_alternate_image(source_file, target_file, 'thumb', record_id)

    target_file = make_file_name(record_id, 'regular')
    make_alternate_image(source_file, target_file, 'regular', record_id)

    target_file = make_file_name(record_id, 'full')
    make_alternate_image(source_file, target_file, 'full', record_id)


def make_alternate_image(source_file, target_file, file_type, record_id):
    file_size = 0, 0
    record_object_category_id = 0
    file_quality = 0
    if file_type == 'thumb':
        file_size = settings.THUMBNAIL_SIZE
        file_quality = settings.THUMBNAIL_QUALITY
        record_object_category_id = settings.THUMBNAIL_RECORD_OBJECT_CATEGORY
    elif file_type == 'regular':
        file_size = settings.REGULAR_SIZE
        file_quality = settings.REGULAR_QUALITY
        record_object_category_id = settings.REGULAR_RECORD_OBJECT_CATEGORY
    elif file_type == 'full':
        file_size = settings.FULL_SIZE
        file_quality = settings.FULL_QUALITY
        record_object_category_id = settings.FULL_RECORD_OBJECT_CATEGORY
    img = Image.open(source_file)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.thumbnail(file_size, Image.ANTIALIAS)
    img.save(target_file, 'JPEG', quality=file_quality)
    add_record_object(record_id, record_object_category_id, target_file, source_file, '')


def get_image_size(request):
    warnings.simplefilter('ignore', Image.DecompressionBombWarning)
    url = request.GET.get('url', '')
    source_file = io.BytesIO(urllib.request.urlopen(url).read())
    img = Image.open(source_file)
    if img.mode != "RGB":
        img = img.convert("RGB")
    size_values = img.size
    # return height, then width
    return_string = '%s,%s' % (size_values[1], size_values[0])
    return return_string


def get_image_size2(request):
    source_file = ''
    warnings.simplefilter('ignore', Image.DecompressionBombWarning)
    url = request.GET.get('url', '')
    filepath = request.GET.get('fp', '')
    if url:
        # url = 'http://www.maritimehistoryofthegreatlakes.ca/temp/36-4-1934.jp2'
        source_file = io.BytesIO(urllib.request.urlopen(url).read())
    elif filepath:
        source_file = filepath
    img = Image.open(source_file)
    if img.mode != "RGB":
        img = img.convert("RGB")
    sizevalues = img.size
    # return height, then width
    return_string = '%s,%s' % (sizevalues[1], sizevalues[0])
    return return_string
