# -*- coding: utf-8 -*-
from django import forms
from thesau.models import MutationsFile


class MutationsUploadForm(forms.ModelForm):
    class Meta:
        model = MutationsFile
        fields = ('sta_file', 'description', )