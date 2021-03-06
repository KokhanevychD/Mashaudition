from django import forms

from patern.models import PatternBody, PatternType


class PatternBodyForm(forms.ModelForm):
    class Meta:
        model = PatternBody
        fields = ['pattern']


class PatternTypeForm(forms.ModelForm):
    class Meta:
        model = PatternType
        fields = '__all__'
