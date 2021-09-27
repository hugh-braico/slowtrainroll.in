from django.db import models
import datetime

# list of valid characters (Following the same naming as TWB)
character_choices = [
    ( "N", "None"),
    ("AN", "Annie"),
    ("BW", "Beowulf"),
    ("BB", "Big Band"),
    ("CE", "Cerebella"),
    ("DB", "Double"),
    ("EL", "Eliza"),
    ("FI", "Filia"),
    ("FU", "Fukua"),
    ("MF", "Ms. Fortune"),
    ("PW", "Painwheel"),
    ("PS", "Parasoul"),
    ("PC", "Peacock"),
    ("RF", "Robo-Fortune"),
    ("SQ", "Squigly"),
    ("UM", "Umbrella"),
    ("VA", "Valentine")
]

character_dict = dict(character_choices)

# list of regions (Following the same naming as TWB)
region_list = [
    "Europe", 
    "Asia", 
    "North America", 
    "Oceania", 
    "South America"
]

# list of Skullgirls versions (Following the same naming as TWB)
# https://github.com/Servan42/TWB_Parser/blob/master/List_of_CharactersCode_Regions_Versions.md
version_list = [
    'Annie Patch',
    'Annie Patch Beta',
    '2E+ Final',
    '2E+ (old UD)',
    '2E', # aka. Robo-Fortune Patch
    'Beowulf Patch',
    'Eliza Patch',
    'Fukua Patch',
    'Big Band Patch',
    'Encore',
    'MDE',
    'SDE'
    # Note: there are no "Vanilla" vods on TWB, SDE is the earliest
]

# all vod column values
required_columns = [
    'event', 'date', 'region', 'netplay', 'version',
    'p1name', 'p1char1', 'p1char2', 'p1char3',
    'p2name', 'p2char1', 'p2char2', 'p2char3',
    'url'
]

# Standard TWB csv header
def csv_header():
    return "Event,Date,Region,Netplay,Version," \
           "P1Name,P1Char1,P1Char2,P1Char3," \
           "P2Name,P2Char1,P2Char2,P2Char3,URL"


# Represents one link to a vod/timestamp + relevant information about the set
class Vod(models.Model): 
    event   = models.CharField('Event', max_length=64)
    date    = models.DateField('Date')
    region  = models.CharField('Region', max_length=16)
    netplay = models.BooleanField('Netplay')
    version = models.CharField('Version', max_length=64)
    p1name  = models.CharField('P1Name', max_length=32)
    p1char1 = models.CharField('P1Char1', max_length=4)
    p1char2 = models.CharField('P1Char2', max_length=4)
    p1char3 = models.CharField('P1Char3', max_length=4)
    p2name  = models.CharField('P2Name', max_length=32)
    p2char1 = models.CharField('P2Char1', max_length=4)
    p2char2 = models.CharField('P2Char2', max_length=4)
    p2char3 = models.CharField('P2Char3', max_length=4)
    url     = models.CharField('URL', max_length=256)

    # brief string summary, eg. "[2021-09-08, Ranbats] SeaJay vs Neffy"
    def __str__(self):
        return f"""[{self.date.strftime('%Y-%m-%d')}, {self.event}] {self.p1name} vs {self.p2name}"""

    def team_cell_html(self, team, icon_dir):
        team = filter(lambda x: x != "N", team)
        return "".join(self.team_icon_html(char, icon_dir) for char in team)
    
    def team_icon_html(self, char, icon_dir):
        # Avoid key error
        if char in character_dict:
            return f'<span class="icon {char}" style="background-image:url(/static/viewer/icons_{icon_dir}/{char}.png)" role="img" aria-label="{character_dict[char]}" title="{character_dict[char]}"></span>'
        else:
            return ''

    # HTML table row that displays all the info about this vod
    def table_row_html(self, icon_dir):
        p1team = self.team_cell_html([self.p1char1, self.p1char2, self.p1char3], icon_dir)
        p2team = self.team_cell_html([self.p2char1, self.p2char2, self.p2char3], icon_dir)
        link_html = f'<a href="{self.url}" class="yt_button"></a>'
        return f"<tr>" \
                   f"<td class=\"name p1\">{self.p1name}</td>" \
                   f"<td class=\"team p1\"><div class=\"container\">{p1team}</div></td>" \
                   f"<td class=\"team p2\"><div class=\"container\">{p2team}</div></td>" \
                   f"<td class=\"name p2\">{self.p2name}</td>" \
                   f"<td class=\"link\">{link_html}</td>" \
               f"</tr>"

    # HTML table header that displays info about the event this vod is a part of
    # (Called whenever the event name changes during the loop)
    def table_header_html(self):
        formatted_date = self.date.strftime('%-d %b %Y')
        event = self.event.replace("Skullgirls OCE ", "")
        return f"<tr class=\"event\">" \
               f"<th colspan=\"4\" class=\"name\">{event}</th>" \
               f"<th class=\"date\">{formatted_date}</th>" \
               f"</tr>"

    # Returns a csv row representation of a Vod
    def to_csv_row(self):
        # Format date as YYYY-MM-DD
        formatted_date = self.date.strftime('%Y-%m-%d')
        # Encapsulate any comma-containing fields in ""
        event   = (f"\"{self.event}\""  if "," in self.event  else self.event)
        p1name  = (f"\"{self.p1name}\"" if "," in self.p1name else self.p1name)
        p2name  = (f"\"{self.p2name}\"" if "," in self.p2name else self.p2name)
        # Convert netplay flag to binary
        netplay = ("1" if self.netplay else "0")
        return f"{event},{formatted_date},{self.region},{netplay},{self.version}," \
               f"{p1name},{self.p1char1},{self.p1char2},{self.p1char3}," \
               f"{p2name},{self.p2char1},{self.p2char2},{self.p2char3},{self.url}"
