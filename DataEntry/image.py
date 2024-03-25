
import urllib.request
import io
import os
import warnings
import subprocess
from PIL import Image, ImageCms
_imaging = Image.core
from django.conf import settings
from CrowdSourcing.customlog import log_request
from DataEntry.models import RecordObject
from DataEntry.record_object_utilities import make_file_name, add_record_object, delete_file, file_ext
from DataEntry.heic import process_heic


def process_image(record_id, upload_file_name, save_original, orientation):
    skip_original = False
    intermediate_file = ''
    if orientation == '':
        orientation = 0
    source_file = settings.MEDIA_ROOT + '/' + upload_file_name
    file_extension = file_ext(source_file)
    # log_request("Image.21 file_extension", file_extension)
    original_file = source_file
    if file_extension == 'heic':
        # Convert file to Tiff
        source_file = process_heic(source_file)
        intermediate_file = source_file

    target_file = make_file_name(record_id, 'thumb')
    make_alternate_image(source_file, target_file, 'thumb', record_id, orientation)

    target_file = make_file_name(record_id, 'regular')
    make_alternate_image(source_file, target_file, 'regular', record_id, orientation)

    target_file = make_file_name(record_id, 'full')
    skip_original = make_alternate_image(source_file, target_file, 'full', record_id, orientation)

    if skip_original == False:
        target_file = make_file_name(record_id, 'original')
        make_copy_image(original_file, target_file, record_id)

    # if there is an intermediate file, drop it now
    if intermediate_file:
        delete_file(intermediate_file, '')


def make_alternate_image(source_file, target_file, file_type, record_id, orientation):
    orientation = int(orientation)
    do_rotation = False
    if orientation > 1:
        do_rotation = True
    file_size = 0, 0
    record_object_category_id = 0
    file_quality = 0
    process_with_pillow = '1'
    skip_original = False
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
    file_extension = file_ext(source_file)
    img = Image.open(source_file)

    if orientation == 0:
        try:
            exif = dict(img._getexif().items())
            if exif[274]:
                orientation = exif[274]
        except:
            one = 1
    # print('62:', orientation)
    if orientation == 3:
        img = img.rotate(180, expand=True)
    elif orientation == 6:
        img = img.rotate(270, expand=True)
    elif orientation == 8:
        img = img.rotate(90, expand=True)
    if img.mode != "RGB":
        img = img.convert("RGB")
    image_width, image_height = img.size
    if file_type == 'full':
        if file_extension == 'jp2':
            target_file = target_file.replace('.jpg', '.jp2')
            target_file = target_file.replace('.jpeg', '.jp2')
            process_with_pillow = '0'
            skip_original = True
            img.close()
            os.rename(source_file, target_file)
        elif image_width > 1600 or image_height > 1600:
            process_with_pillow = '0'
            # and fire up kdu_compress
            target_file = target_file.replace('.jpg', '.jp2')
            target_file = target_file.replace('.jpeg', '.jp2')
            jp2_compress(source_file, target_file)
        elif file_extension == 'png':
            target_file = target_file.replace('.jpg', '.png')
            process_with_pillow = '0'
            if do_rotation:
                img.save(target_file, 'PNG')
            else:
                img.close()
                os.rename(source_file, target_file)
            skip_original = True
        elif file_extension == 'jpg' or file_extension == 'jpeg':
            process_with_pillow = '0'
            if do_rotation:
                img.save(target_file, 'JPEG')
            else:
                img.close()
                os.rename(source_file, target_file)
            skip_original = True
    if process_with_pillow == '1':
        img.thumbnail(file_size, Image.ANTIALIAS)
        img.save(target_file, 'JPEG', quality=file_quality)
    add_record_object(record_id, record_object_category_id, target_file, source_file, '')
    return skip_original


def make_copy_image(source_file, target_file, record_id):
    file_extension = file_ext(source_file)
    target_file = "%s.%s" % (target_file, file_extension)
    os.rename(source_file, target_file)
    add_record_object(record_id, 4, target_file, source_file, '')


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


def mode_convert(image_file_path):
    img_mode = Image.open(image_file_path)
    # log_request('img_mode.mode', img_mode.mode)
    file_extension = file_ext(image_file_path)
    if file_extension == 'tif' or file_extension == 'tiff':
        del img_mode.tag[347]
    if img_mode.mode == "RGBA":
        img_mode = img_mode.convert("RGB")
    elif img_mode.mode != "RGB":
        img_mode = img_mode.convert("RGB")
    return img_mode


def jp2_compress(source_file, target_file):
    temp_file_name = target_file.replace('jp2', 'tif')
    problem_file = temp_file_name.replace(settings.MEDIA_ROOT, settings.PROBLEM_PATH)
    kdu = settings.KAKADU_PATH
    file_extension = file_ext(source_file)
    # log_request('file_extension',file_extension.lower())
    if file_extension == 'tif' or file_extension == 'tiff' or file_extension == 'gif':
        img2 = mode_convert(source_file)
    else:
        img2 = Image.open(source_file)
    # log_request('got to line 122',temp_file_name)
    try:
        log_request('source ICC:', img2.info.get('icc_profile'))
        data = list(img2.getdata())
        image_without_exif = Image.new(img2.mode, img2.size)
        image_without_exif.putdata(data)
        image_without_exif.save(temp_file_name, 'TIFF', compression=None)
        # img2.save(temp_file_name, 'TIFF', compression=None, icc_profile=img2.info.get('icc_profile'))
        img_tiff = Image.open(source_file)
        # log_request('TIFF ICC:', img_tiff.info.get('icc_profile'))
        try:
            kdu_args = '%s -i %s -o %s -rate 1.0' % (kdu, temp_file_name, target_file)
            # log_request('file_extension',file_extension.lower())
            log_request('kdu_args', kdu_args)
            subprocess.call(kdu_args, shell=True)
            os.remove(temp_file_name)
        except OSError:
            img_tiff.close()
            os.rename(source_file, problem_file)
    except RuntimeError:
        img2.close()
        os.rename(source_file, problem_file)


def rotate_image(record_id, orientation):
    image_file_name_qs = RecordObject.objects.filter(record_id=record_id,record_object_category_id=4).only('file_name')
    if not image_file_name_qs:
        image_file_name_qs = RecordObject.objects.filter(record_id=record_id,record_object_category_id=2).only('file_name')
    save_original = ''
    for ro_file_name in image_file_name_qs:
        image_file_name = 'project/%s' % ro_file_name.file_name
        process_image(record_id, image_file_name, save_original, orientation)
    return 'ok'


def copy_file(request):
    file_name = request.GET.get('fn', '')
    target_file_path = request.GET.get('tp', '')
    root = settings.PROJECT_MEDIA_ROOT.replace('/','\\')
    copy_plan = "copy %s%s %s" % (root, file_name, target_file_path)
    # print("copyplan: ", copy_plan)
    os.popen(copy_plan)
    return 'ok'