import os
import sys

path = 'E:\django\contribute_vitacollections'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'CrowdSourcing.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
