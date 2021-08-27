import random
from studies.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from datetime import timedelta
import datetime

from studies.forms import StudiesNotesForm, BookForm, ChapterForm


class UserAction:

    def get_books(self, request):
        """ get all books from 1 user """
        books = Book.objects.filter(users=request.user, userbookmany__to_accept=False).order_by(
            'userbookmany__order_book')
        return books

    def get_UserBookMany(self, request):
        """ get all books from 1 user """
        data = UserBookMany.objects.filter(user=request.user, to_accept=False)
        return data

    def get_book_404(self, request, book):
        """ get 1 book from 1 user """
        book = get_object_or_404(Book, pk=book, users=request.user)
        return book

    def create_or_update_book(self, request, context):
        """ create a new book or update an existing one """
        form_book = BookForm(request.POST)

        if form_book.is_valid():
            if context["selectedBook"] is not None:
                name = form_book.cleaned_data['name']
                description = form_book.cleaned_data['description']
                source_info = form_book.cleaned_data['source_info']
                order_book = form_book.cleaned_data['order_book']
                book_id = form_book.cleaned_data['book_id']
                
                if name :
                    Book.objects.filter(id=book_id, users=request.user).update(
                    name=name, description=description, source_info=source_info)

                books_before = UserBookMany.objects.filter(user=request.user,to_accept=False).order_by(
                    'order_book').exclude(book=book_id, user=request.user)[:(order_book-1)]
                books_after = UserBookMany.objects.filter(user=request.user,to_accept=False).order_by(
                    'order_book').exclude(book=book_id, user=request.user)[(order_book-1):]
                loop = 1

                for elt in books_before:
                    elt.order_book = loop
                    loop += 1
                    elt.save()

                UserBookMany.objects.filter(
                    book=book_id, user=request.user).update(order_book=loop)
                loop += 1

                for elt in books_after:
                    elt.order_book = loop
                    loop += 1
                    elt.save()

            else:
                name = form_book.cleaned_data['name']
                description = form_book.cleaned_data['description']
                source_info = form_book.cleaned_data['source_info']
                new_book = Book.objects.create(
                    name=name, description=description, source_info=source_info)

                book_counter = UserBookMany.objects.filter(
                    user=request.user, to_accept=False).count() + 1
                new_book.users.add(request.user, through_defaults={
                                   "order_book": book_counter})
                new_book.save()

        else:
            print('error')
        return redirect('home')

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
        form_chapter = ChapterForm(request.POST)
        context["form_chapter"] = form_chapter

        if form_chapter.is_valid():
            if context["chapter"] is not None:
                name = form_chapter.cleaned_data['name']
                order_chapter = form_chapter.cleaned_data['order_chapter']
                chapter_id = form_chapter.cleaned_data['chapter_id']
                Chapter.objects.filter(id=chapter_id, book__users=request.user).update(
                    name=name, order_chapter=order_chapter)

                chapters_before = Chapter.objects.filter(
                    book=book, book__users=request.user).order_by('order_chapter').exclude(id=chapter_id)[:(order_chapter-1)]
                chapters_after = Chapter.objects.filter(
                    book=book, book__users=request.user).order_by('order_chapter').exclude(id=chapter_id)[(order_chapter-1):]
                loop = 1

                for elt in chapters_before:
                    elt.order_chapter = loop
                    loop += 1
                    elt.save()

                Chapter.objects.filter(
                    id=chapter_id, book=book).update(order_chapter=loop)
                loop += 1

                for elt in chapters_after:
                    elt.order_chapter = loop
                    loop += 1
                    elt.save()

            else:
                name = form_chapter.cleaned_data['name']
                chapter_counter = Chapter.objects.filter(
                    book=book, book__users=request.user).count() + 1

                Chapter.objects.create(
                    name=name, order_chapter=chapter_counter, book=context["book"])

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

                obj.order_note = self.get_notes(request, chapter).count() + 1
                obj.chapter = self.get_chapter_404(request, chapter)
                obj.save()
                obj.users.add(request.user, through_defaults={})
                obj.save()
