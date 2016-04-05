# -*- coding utf-8 -*-

from django import forms
from scrumdea import models as scr_models


class ProjectFrom(forms.ModelForm):
    class Meta:
        model = scr_models.Project
        fields = ('name', 'description')