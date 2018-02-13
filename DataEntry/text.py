__author__ = 'walter'

import os
import requests
from wand.image import Image
from django.conf import settings
from DataEntry.record_object_utilities import make_file_name, add_record_object
from DataEntry.lmimetypes import mime
from DataEntry.image import make_alternate_image


def process_text(record_id, upload_file_name):
    source_file = settings.MEDIA_ROOT + '/' + upload_file_name
    file_extension = os.path.splitext(source_file)[1][1:]
    # if a pdf generate a thumb
    if file_extension.lower() == 'pdf':
        intermediate_source_file_as_jpeg = pdf_convert_to_jpeg(source_file)
        # make thumb using pillow
        target_file = make_file_name(record_id, 'thumb')
        make_alternate_image(intermediate_source_file_as_jpeg, target_file, 'thumb', record_id)

        target_file = make_file_name(record_id, 'regular')
        make_alternate_image(intermediate_source_file_as_jpeg, target_file, 'regular', record_id)

    # extract text
    target_file = make_file_name(record_id, 'pdf')
    fulltext = extract_text(source_file)
    record_object_category_id = settings.TEXT_RECORD_OBJECT_CATEGORY
    os.renames(source_file, target_file)
    add_record_object(record_id, record_object_category_id, target_file, source_file, fulltext)


def extract_text(upload_file_name):
    file_extension = os.path.splitext(upload_file_name)[1][1:]
    mt = mime(file_extension)
    with open(upload_file_name, mode='rb') as fh:
        mydata = fh.read()
        r = requests.put('http://172.18.2.9:9998/tika',
                         data=mydata,
                         headers={'content-type': mt},
                         params={'file': upload_file_name})
    results = r.text
    return results


def pdf_convert_to_jpeg(source_file):
    source_page_one = source_file+'[0]'
    intermediate_source_file_as_jpeg = source_file.replace('.pdf', '.jpg')
    # reduce size
    with Image(filename=source_page_one) as original:
        # convert to jpeg
        with original.convert('jpeg') as converted:
            converted.save(filename=intermediate_source_file_as_jpeg)
            return intermediate_source_file_as_jpeg
