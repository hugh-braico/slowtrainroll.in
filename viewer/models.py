from django.db import models
import datetime

# list of valid characters
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

# list of regions
region_list = ["Europe", "Asia", "North America", "Oceania", "South America"]

# TODO: generate (and cache) a distinct, alphabetised list of all events
event_list = None

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

    # HTML table row that displays all the info about this vod
    def table_row_html(self):
        p1team =f"{self.p1char1}" + \
               (f"/{self.p1char2}"  if self.p1char2 != "N" else "") + \
               (f"/{self.p1char3}" if self.p1char3 != "N" else "")
        p2team =f"{self.p2char1}" + \
               (f"/{self.p2char2}"  if self.p2char2 != "N" else "") + \
               (f"/{self.p2char3}" if self.p2char3 != "N" else "")
        link_html = f"<a href=\"{self.url}\">(Link)</a>"
        return f"<tr>" \
                   f"<td class=\"name p1\">{self.p1name}</td>" \
                   f"<td class=\"team p1\">{p1team}</td>" \
                   f"<td class=\"team p2\">{p2team}</td>" \
                   f"<td class=\"name p2\">{self.p2name}</td>" \
                   f"<td class=\"link\">{link_html}</td>" \
               f"</tr>"
            
    # HTML table header that displays info about the event this vod is a part of
    # (Called whenever the event name changes during the loop)
    def table_header_html(self):
        formatted_date = f"{self.date.strftime('%Y-%m-%d')}"
        event = self.event.replace("Skullgirls OCE ", "")
        return f"<tr class=\"event\">" \
               f"<th colspan=\"4\" class=\"name\">{event}</th>" \
               f"<th class=\"date\">{formatted_date}</th>" \
               f"</tr>"