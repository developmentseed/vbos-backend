from django import forms
from .models import TabularDataset


class CSVUploadForm(forms.Form):
    file = forms.FileField(label="File")
    dataset = forms.ModelChoiceField(
        queryset=TabularDataset.objects.all(), empty_label="Select a dataset"
    )
