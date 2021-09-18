from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView

from .models import Vod, csv_header
from .forms import FilterForm


# Return a list of vods that the user is interested in
# TODO: make this nice and paged
def index(request):
    # If the user used the search form:
    if request.GET:
        # Filter vods + pre-fill the filter form with previous selections
        vods = filtered_vods(request.GET)
        form = FilterForm(request.GET)
    else:
        # Otherwise, get ALL vods + return an empty filter form
        vods = Vod.objects.all()
        form = FilterForm()
    # Finally, order the results by newest first and return
    vods = vods.order_by('-date')
    
    # Read icon_dir from the cookies, use a default value if not found, and validate
    # TODO: Store the icon dir list in some config/setting so it's not hardcoded in two different places and is easy to update
    icon_dir = request.COOKIES.get('icon_dir', 'charselect')
    if icon_dir not in ['charselect', 'emoji', 'sigil']:
        icon_dir = 'charselect'

    return render(request, 'viewer/index.html', {'vods': vods, 'form': form, 'icon_dir': icon_dir})


# Return a plain, csv-formatted page of every vod that can easily be used for backups
def csv(request):
    vods = Vod.objects.all().order_by('-date')
    output = csv_header() + "\n" + "\n".join([v.to_csv_row() for v in vods])
    return HttpResponse(output, content_type='text/plain')


# Function that returns a filtered QuerySet of vods according to user input
def filtered_vods(filter_dict):
    # Start with every vod
    vods = Vod.objects.all()

    # Filter event
    event = filter_dict.get('event', "")
    vods = vods.filter(event__icontains=event)

    # If you want to add more filters (region, version, etc), 
    # do it here before it gets complicated!

    # Filter player names
    # Since we want to capture "A vs B" as well as "B vs A", we need to create 
    # two cases - one where P1/P2 is the right way around, and one backwards.
    p1name = filter_dict.get('p1name', "")
    p2name = filter_dict.get('p2name', "")
    vods1 = vods.filter(p1name__icontains=p1name).filter(p2name__icontains=p2name)
    vods2 = vods.filter(p1name__icontains=p2name).filter(p2name__icontains=p1name)

    # Filter teams.
    # Since there are 6 selections, multiplied by 2 different ways the player
    # names can be around, plus a "team order matters" factor, this gets long.
    p1char1 = filter_dict.get('p1char1', "Any")
    p1char2 = filter_dict.get('p1char2', "Any")
    p1char3 = filter_dict.get('p1char3', "Any")
    p2char1 = filter_dict.get('p2char1', "Any")
    p2char2 = filter_dict.get('p2char2', "Any")
    p2char3 = filter_dict.get('p2char3', "Any")
    team_order_matters = filter_dict.get('teamorder', False)
    if team_order_matters:
        if p1char1 != 'Any': 
            vods1 = vods1.filter(p1char1=p1char1)
            vods2 = vods2.filter(p2char1=p1char1)
        if p1char2 != 'Any': 
            vods1 = vods1.filter(p1char2=p1char2)
            vods2 = vods2.filter(p2char2=p1char2)
        if p1char3 != 'Any': 
            vods1 = vods1.filter(p1char3=p1char3)
            vods2 = vods2.filter(p2char3=p1char3)
        if p2char1 != 'Any': 
            vods1 = vods1.filter(p2char1=p2char1)
            vods2 = vods2.filter(p1char1=p2char1)
        if p2char2 != 'Any': 
            vods1 = vods1.filter(p2char2=p2char2)
            vods2 = vods2.filter(p1char2=p2char2)
        if p2char3 != 'Any': 
            vods1 = vods1.filter(p2char3=p2char3)
            vods2 = vods2.filter(p1char3=p2char3)
    else:
        if p1char1 != 'Any': 
            vods1 = vods1.filter(p1char1=p1char1) | vods1.filter(p1char2=p1char1) | vods1.filter(p1char3=p1char1)
            vods2 = vods2.filter(p2char1=p1char1) | vods2.filter(p2char2=p1char1) | vods2.filter(p2char3=p1char1)
        if p1char2 != 'Any': 
            vods1 = vods1.filter(p1char1=p1char2) | vods1.filter(p1char2=p1char2) | vods1.filter(p1char3=p1char2)
            vods2 = vods2.filter(p2char1=p1char2) | vods2.filter(p2char2=p1char2) | vods2.filter(p2char3=p1char2)
        if p1char3 != 'Any': 
            vods1 = vods1.filter(p1char1=p1char3) | vods1.filter(p1char2=p1char3) | vods1.filter(p1char3=p1char3)
            vods2 = vods2.filter(p2char1=p1char3) | vods2.filter(p2char2=p1char3) | vods2.filter(p2char3=p1char3)
        if p2char1 != 'Any': 
            vods1 = vods1.filter(p2char1=p2char1) | vods1.filter(p2char2=p2char1) | vods1.filter(p2char3=p2char1)
            vods2 = vods2.filter(p1char1=p2char1) | vods2.filter(p1char2=p2char1) | vods2.filter(p1char3=p2char1)
        if p2char2 != 'Any': 
            vods1 = vods1.filter(p2char1=p2char2) | vods1.filter(p2char2=p2char2) | vods1.filter(p2char3=p2char2)
            vods2 = vods2.filter(p1char1=p2char2) | vods2.filter(p1char2=p2char2) | vods2.filter(p1char3=p2char2)
        if p2char3 != 'Any': 
            vods1 = vods1.filter(p2char1=p2char3) | vods1.filter(p2char2=p2char3) | vods1.filter(p2char3=p2char3)
            vods2 = vods2.filter(p1char1=p2char3) | vods2.filter(p1char2=p2char3) | vods2.filter(p1char3=p2char3)

    # If I could be bothered, here is where I would count how many N's were
    # selected, and make sure the teams have at least that many. Right now eg.
    # FI/N/N will match FI/X/N is order is unchecked, which is not very good

    # Combine the "A vs B" and "B vs A" cases together at the end
    return vods1 | vods2