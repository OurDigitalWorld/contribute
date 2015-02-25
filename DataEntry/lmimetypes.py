__author__ = 'walter'

#import mimetypes

def mime(fe):
    mime_types = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'doc': 'application/msword',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'xltx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.template',
        'potx': 'application/vnd.openxmlformats-officedocument.presentationml.template',
        'ppsx': 'application/vnd.openxmlformats-officedocument.presentationml.slideshow',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'sldx': 'application/vnd.openxmlformats-officedocument.presentationml.slide',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'dotx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.template',
        'xlam': 'application/vnd.ms-excel.addin.macroEnabled.12'
    }

    return mime_types[fe]