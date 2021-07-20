from django.forms import ModelForm
from .models import StudiesNotes, Chapter, Book


class StudiesNotesForm(ModelForm):
    class Meta:
        model = StudiesNotes
        fields = ['text_recto', 'text_verso',
                  'studie_recto', 'studie_verso']


class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = ["name"]


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["name", "description", "source_info"]
