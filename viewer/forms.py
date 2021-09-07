from django import forms

from .models import *

# Form for filtering results on the main page
class FilterForm(forms.Form):
    character_filters = [("Any", "Any")] + character_choices
    p1name    = forms.CharField(label='P1 name', required=False, max_length=32)
    p1char1   = forms.ChoiceField(label='P1 char 1', required=False, choices=character_filters)
    p1char2   = forms.ChoiceField(label='P1 char 2', required=False, choices=character_filters)
    p1char3   = forms.ChoiceField(label='P1 char 3', required=False, choices=character_filters)
    p2name    = forms.CharField(label='P2 name', required=False, max_length=32)
    p2char1   = forms.ChoiceField(label='P2 char 1', required=False, choices=character_filters)
    p2char2   = forms.ChoiceField(label='P2 char 2', required=False, choices=character_filters)
    p2char3   = forms.ChoiceField(label='P2 char 3', required=False, choices=character_filters)
    event     = forms.CharField(label='Event', required=False, max_length=64)
    teamorder = forms.BooleanField(label='Team order matters?', required=False)

    # Input validation TODO
    def is_valid(self):
        # - Check for duplicate non-N characters (FI/FI/N)
        # - Check for N before not-N (N/FI/N)
        # - Sanitize text fields
        return True
