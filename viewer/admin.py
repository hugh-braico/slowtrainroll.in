from django.contrib import admin
from django.db import models
from .models import Vod
from etc.admin import CustomModelPage


# Simple CSV upload page
# TODO: work out how to get the multi-file uploader widget into this page
# TODO: work out how to do input validation with this
class CsvUploadPage(CustomModelPage):
    title = 'Upload vods from csv'
    file = models.FileField('File')
    def save(self):
        add_vods_from_csv(self.bound_request.FILES['file'])
        super().save()


# Parses a csv file and adds a vod for each row
def add_vods_from_csv(f):
    from csv import DictReader
    import codecs
    from datetime import datetime
    reader = DictReader(codecs.iterdecode(f, 'utf-8'))
    for row in reader:
        # Make a copy of this row that has lowercase keys 
        temp_row = {}
        for key in row:
            temp_row[key.lower()] = row[key]
        # Check for duplicates by URL 
        # (not comprehensive, but good enough for uploading the same file twice)
        if not Vod.objects.filter(url=temp_row['url']):
            # Convert 0/1 to false/true
            temp_row['netplay'] = (temp_row['netplay'] == 1)
            # Parse out the date field from string
            temp_row['date'] = datetime.strptime(temp_row['date'], '%d/%m/%Y').date()
            # Construct and add a vod that uses all this row's values
            v = Vod(**temp_row)
            v.save()


# just extra little navigation bits in the vod admin screen
class VodAdmin(admin.ModelAdmin):
    list_filter   = ['date', 'region', 'version', 'event']
    search_fields = ['p1name', 'p1char1', 'p1char2', 'p1char3', 
                     'p2name', 'p2char1', 'p2char2', 'p2char3', 
                     'event']


admin.site.register(Vod, VodAdmin)
CsvUploadPage.register()
