from django import forms
from .models import Video


# Form for adding a new video
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name', 'url', 'notes']


# Form to search through list of videos
class SearchForm(forms.Form):
    search_term = forms.CharField()