__author__ = 'walter'

import os
import requests
import subprocess
from django.conf import settings
from DataEntry.record_object_utilities import make_file_name, add_record_object, delete_file, file_ext
from CrowdSourcing.customlog import log_request


def process_video(record_id, upload_file_name):
    source_file = settings.MEDIA_ROOT + '/' + upload_file_name
    file_extension = file_ext(source_file)
    target_file = make_file_name(record_id, file_extension)

    # extract text would be nice
    fulltext = ''

    record_object_category_id = settings.VIDEO_RECORD_OBJECT_CATEGORY
    os.renames(source_file, target_file)
    add_record_object(record_id, record_object_category_id, target_file, source_file, fulltext)
