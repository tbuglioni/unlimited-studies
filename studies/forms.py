from django.forms import ModelForm
from .models import StudiesNotes, Chapter, Book
from django import forms


class StudiesNotesForm(ModelForm):
    class Meta:
        model = StudiesNotes
        fields = ['text_recto', 'text_verso',
                  'studie_recto', 'studie_verso']


class ChapterForm(forms.Form):
    name = forms.CharField(max_length=100)
    order_chapter = forms.IntegerField(
        min_value=1, max_value=100, required=False)
    chapter_id = forms.IntegerField(widget=forms.HiddenInput, required=False)


class BookForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    description = forms.CharField(
        widget=forms.Textarea, max_length=1000, required=False)
    source_info = forms.CharField(
        widget=forms.Textarea, max_length=1000, required=False)
    order_book = forms.IntegerField(min_value=1, max_value=100, required=False)
    book_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
