import re
import html
from csv import DictReader
import codecs
from datetime import datetime

from django.contrib import admin
from django.db import models
from .models import Vod, required_columns, character_choices, region_list, version_list
from etc.admin import CustomModelPage


# Simple CSV upload page
class CsvUploadPage(CustomModelPage):
    title = 'Upload vods from csv'
    file = models.FileField('file')
    def save(self):
        # Parse out all the csv rows into Vods, but if any of them are invalid,
        # reject the whole file with an error message.
        try:
            parsed_vods = parse_vods_from_csv(self.bound_request.FILES['file'])
            for v in parsed_vods:
                v.save()
        except Exception as err: 
            self.bound_admin.message_error(self.bound_request, str(err))
        else:
            super().save()


# Parses a csv file and returns a list of Vod
def parse_vods_from_csv(f):
    reader = DictReader(codecs.iterdecode(f, 'utf-8'))
    parsed_vods = []
    row_number = 0
    for row in reader:
        row_number += 1
        # Make a copy of this row that has lowercase keys 
        temp_row = {}
        for key in row:
            temp_row[key.lower()] = row[key]

        # Check for duplicates by URL (not totally comprehensive, but good 
        # enough for uploading the exact same row twice)
        if Vod.objects.filter(url=temp_row['url']):
            raise ValueError(f"""ERROR: row {row_number}: duplicate url {html.escape(temp_row['url'])} already exists in database""")

        # Don't allow <> in URLs as a rudimentary html injection defense
        if re.search('[<>]', temp_row['url']):
            raise ValueError(f"""ERROR: row {row_number}: invalid url '{html.escape(temp_row['url'])}'""")

        # Check for any missing or blank column values
        for column in required_columns:
            if column not in temp_row: 
                raise ValueError(f"ERROR: row {row_number}: missing column value '{column}'")
            if temp_row[column] == '': 
                raise ValueError(f"ERROR: row {row_number}: empty column value '{column}'")

        # Restrict player names and events to a sane set of characters
        for pname in ['p1name', 'p2name', 'event']:
            if not re.fullmatch('[a-zA-Z0-9-_&%;:?, ]+', temp_row[pname]):
                raise ValueError(f"""ERROR: row {row_number}: invalid {pname} '{html.escape(temp_row[pname])}'""")

        # Check every character in each team is a valid character
        valid_characters = [shortname for shortname, longname in character_choices]
        for char in ['p1char1', 'p1char2', 'p1char3', 'p2char1', 'p2char2', 'p2char3']: 
            if temp_row[char] not in valid_characters:
                raise ValueError(f"""ERROR: row {row_number}: invalid {char} '{html.escape(temp_row[char])}'""")

        # Check the regions are all valid places on Earth to live in
        if temp_row['region'] not in region_list:
            raise ValueError(f"""ERROR: row {row_number}: invalid region '{html.escape(temp_row['region'])}'""")

        # Check the version is an actual version that exists
        if temp_row['version'] not in version_list:
            raise ValueError(f"""ERROR: row {row_number}: invalid version '{html.escape(temp_row['version'])}'""")

        # The netplay flag must be either 0 or 1
        if temp_row['netplay'] not in ['0', '1']:
            raise ValueError(f"""ERROR: row {row_number}: invalid netplay flag '{html.escape(temp_row['netplay'])}'""")

        # Convert netplay flag 0/1 to false/true
        temp_row['netplay'] = (temp_row['netplay'] == 1)

        # Parse out the date field from string
        temp_row['date'] = datetime.strptime(temp_row['date'], '%d/%m/%Y').date()

        # Construct and add a vod that uses all this row's values
        parsed_vods.append(Vod(**temp_row))

    # Check none of the parsed vods are duplicates of each other by URL
    parsed_urls = [v.url for v in parsed_vods]
    for url in parsed_urls:
        if parsed_urls.count(url) > 1:
            raise ValueError(f"ERROR: file contains duplicate URL '{html.escape(url)}'")

    return parsed_vods


# just extra little navigation bits in the vod admin screen
class VodAdmin(admin.ModelAdmin):
    list_filter   = ['date', 'region', 'version', 'event']
    search_fields = ['p1name', 'p1char1', 'p1char2', 'p1char3', 
                     'p2name', 'p2char1', 'p2char2', 'p2char3', 
                     'event']


admin.site.register(Vod, VodAdmin)
CsvUploadPage.register()
