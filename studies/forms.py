from django import forms


class StudiesNotesForm(forms.Form):

    text_recto = forms.CharField(
        widget=forms.Textarea, max_length=1000, required=False)
    text_verso = forms.CharField(
        widget=forms.Textarea, max_length=1000, required=False)
    studie_recto = forms.BooleanField(required=False)
    studie_verso = forms.BooleanField(required=False)
    note_id = forms.IntegerField(widget=forms.HiddenInput, required=False)


class ChapterForm(forms.Form):
    name = forms.CharField(max_length=100)
    order_chapter = forms.IntegerField(
        min_value=1, max_value=100, required=False)
    chapter_id = forms.IntegerField(widget=forms.HiddenInput, required=False)


class BookForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    description = forms.CharField(
        widget=forms.Textarea, max_length=1000, required=False
    )
    source_info = forms.CharField(
        widget=forms.Textarea, max_length=1000, required=False
    )
    order_book = forms.IntegerField(min_value=1, max_value=100, required=False)
    book_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
