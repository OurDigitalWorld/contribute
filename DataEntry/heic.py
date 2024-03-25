import re
from wand.image import Image
from CrowdSourcing.customlog import log_request


def process_heic(source_file):
    log_request('source_file', source_file)
    target_file = re.sub("(?i).heic", ".png", source_file)
    log_request('target_file', target_file)
    img = Image(filename=source_file)
    log_request('HEIC (11): got to line 11', '')
    img.format = 'PNG'
    img.save(filename=target_file)
    img.close()
    return target_file
