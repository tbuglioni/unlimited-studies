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
        """ get all books from 1 user """
        books = Book.objects.filter(users=request.user)
        return books

    def get_book_404(self, request, book):
        """ get 1 book from 1 user """
        book = get_object_or_404(Book, pk=book, users=request.user)
        return book

    def create_or_update_book(self, request, context):
        """ create a new book or update an existing one """
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
        """ get all chapters from 1 user in 1 book"""
        chapters = Chapter.objects.filter(book__users=request.user, book=book)
        return chapters

    def get_chapter_404(self, request, chapter):
        """ get 1 chapter from 1 user in 1 book"""
        chapter = get_object_or_404(
            Chapter, pk=chapter, book__users=request.user)
        return chapter

    def create_or_update_chapter(self, request, context, book, chapter):
        """ create a new chapter or update an existing one """
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
        """ get all notes from 1 user in 1 chapter """
        notes = StudiesNotes.objects.filter(
            users=request.user, chapter=chapter)
        return notes

    def get_note_404(self, request, note):
        """ get 1 note from 1 user in 1 chapter """
        note = get_object_or_404(
            StudiesNotes, pk=note, users=request.user)
        return note

    def create_or_update_note(self, request, context, chapter):
        """ create a new chapter or update an existing one """
        form = StudiesNotesForm(
            request.POST, instance=context["instance_note"])
        context["form"] = form

        if form.is_valid():
            if context["instance_note"] is not None:
                form.save()
            else:
                obj = form.save(commit=False)

                obj.order_note = len(
                    self.get_notes(request, chapter)) + 1
                obj.chapter = self.get_chapter_404(request, chapter)
                obj.save()
                obj.users.add(request.user, through_defaults={})
                obj.save()
