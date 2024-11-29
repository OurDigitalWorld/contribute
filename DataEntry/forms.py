__author__ = 'walter'
from django import forms
from django.utils.html import strip_tags
from DataEntry.models import Record, Geography


class UploadForm(forms.ModelForm):
    title = forms.CharField(max_length=256)
    description = (forms.CharField
                   (widget=forms.Textarea(),  required=False))
    full_text = forms.CharField(widget=forms.Textarea(),  required=False)
    contributor = forms.CharField(max_length=256)
    contributor_email = forms.EmailField(required=False)
    contributor_name_permission = forms.BooleanField(required=False)
    image_file = forms.FileField(
        label="Pick a file",
        help_text="max. 42 MBs",
        required=False
    )

    def save(self, request, site_id, record_id, *args, **kwargs):
        record_id = int(record_id)
        post = super(UploadForm, self).save(commit=False)
        if record_id > 0:
            post.record_id = record_id
        post.title = scrub_html(request.POST.get('title'))
        post.description = clean_content(request.POST.get('description'))
        post.full_text = request.POST.get('full_text')
        post.contributor = request.POST.get('contributor')
        post.contributor_email = request.POST.get('contributor_email')
        if request.POST.get('contributor_name_permission') == 'True':
            post.contributor_name_permission = True
        else:
            post.contributor_name_permission = False
        if record_id == 0:
            post.image_file = request.FILES.get('image_file')
        post.agency_id = site_id
        post.save()
        if record_id == 0:
            record_id = post.pk
        geonameids = request.POST.getlist('geonameid')
        Geography.objects.filter(record_id=record_id).delete()
        for gid in geonameids:
            if gid != '':
                new_gn = Geography(
                    record_id=record_id,
                    geonameid=gid
                )
                new_gn.save()
        return record_id

    class Meta:
        model = Record
        fields = ['title',
                  'description',
                  'full_text',
                  'contributor',
                  'contributor_email',
                  'rights',
                  'contributor_name_permission']
        exclude = ['agency_id',
                   'slug',
                   'image_file']

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        # Call to ModelForm constructor
        self.fields['title'].widget.attrs['size'] = 80
        self.fields['title'].widget.attrs['class'] = 'title'
        self.fields['description'].widget.attrs['rows'] = 10
        self.fields['description'].widget.attrs['cols'] = 70
        self.fields['description'].widget.attrs['class'] = 'description'
        self.fields['full_text'].widget.attrs['rows'] = 10
        self.fields['full_text'].widget.attrs['cols'] = 70
        self.fields['full_text'].widget.attrs['class'] = 'full_text'
        self.fields['contributor'].widget.attrs['size'] = 80
        self.fields['contributor'].widget.attrs['class'] = 'contributor'
        self.fields['contributor_email'].widget.attrs['size'] = 80


def clean_content(content_string):
    output_string = ''
    if content_string:
        output_string = strip_tags(content_string)
    return output_string


def scrub_html(content_string):
    if content_string:
        output_string = strip_tags(content_string)
        return output_string
