from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from studies.logic.userAction import UserAction
from studies.forms import StudiesNotesForm, BookForm, ChapterForm
from django.db.models import Avg, Max, Min

user_action = UserAction()


def personal_home_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    # context["form_chapter"] = ChapterForm()
    # context["books"] = user_action.get_books(request)
    context = user_action.get_books(request)
    if request.POST:
        form_book = BookForm(request.POST)
        if form_book.is_valid():

            book = form_book.save(commit=False)
            book.order_book = len(Book.objects.filter(users=request.user)) + 1
            book.save()
            book.users.add(request.user, through_defaults={
                'user_fonction': "owner", "level_chapter": 1})
            book.save()
            return redirect('studies:personal_home')
        else:
            context["form_book"] = form_book

    return render(request, "studies/personal_home.html", context)


def book_view(request, book, chapter=None):
    """ book with 0/1 selected chapter"""
    context = {}
    context["book"] = get_object_or_404(Book,
                                        users=request.user, pk=book)
    context["chapters"] = Chapter.objects.filter(book=book)

    if chapter is not None:
        context["notes"] = StudiesNotes.objects.filter(chapter=chapter)

    if request.POST:
        form_chapter = ChapterForm(request.POST)
        context["form_chapter"] = form_chapter
        if form_chapter.is_valid():
            chapter = Chapter.objects.create(
                book=Book.objects.get(pk=book, users=request.user), name=form_chapter.cleaned_data["name"],
                order_chapter=len(Chapter.objects.filter(book=book)) + 1)
            return redirect('studies:book_page', book=book, chapter=chapter.id)
    else:
        form_chapter = ChapterForm()
        context["form_chapter"] = form_chapter

    return render(request, "studies/book.html", context)


def note_add_or_update(request, chapter=None, note=None):
    """ 1 note to add / change """
    context = {}
    context["chapter"] = chapter
    book = Chapter.objects.get(pk=chapter).book.id

    if note is not None:
        instance_note = StudiesNotes.objects.get(
            chapter__book__users=request.user, pk=note)

        context["instance_note"] = instance_note  # update note

    else:
        instance_note = None  # new note

        context["instance_note"] = instance_note

    if request.POST:

        form = StudiesNotesForm(request.POST, instance=instance_note)
        context["form"] = form

        if form.is_valid():
            if instance_note is not None:
                form.save()
            else:
                obj = form.save(commit=False)

                obj.order_note = len(
                    StudiesNotes.objects.filter(users=request.user, chapter__pk=chapter)) + 1
                obj.chapter = Chapter.objects.get(pk=chapter)
                obj.save()

            return redirect('studies:book_page', chapter=chapter, book=book)

    else:
        context["form"] = StudiesNotesForm(instance=instance_note)
    return render(request, "studies/note.html", context)


def delete_book(request, book):
    selected_book = get_object_or_404(Book, pk=book, users=request.user)
    selected_book.delete()

    return redirect('studies:personal_home')


def delete_chapter(request, chapter):
    selected_chapter = get_object_or_404(
        Chapter, pk=chapter, book__users=request.user)
    book = selected_chapter.book.id
    selected_chapter.delete()
    return redirect('studies:book_page', book=book)


def delete_note(request, note):
    selected_note = get_object_or_404(
        StudiesNotes, pk=note, chapter__book__users=request.user)
    book = selected_note.chapter.book.id
    chapter = selected_note.chapter.id
    selected_note.delete()
    return redirect('studies:book_page', book=book, chapter=chapter)


def add_data_in_db(request):
    if not request.user.is_authenticated:
        return redirect("login")

    italien, created = Book.objects.get_or_create(
        name="italien",
        order_book=1,
        description="hello world in italia", source_info='wikipedia is bad :)')

    italien.users.add(request.user, through_defaults={
                      'user_fonction': "owner", "level_chapter": 3})

    anglais, created = Book.objects.get_or_create(
        name="anglais",
        order_book=2,
        description="hello world in england", source_info='wikipedia is bad :)')

    anglais.users.add(request.user, through_defaults={
                      'user_fonction': "owner", "level_chapter": 2})

    francais, created = Book.objects.get_or_create(
        name="francais",
        order_book=3,
        description="hello world in france", source_info='wikipedia is bad :)')

    francais.users.add(request.user, through_defaults={
        'user_fonction': "owner", "level_chapter": 2})

    vocabulaire_it, created = Chapter.objects.get_or_create(
        name="vocabulaire",
        order_chapter=1,
        book=italien,
    )

    vocabulaire_en, created = Chapter.objects.get_or_create(
        name="vocabulaire",
        order_chapter=1,
        book=anglais,
    )
    vocabulaire_fr, created = Chapter.objects.get_or_create(
        name="vocabulaire",
        order_chapter=1,
        book=francais,
    )

    word_it_1, created = StudiesNotes.objects.get_or_create(
        text_recto="bongiorno",
        text_verso="bonjour",
        chapter=vocabulaire_it,
        order_note=1,
        studie_verso=True,

    )

    word_it_1.users.add(request.user, through_defaults={
        'lvl_recto': "4", "lvl_verso": 3})

    word_it_2, created = StudiesNotes.objects.get_or_create(
        text_recto="ciao",
        text_verso="salut",
        chapter=vocabulaire_it,
        order_note=2,
        studie_verso=True,

    )
    word_it_2.users.add(request.user, through_defaults={
        'lvl_recto': "3", "lvl_verso": 2})

    word_it_3, created = StudiesNotes.objects.get_or_create(
        text_recto="grazie",
        text_verso="merci",
        chapter=vocabulaire_it,
        order_note=3,
        studie_verso=True,

    )

    word_it_3.users.add(request.user, through_defaults={
        'lvl_recto': "2", "lvl_verso": 1})

    return redirect('studies:personal_home')
