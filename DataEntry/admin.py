from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.timezone import activate
#activate(settings.TIMEZONE)

from DataEntry.models import Right
admin.site.register(Right)


from DataEntry.models import Record

class RecordAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Object', {'fields': ['title', 'description', 'full_text']}),
        ('Contributor', {'fields': ['contributor', 'contributor_email']}),
        ('other stuff', {'fields': ['rights', 'image_file'], 'classes': ['collapse']})
    ]
    list_display = ['title', 'contributor', 'server_date_added']
    list_filter = ['date_added']
admin.site.register(Record, RecordAdmin)


from DataEntry.models import Site
admin.site.register(Site)


from DataEntry.models import SiteSetup

class SiteSetupAdmin(admin.ModelAdmin):
    list_display = ['site', 'afield', 'avalue']
admin.site.register(SiteSetup, SiteSetupAdmin)
