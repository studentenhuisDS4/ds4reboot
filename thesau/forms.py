# -*- coding: utf-8 -*-
from django import forms

class MutationsUploadForm(forms.Form):
    docfile = forms.FileField(
        label='Drag a .sta file from ABN, ING, Rabo or any other bank (MT940 format).',
        help_text='Max. 1 megabyte'
    )