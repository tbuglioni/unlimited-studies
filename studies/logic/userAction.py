import random
from studies.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from datetime import timedelta
import datetime

from studies.forms import StudiesNotesForm, BookForm, ChapterForm


class UserAction:
    def __init__(self):
        self.name = 1
        self.game_list_auto = []
        self.notes_todo = []
        self.TIME_NOW = datetime.date.today()

    def get_books(self, request):
        books = Book.objects.filter(users=request.user)
        return books

    def get_book_404(self, request, book):
        book = get_object_or_404(Book, pk=book, users=request.user)
        return book

    def create_or_update_book(self, request, context):
        form_book = BookForm(request.POST, instance=context["selectedBook"])
        if form_book.is_valid():
            if context["selectedBook"] is not None:
                form_book.save()
            else:
                newBook = form_book.save(commit=False)
                newBook.order_book = len(
                    Book.objects.filter(users=request.user)) + 1
                newBook.save()
                newBook.users.add(request.user, through_defaults={})
                newBook.save()
            return redirect('studies:personal_home')

    def get_chapters(self, request, book):
        chapters = Chapter.objects.filter(book__users=request.user, book=book)
        return chapters

    def get_chapter_404(self, request, chapter):
        chapter = get_object_or_404(
            Chapter, pk=chapter, book__users=request.user)
        return chapter

    def create_or_update_chapter(self, request, context, book, chapter):
        form_chapter = ChapterForm(request.POST, instance=context["chapter"])
        context["form_chapter"] = form_chapter

        if form_chapter.is_valid():
            if context["chapter"] is not None:
                form_chapter.save()
                return redirect('studies:book_page', book=book, chapter=chapter)
            else:
                chapter = form_chapter.save(commit=False)
                chapter.book = self.get_book_404(request, book)
                chapter.name = form_chapter.cleaned_data["name"]
                chapter.order_chapter = len(
                    self.get_chapters(request, book)) + 1
                chapter.save()

                return redirect('studies:book_page', book=book)

    def get_notes(self, request, chapter):
        notes = StudiesNotes.objects.filter(
            users=request.user, chapter=chapter)
        return notes

    def get_note_404(self, request, note):
        note = get_object_or_404(
            StudiesNotes, pk=note, users=request.user)
        return note

    def __notes_todo(self, request, speed=True, number_of_notes=10):
        """ find notes to run auto game """
        if speed:
            self.notes_todo = StudiesNotesProgression.objects.filter(
                (
                    Q(lvl_recto__lt=6)
                    & Q(notes__studie_recto=True)
                    & Q(next_studied_date_recto__lte=self.TIME_NOW, user=request.user)
                )
                | (
                    Q(lvl_verso__lt=6)
                    & Q(notes__studie_verso=True)
                    & Q(next_studied_date_verso__lte=self.TIME_NOW, user=request.user)
                )
            ).order_by("notes__chapter__book", "notes__chapter")[:number_of_notes]

        else:
            self.notes_todo = StudiesNotesProgression.objects.filter(
                (
                    Q(lvl_recto__gt=5)
                    & Q(notes__studie_verso=True)
                    & Q(next_studied_date_recto__lte=self.TIME_NOW, user=request.user)
                )
                | (
                    Q(lvl_verso__gt=5)
                    & Q(notes__studie_recto=True)
                    & Q(next_studied_date_verso__lte=self.TIME_NOW, user=request.user)
                )
            ).order_by("notes__chapter__book", "notes__chapter")[:number_of_notes]

    def __split_notes(self):
        """ splits selected notes into dict """

        for elt in self.notes_todo:
            if elt.next_studied_date_recto <= self.TIME_NOW and elt.notes.studie_recto is True:
                self.game_list_auto.append({
                    "id": elt.id,
                    "sens": "recto",
                    "text": elt.notes.text_recto,
                    "response": elt.notes.text_verso,
                    "class_button_true": "ajax-true-recto",
                    "class_button_wrong": "ajax-wrong-recto",

                })
            elif elt.next_studied_date_verso <= self.TIME_NOW and elt.notes.studie_verso is True:
                self.game_list_auto.append({
                    "id": elt.id,
                    "sens": "verso",
                    "text": elt.notes.text_verso,
                    "response": elt.notes.text_recto,
                    "class_button_true": "ajax-true-verso",
                    "class_button_wrong": "ajax-wrong-verso",


                })

    def get_notes_todo(self, request, nbr_speed=10, nbr_long=10):
        """ get notes auto mode, split them and return all """
        self.__notes_todo(request, speed=True, number_of_notes=nbr_speed)
        self.__split_notes()
        self.__notes_todo(request, speed=False, number_of_notes=nbr_long)
        self.__split_notes()
        random.shuffle(self.game_list_auto)
        return self.game_list_auto
