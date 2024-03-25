__author__ = 'walter'

import os
import requests
import subprocess
from django.conf import settings
from DataEntry.record_object_utilities import make_file_name, add_record_object, delete_file, file_ext
from DataEntry.lmimetypes import mime
from DataEntry.image import make_alternate_image
from CrowdSourcing.customlog import log_request


def process_text(record_id, upload_file_name):
    source_file = settings.MEDIA_ROOT + '/' + upload_file_name
    file_extension = file_ext(source_file)
    # if a pdf generate a thumb
    if file_extension == 'pdf':
        intermediate_source_file_as_jpeg = pdf_convert_to_jpeg(source_file)
        # make thumb using pillow
        target_file = make_file_name(record_id, 'thumb')
        make_alternate_image(intermediate_source_file_as_jpeg, target_file, 'thumb', record_id, '0')

        target_file = make_file_name(record_id, 'regular')
        make_alternate_image(intermediate_source_file_as_jpeg, target_file, 'regular', record_id, '0')
        #clean up the intermediate file
        delete_file(intermediate_source_file_as_jpeg, '')

    # extract text
    target_file = make_file_name(record_id, file_extension)
    fulltext = extract_text(source_file)
    record_object_category_id = settings.TEXT_RECORD_OBJECT_CATEGORY
    os.renames(source_file, target_file)
    add_record_object(record_id, record_object_category_id, target_file, source_file, fulltext)


def extract_text(upload_file_name):
    file_extension = file_ext(upload_file_name)
    mt = mime(file_extension)
    with open(upload_file_name, mode='rb') as fh:
        mydata = fh.read()
        r = requests.put('http://172.18.2.9:9998/tika',
                         data=mydata,
                         headers={'content-type': mt},
                         params={'file': upload_file_name})
    results = r.text
    # log_request("text[44] tika_results: ", results)
    return results


def pdf_convert_to_jpeg(source_file):
    source_page_one = source_file+'[0]'
    intermediate_source_file_as_jpeg = source_file.replace('.pdf', '.jpg')
    # reduce size
    # with Image(filename=source_page_one) as original:
        # convert to jpeg
    #    with original.convert('jpeg') as converted:
    #        converted.save(filename=intermediate_source_file_as_jpeg)
    #        return intermediate_source_file_as_jpeg
    gs_args = "%s -sDEVICE=jpeg -r72x72 -dFirstPage=1 -dLastPage=1 -o %s %s"  % (settings.GHOSTSCRIPT_PATH, intermediate_source_file_as_jpeg, source_page_one)
    subprocess.call(gs_args, shell=True)
    return intermediate_source_file_as_jpeg
