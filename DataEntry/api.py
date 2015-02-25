__author__ = 'walter'

from tastypie.resources import ModelResource
from tastypie import fields
from DataEntry.models import Record, RecordObject, Geography, Right


class RecordObjectResource(ModelResource):
    record = fields.ToOneField('DataEntry.api.RecordResource', 'record', null=True, blank=True)

    class Meta:
        queryset = RecordObject.objects.all()
        resource_name = 'recordobject'


class GeographyResource(ModelResource):
    record = fields.ToOneField('DataEntry.api.RecordResource', 'record', null=True, blank=True)

    class Meta:
        queryset = Geography.objects.all()
        resource_name = 'geography'


class RightsResource(ModelResource):

    class Meta:
        queryset = Right.objects.all()
        resource_name = 'right'


class RecordResource(ModelResource):
    recordobject = fields.ToManyField(
        RecordObjectResource, 'recordobject_set',
        related_name='record',
        full=True,
        null=True,
        blank=True)
    geography = fields.ToManyField(
        GeographyResource,
        'geography_set',
        related_name='record',
        full=True,
        null=True,
        blank=True)
    right = fields.CharField(attribute='rights__cccode')

    class Meta:
        queryset = Record.objects.all()
        resource_name = 'record'
        excludes = ['agency_id', 'date_modified', 'slug']
        allowed_methods = ['get']