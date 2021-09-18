from urllib.parse import urlencode

from django import forms
from django.core.exceptions import ValidationError

from .models import *

# Form for filtering results on the main page
class FilterForm(forms.Form):
    character_filters = [("Any", "Any")] + character_choices
    # Don't allow the user to select "None" for the first character
    first_character_filters = character_filters[:]
    first_character_filters.remove(("N", "None"))
    p1name    = forms.CharField(label='P1 name', required=False, max_length=32)
    p1char1   = forms.ChoiceField(label='P1 char 1', required=False, choices=first_character_filters)
    p1char2   = forms.ChoiceField(label='P1 char 2', required=False, choices=character_filters)
    p1char3   = forms.ChoiceField(label='P1 char 3', required=False, choices=character_filters)
    p2name    = forms.CharField(label='P2 name', required=False, max_length=32)
    p2char1   = forms.ChoiceField(label='P2 char 1', required=False, choices=first_character_filters)
    p2char2   = forms.ChoiceField(label='P2 char 2', required=False, choices=character_filters)
    p2char3   = forms.ChoiceField(label='P2 char 3', required=False, choices=character_filters)
    event     = forms.CharField(label='Event', required=False, max_length=64)
    teamorder = forms.BooleanField(label='Team order matters?', required=False)

    # Validate data
    def clean(self):
        data = super().clean()
        # Check for valid team structure
        for char in [['p1char1', 'p1char2', 'p1char3'], ['p2char1', 'p2char2', 'p2char3']]:
            # Check for duplicate non-N characters
            if (data[char[0]] == data[char[1]] and data[char[0]] not in ['N', 'Any', '']) or \
               (data[char[0]] == data[char[2]] and data[char[0]] not in ['N', 'Any', '']) or \
               (data[char[1]] == data[char[2]] and data[char[1]] not in ['N', 'Any', '']):
                raise ValidationError(f"""Cannot have duplicate characters in a team!""", code='invalid')
            # Check for N's appearing before non-N
            # (but only give a shit if team order was checked)
            if (data['teamorder'] and data[char[1]] == 'N' and data[char[2]] not in ['N', 'Any', '']):
                raise ValidationError(f"Cannot have None before non-None characters in a team!", code='invalid')


# List of the default form values (used in cleaning out url parameters)
default_form_values = [
    ("p1name", ""),
    ("p1char1", "Any"),
    ("p1char2", "Any"),
    ("p1char3", "Any"),
    ("p2name", ""),
    ("p2char1", "Any"),
    ("p2char2", "Any"),
    ("p2char3", "Any"),
    ("event", ""),
    ("teamorder", False)
]


# Determines whether any parameter is present and equal to the default
# (used to determine whether a redirect to a cleaner URL is needed)
def is_clean_filter(filter_dict):
    for field, default_value in default_form_values:
        if field in filter_dict and filter_dict[field] == default_value:
            return False
    return True


# Creates a clean url argument string from a set of filter parameters
def clean_filter_url_parameters(filter_dict):
    # Get only the parameters that matter
    non_default_values = [
        (field, filter_dict[field]) for (field, default_value) in default_form_values
        if field in filter_dict and filter_dict[field] != default_value
    ]
    if non_default_values:
        # If there are any non-default arguments, format it up
        return "/?" + urlencode(non_default_values)
    else:
        # If empty for whatever reason, just go back to the index
        return "/"