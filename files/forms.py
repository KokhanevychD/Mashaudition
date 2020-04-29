from django import forms

from files.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['excel']
