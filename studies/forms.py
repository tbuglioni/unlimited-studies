from django.forms import ModelForm
from .models import StudiesNotes


class StudiesNotesForm(ModelForm):
    class Meta:
        model = StudiesNotes
        fields = ['text_recto', 'text_verso',
                  'studie_recto', 'studie_verso', 'order_note', "chapter"]
