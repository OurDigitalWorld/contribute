__author__ = 'walter'

import logging
from datetime import datetime

logger = logging.getLogger('django.request')

def log_request(variable, error_request):
    dt = "{:%d %B %Y %H:%M:%S}".format(datetime.now())
    log_string = '%s:  %s: [%s]' % (dt, variable, error_request)
    logger.error(log_string)