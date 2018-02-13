__author__ = 'walter'

import os
from PIL import Image
from django.conf import settings
from DataEntry.models import RecordObject, Record


def make_file_name(file_id, file_type):
    """
    generate a distinct thumb filename for a given file; assume the id of the generated record
    """
    file_extension = ''
    if file_type == 'thumb':
        file_extension = settings.THUMBNAIL_EXTENSION
    elif file_type == 'regular':
        file_extension = settings.REGULAR_EXTENSION
    elif file_type == 'full':
        file_extension = settings.FULL_EXTENSION
    elif file_type == 'pdf':
        file_extension = 't.pdf'

    n = str(file_id)
    file_name = "%s%s%s%s" % (settings.PROJECT_MEDIA_ROOT, settings.FILE_PREFIX, n.zfill(9), file_extension)
    return file_name


def add_record_object(record_id, record_object_category_id, target_file, source_file, fulltext=''):
    # add to database RecordObjects
    file_type = ''
    object_width = 0
    object_height = 0
    file_name = target_file.replace(settings.PROJECT_MEDIA_ROOT, '')
    original_file_name = source_file.replace(settings.PROJECT_MEDIA_ROOT, '')
    if record_object_category_id == 1 \
            or record_object_category_id == 2 \
            or record_object_category_id == 3 \
            or record_object_category_id == 0:
        img = Image.open(target_file)
        object_width = img.size[0]
        object_height = img.size[1]
        file_type = img.format
    file_size = os.path.getsize(target_file)
    if not file_type:
        # if not an image use the file extension
        file_type = os.path.splitext(target_file)[1][1:].upper()
    new_ro = RecordObject(
        record_id=record_id,
        object_width=object_width,
        object_height=object_height,
        record_object_category_id=record_object_category_id,
        file_name=file_name,
        file_type=file_type,
        file_size=file_size,
        original_file_name=original_file_name,
        full_text=fulltext
    )
    new_ro.save()


def delete_record(record_id):
    # start by finding binaries objects and deleting them
    are_we_done_yet = delete_record_objects(record_id)
    # delete (cascade) the record
    if are_we_done_yet == 'done':
        Record.objects.filter(pk=record_id).delete()
        return 'done'


def delete_record_objects(record_id):
    # find and delete all objects attached to that record
    delete_file_list = RecordObject.objects.filter(record_id=record_id)
    for file in delete_file_list:
        file_name = file.file_name
        delete_file(file_name, settings.PROJECT_MEDIA_ROOT)
    # find and delete uploaded file
    uploaded_file_record = Record.objects.get(pk=record_id)
    # for file in uploaded_file_list:
    file_name = uploaded_file_record.image_file
    if file_name:
        upload_path = "%s/" % settings.MEDIA_ROOT  # because MEDIA_ROOT is slashless
        delete_file(file_name, upload_path)
    return "done"


def delete_file(file_name, path):
    file_path = "%s%s" % (path, file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)
