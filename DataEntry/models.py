from django.db import models
import datetime
import os.path
from django.template.defaultfilters import slugify


class Right(models.Model):
    id = models.BigAutoField(primary_key=True)
    cccode = models.CharField('Creative Commons code', max_length=10)
    cc_label = models.CharField(null=True, max_length=30)
    cc_description = models.TextField(null=True)
    cc_url = models.URLField(null=True)

    def __str__(self):
        return self.cccode


class Record(models.Model):
    id = models.BigAutoField(primary_key=True)
    agency_id = models.IntegerField(null=True)
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    contributor = models.CharField(max_length=256, null=True, blank=True)
    contributor_email = models.EmailField(null=True, blank=True)
    contributor_name_permission = models.BooleanField(default=False)
    rights = models.ForeignKey(Right, null=True, blank=True, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    image_file = models.FileField(max_length=256, upload_to='project/', null=True, blank=True)
    full_text = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=60, blank=True)

    def __str__(self):
        return self.title

    def server_date_added(self):
        return self.date_added - datetime.timedelta(hours=5)

    def thumbnail(self):
        return RecordObject(record=self, record_object_category_id=0).file_name

    @property
    def filename(self):
        # return os.path.basename(self.image_file.name)
        return self.image_file.path

    def save(self, *args, **kwargs):
        if not self.id:
            # Only set the slug when the Record is created
            self.slug = slugify(self.title)
        super(Record, self).save()


class RecordObject(models.Model):
    id = models.BigAutoField(primary_key=True)
    record = models.ForeignKey(Record, null=False, on_delete=models.DO_NOTHING)
    record_object_category_id = models.IntegerField()
    file_name = models.CharField(max_length=256)
    thumbnail = models.CharField(max_length=256, null=True)
    original_file_name = models.CharField(max_length=256, null=True)
    large_file_name = models.CharField(max_length=256, null=True)
    object_height = models.IntegerField(null=True)
    object_width = models.IntegerField(null=True)
    file_size = models.BigIntegerField(null=True)
    file_type = models.CharField(max_length=10, null=True)
    zoomify_folder = models.CharField(max_length=256, null=True)
    full_text = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Site(models.Model):
    id = models.BigAutoField(primary_key=True)
    site_name = models.CharField(max_length=256, null=False)
    site_url = models.CharField(max_length=256, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    group_identifier = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.site_name


class SiteSetup(models.Model):
    id = models.BigAutoField(primary_key=True)
    site = models.ForeignKey(Site, null=False, on_delete=models.DO_NOTHING)
    afield = models.CharField(max_length=50, null=False)
    avalue = models.TextField(null=True)


class Geography(models.Model):
    id = models.BigAutoField(primary_key=True)
    record = models.ForeignKey(Record, on_delete=models.DO_NOTHING)
    geonameid = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    relationship = models.CharField(max_length=20, null=True, blank=True)


class site_contribute_geography(models.Model):
    id = models.BigAutoField(primary_key=True)
    geonameid = models.IntegerField(primary_key=False)
    name = models.CharField(max_length=200, blank=True, null=True)
    site_id = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'site_contribute_geography'
